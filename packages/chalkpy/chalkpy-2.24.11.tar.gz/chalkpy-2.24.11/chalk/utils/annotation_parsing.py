import ast
import inspect
import textwrap
from typing import Any, Callable, Dict, Optional

from chalk._lsp.error_builder import ResolverErrorBuilder
from chalk.df.ast_parser import convert_slice, eval_converted_expr


class ResolverAnnotationParser:
    def __init__(
        self,
        resolver: Callable,
        glbs: Optional[Dict[str, Any]],
        lcls: Optional[Dict[str, Any]],
        error_builder: ResolverErrorBuilder,
    ):
        self.resolver = resolver
        self.glbs = glbs
        self.lcls = lcls

        self._args = {arg.arg: arg for arg in self._get_resolver_args()}
        self.builder = error_builder

    def _get_resolver_args(self):
        source = inspect.getsource(self.resolver)
        parsed_source = ast.parse(textwrap.dedent(source))
        assert len(parsed_source.body) == 1
        function_def = parsed_source.body[0]
        assert isinstance(
            function_def, (ast.FunctionDef, ast.AsyncFunctionDef)
        ), f"The resolver must be a function. Received:\n\n{source}"
        args = function_def.args
        all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
        return all_args

    def parse_annotation(self, name: str):
        arg = self._args[name]
        annotation = arg.annotation
        if annotation is None:
            self.builder.add_diagnostic(
                message=(
                    f"Argument '{name}' for resolver '{self.resolver.__name__}' was not defined with a type annotation."
                ),
                code="84",
                label="resolver argument lacks an annotation",
                range=self.builder.function_arg_values()[name],
                raise_error=TypeError,
            )
        if isinstance(annotation, ast.Constant):
            val = annotation.value
            if not isinstance(val, str):
                self.builder.add_diagnostic(
                    message=(f"Argument {name} has a Literal type annotation, but it is not a string"),
                    code="85",
                    label="resolver argument annotation is a Literal that is not a string",
                    range=self.builder.function_arg_annotations()[name],
                    raise_error=TypeError,
                )
            # string of type annotation
            val = ast.parse(val, mode="eval")
            if not isinstance(val, ast.Expr):
                self.builder.add_diagnostic(
                    message=(f"Argument {name} has a Literal type annotation, but it is not a string"),
                    code="86",
                    label="resolver argument annotation is a Literal that is not a string",
                    range=self.builder.function_arg_annotations()[name],
                    raise_error=TypeError,
                )
            annotation = val.body
        if isinstance(annotation, ast.Subscript):
            # All fancy ast parsing would appear within the subscript of a df __getitem__
            annotation = ast.Subscript(
                value=annotation.value,
                slice=convert_slice(annotation.slice),
                ctx=annotation.ctx,
            )
        return eval_converted_expr(annotation, self.glbs, self.lcls)
