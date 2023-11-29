from __future__ import annotations

import ast
import inspect
import weakref
from collections import defaultdict
from typing import TYPE_CHECKING, List, Mapping, Optional, Type, Union

import Levenshtein
from executing import Source

from chalk._lsp.finders import (
    get_annotation_range,
    get_class_definition_range,
    get_decorator_kwarg_value_range,
    get_function_arg_annotations,
    get_function_arg_values,
    get_function_decorator_range,
    get_function_return_annotation,
    get_function_return_statement,
    get_property_range,
    get_property_value_call_range,
    get_property_value_range,
    node_to_range,
)
from chalk.parsed.duplicate_input_gql import (
    CodeActionGQL,
    CodeDescriptionGQL,
    DiagnosticGQL,
    DiagnosticRelatedInformationGQL,
    DiagnosticSeverityGQL,
    LocationGQL,
    PositionGQL,
    RangeGQL,
    TextDocumentEditGQL,
    TextDocumentIdentifierGQL,
    TextEditGQL,
    WorkspaceEditGQL,
)
from chalk.utils.string import oxford_comma_list

if TYPE_CHECKING:
    import types


class DiagnosticBuilder:
    def __init__(
        self,
        severity: DiagnosticSeverityGQL,
        message: str,
        uri: str,
        range: RangeGQL,
        label: str,
        code: str,
        code_href: str | None,
    ):
        self.uri = uri
        self.diagnostic = DiagnosticGQL(
            range=range,
            message=message,
            severity=severity,
            code=code,
            codeDescription=CodeDescriptionGQL(href=code_href) if code_href is not None else None,
            relatedInformation=[
                DiagnosticRelatedInformationGQL(
                    location=LocationGQL(uri=uri, range=range),
                    message=label,
                )
            ],
        )

    def with_range(
        self,
        range: RangeGQL | ast.AST | None,
        label: str,
    ) -> DiagnosticBuilder:
        if isinstance(range, ast.AST):
            range = node_to_range(range)
        if range is None:
            return self

        self.diagnostic.relatedInformation.append(
            DiagnosticRelatedInformationGQL(
                location=LocationGQL(
                    uri=self.uri,
                    range=range,
                ),
                message=label,
            )
        )
        return self


_dummy_builder = DiagnosticBuilder(
    severity=DiagnosticSeverityGQL.Error,
    message="",
    uri="",
    range=RangeGQL(
        start=PositionGQL(line=0, character=0),
        end=PositionGQL(line=0, character=0),
    ),
    label="",
    code="",
    code_href=None,
)


class LSPErrorBuilder:
    lsp: bool = False
    """This should ONLY be True if we're running `chalk export`.
    DO NOT SET THIS TO TRUE IN ANY OTHER CONTEXT.
    Talk to Elliot if you think you need to set this to True."""

    all_errors: Mapping[str, list[DiagnosticGQL]] = defaultdict(list)
    all_edits: list[CodeActionGQL] = []

    _exception_map: dict[int, (str, DiagnosticGQL)] = {}
    _strong_refs: dict[int, Exception] = {}
    """Maintain exception_map's keys `id(exception)`.
    This could be done better with weakrefs, but you
    cant naively use a weakref.WeakKeyDictionary because
    we can't depend on the __eq__ method of the exception
    object."""

    @classmethod
    def save_exception(cls, e: Exception, uri: str, diagnostic: DiagnosticGQL):
        """Save an exception to be promoted to a diagnostic later.
        Some exceptions are handled (e.g. hasattr(...) handles AttributeError)
        and should not become diagnostics unless the error isn't handled."""
        cls._exception_map[id(e)] = (uri, diagnostic)
        cls._strong_refs[id(e)] = e

    @classmethod
    def promote_exception(cls, e: Exception) -> bool:
        """Promote a previously saved exception to a diagnostic.
        Returns whether the exception was promoted."""
        if id(e) in cls._exception_map:
            uri, diagnostic = cls._exception_map[id(e)]
            cls.all_errors[uri].append(diagnostic)
            del cls._exception_map[id(e)]
            del cls._strong_refs[id(e)]
            return True

        return False


