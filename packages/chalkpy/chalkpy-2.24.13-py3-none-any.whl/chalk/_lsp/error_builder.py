from __future__ import annotations

import ast
import dataclasses
import inspect
import textwrap
import weakref
from collections import defaultdict
from typing import TYPE_CHECKING, Callable, Dict, List, Mapping, Optional, Type, Union

import Levenshtein
from executing import Source

from chalk._lsp._class_finder import get_function_ast
from chalk._lsp.finders import (
    get_annotation_range,
    get_class_definition_range,
    get_decorator_kwarg_value_range,
    get_function_arg_annotations,
    get_function_arg_values,
    get_function_decorator_range,
    get_function_name,
    get_function_return_annotation,
    get_function_return_statement,
    get_missing_return_annotation,
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
    def has_errors(cls):
        return cls.lsp and len(cls.all_errors) > 0

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
    def __init__(self, uri: str, namespace: str, node: ast.ClassDef | None):
        self.uri = uri
        self.diagnostics: List[DiagnosticGQL] = []
        self.namespace = namespace
        self.node = node

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
        node: ast.FunctionDef | ast.AsyncFunctionDef | None,
    ):
        self.uri = uri
        self.diagnostics: List[DiagnosticGQL] = []
        self.node = node

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
        """

        :param message: longform description of error with names of attributes, etc.
        :param label: shortform category of error
        :param code: unique identifier of error kind
        :param range: line number + offset of start and end of text with error
        :param code_href: code_href: link to doc
        :param severity: is it an error? a warning?
        :param raise_error: if we cannot proceed, raise with this error kind and the message.
        :param uri: filepath
        :return:
        """
        if not LSPErrorBuilder.lsp:
            if raise_error is not None:
                raise raise_error(message)
            return _dummy_builder
        uri = self.uri if uri is None else uri

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

    def function_decorator(self) -> ast.AST | None:
        if self.node is None:
            return None

        return get_function_decorator_range(node=self.node)

    def function_arg_values(self) -> Dict[str, ast.AST | None]:
        if self.node is None:
            return {}

        return get_function_arg_values(node=self.node)

    def function_arg_value_by_name(self, name: str) -> ast.AST | None:
        return self.function_arg_values().get(name)

    def function_arg_annotations(self) -> Dict[str, ast.AST | None]:
        if self.node is None:
            return {}

        return get_function_arg_annotations(node=self.node)

    def function_arg_annotation_by_name(self, name: str) -> ast.AST | None:
        return self.function_arg_annotations().get(name)

    def function_return_annotation(self) -> ast.AST | None:
        if self.node is None:
            return None

        node_or_none = get_function_return_annotation(node=self.node)
        return node_or_none or get_missing_return_annotation(self.node, self.uri)

    def function_return_statements(self) -> List[ast.AST | None]:
        if self.node is None:
            return []

        return get_function_return_statement(node=self.node)

    def function_name(self) -> RangeGQL | None:
        if self.node is None:
            return None

        return get_function_name(self.node, self.uri)


@dataclasses.dataclass
class FunctionSource:
    filename: str
    source: str | None
    dedent_source: str | None
    tree: ast.FunctionDef | ast.AsyncFunctionDef | None


def get_resolver_error_builder(fn: Callable) -> ResolverErrorBuilder:
    source_info: Optional[FunctionSource] = None
    try:
        filename = inspect.getfile(fn)
        resolver_source = inspect.getsource(fn)
        dedent_source = resolver_source and textwrap.dedent(resolver_source)
        try:
            tree = get_function_ast(fn)
        except:
            tree = None
        source_info = FunctionSource(
            filename=filename,
            source=resolver_source,
            dedent_source=dedent_source,
            tree=tree,
        )
    except Exception as e:
        pass

    error_builder = ResolverErrorBuilder(
        uri=source_info.filename if source_info is not None else "__main__",
        node=source_info and source_info.tree,
    )
    return error_builder