class FeatureClassErrorBuilder:
    def __init__(
        self,
        uri: str,
        namespace: str,
        node: ast.ClassDef | None,
    ):
        self.uri = uri
        self.diagnostics: List[DiagnosticGQL] = []
        self.namespace = namespace
        self.node: ast.ClassDef | None = node

    def property_range(self, feature_name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_property_range(cls=self.node, name=feature_name)

    def annotation_range(self, feature_name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_annotation_range(cls=self.node, name=feature_name)

    def property_value_range(self, feature_name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_property_value_range(cls=self.node, name=feature_name)

    def property_value_kwarg_range(self, feature_name: str, kwarg: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_property_value_call_range(cls=self.node, name=feature_name, kwarg=kwarg)

    def decorator_kwarg_value_range(self, kwarg: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_decorator_kwarg_value_range(cls=self.node, kwarg=kwarg)

    def class_definition_range(self) -> RangeGQL | None:
        if self.node is None:
            return None

        return get_class_definition_range(cls=self.node, filename=self.uri)

    def invalid_attribute(
        self,
        item: str,
        candidates: List[str],
        back: int,
    ):
        back = back + 1
        if not LSPErrorBuilder.lsp:
            # Short circuit if we're not in an LSP context. What follows is expensive.
            raise AttributeError(f"Invalid attribute '{item}'.")

        frame: Optional[types.FrameType] = inspect.currentframe()
        i = 0
        while i < back and frame is not None:
            frame = frame.f_back
            i += 1

        if frame is None or i != back:
            raise AttributeError(f"Invalid attribute '{item}'.")

        try:
            node = Source.executing(frame).node
        except Exception:
            raise AttributeError(f"Invalid attribute '{item}'.")

        if "__file__" not in frame.f_locals:
            raise AttributeError(f"Invalid attribute '{item}'.")

        uri = frame.f_locals["__file__"]
        if isinstance(node, ast.Attribute):
            node = RangeGQL(
                start=PositionGQL(
                    line=node.end_lineno,
                    character=node.end_col_offset - len(node.attr),
                ),
                end=PositionGQL(
                    line=node.end_lineno,
                    character=node.end_col_offset,
                ),
            )

        candidates = [f"'{c}'" for c in candidates if not c.startswith("_")]
        message = f"Invalid attribute '{item}'."
        if len(candidates) > 0:
            all_scores = [
                (
                    Levenshtein.distance(item, candidate),
                    candidate,
                )
                for candidate in candidates
            ]
            all_scores.sort(key=lambda x: x[0])

            if len(candidates) > 5:
                prefix = "The closest options are"
                candidates = [c for (_, c) in all_scores[:5]]
            elif len(candidates) == 1:
                prefix = "The only valid option is"
            else:
                prefix = "Valid options are"

            message += f" {prefix} {oxford_comma_list(candidates)}."

        self.add_diagnostic(
            message=message,
            range=node,
            label="Invalid attribute",
            code="55",
            raise_error=AttributeError,
            uri=uri,
        )

    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] | None = None,
        uri: str | None = None,
    ) -> DiagnosticBuilder:
        uri = self.uri if uri is None else uri
        if not LSPErrorBuilder.lsp:
            if raise_error is not None:
                raise raise_error(message)
            return _dummy_builder

        if isinstance(range, ast.AST):
            range = node_to_range(range)

        builder = DiagnosticBuilder(
            severity=severity,
            message=message,
            uri=uri,
            range=range,
            label=label,
            code=code,
            code_href=code_href,
        )

        error = None if raise_error is None else raise_error(message)
        if range is not None:
            # TODO: Raise in here if we don't have the range.
            if error is None:
                self.diagnostics.append(builder.diagnostic)
                LSPErrorBuilder.all_errors[uri].append(builder.diagnostic)
            else:
                LSPErrorBuilder.save_exception(error, uri, builder.diagnostic)
                raise error

        if error is not None:
            raise error

        return builder


class ResolverErrorBuilder:
    def __init__(
        self,
        uri: str,
        node: ast.FunctionDef | None,
    ):
        self.uri = uri
        self.diagnostics: List[DiagnosticGQL] = []
        self.node: ast.FunctionDef | None = node

    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] | None = None,
    ) -> DiagnosticBuilder:
        if isinstance(range, ast.AST):
            range = node_to_range(range)
        builder = DiagnosticBuilder(
            severity=severity,
            message=message,
            uri=self.uri,
            range=range,
            label=label,
            code=code,
            code_href=code_href,
        )
        if range is not None:
            # TODO: Raise in here if we don't have the range.
            self.diagnostics.append(builder.diagnostic)
            LSPErrorBuilder.all_errors[self.uri].append(builder.diagnostic)
        if raise_error is not None:
            raise raise_error(message)
        return builder

    def add_function_decorator_error(
        self,
        message: str,
        label: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: Union[str, None] = None,
    ) -> bool:
        if self.node is None:
            return False

        r = get_function_decorator_range(node=self.node)
        if r is None:
            return False

        self.add_diagnostic(
            range=r,
            label=label,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )
        return True

    def add_function_arg_values_error(
        self,
        index: int,
        message: str,
        label: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: Union[str, None] = None,
    ) -> bool:
        if self.node is None:
            return False

        ranges = get_function_arg_values(node=self.node)
        if ranges == [] or index >= len(ranges):
            return False

        self.add_diagnostic(
            range=ranges[index],
            label=label,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )
        return True

    def add_function_arg_annotations_error(
        self,
        index: int,
        message: str,
        label: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: Union[str, None] = None,
    ) -> bool:
        if self.node is None:
            return False

        ranges = get_function_arg_annotations(node=self.node)
        if ranges == [] or index >= len(ranges):
            return False

        self.add_diagnostic(
            range=ranges[index],
            label=label,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )
        return True

    def add_function_return_annotation_error(
        self,
        message: str,
        label: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: Union[str, None] = None,
    ) -> bool:
        if self.node is None:
            return False

        r = get_function_return_annotation(node=self.node)
        if r is None:
            return False

        self.add_diagnostic(
            range=r,
            label=label,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )
        return True

    def add_function_return_statement_error(
        self,
        index: int,
        message: str,
        label: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: Union[str, None] = None,
    ) -> bool:
        if self.node is None:
            return False

        ranges = get_function_return_statement(self.node)
        if ranges == [] or index >= len(ranges):
            return False

        self.add_diagnostic(
            range=ranges[index],
            label=label,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )
        return True

    def return_annotation(self) -> ast.AST | None:
        if self.node is None:
            return None

        return get_function_return_annotation(self.node)
