from __future__ import annotations

import ast
from typing import List, Union

from chalk.parsed.duplicate_input_gql import PositionGQL, RangeGQL


def node_to_range(node: ast.AST) -> RangeGQL:
    return RangeGQL(
        start=PositionGQL(
            line=node.lineno,
            character=node.col_offset,
        ),
        end=PositionGQL(
            line=node.end_lineno,
            character=node.end_col_offset,
        ),
    )


def get_class_definition_range(cls: ast.ClassDef, filename: str) -> RangeGQL:
    with open(filename) as f:
        lines = f.readlines()

    line_length = len(lines[cls.lineno - 1]) if cls.lineno < len(lines) else len("class ") + len(cls.name)
    return RangeGQL(
        start=PositionGQL(
            line=cls.lineno,
            character=0,
        ),
        end=PositionGQL(
            line=cls.lineno,
            character=max(line_length - 1, 1),
        ),
    )


def get_decorator_kwarg_value_range(cls: ast.ClassDef, kwarg: str) -> Union[ast.AST, None]:
    for stmt in cls.decorator_list:
        if isinstance(stmt, ast.Call):
            for keyword in stmt.keywords:
                if keyword.arg == kwarg:
                    return keyword.value
    return None


def get_property_range(cls: ast.ClassDef, name: str) -> Union[ast.AST, None]:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            return stmt.target

        elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return target

    return None


def get_property_value_call_range(cls: ast.ClassDef, name: str, kwarg: str) -> Union[ast.AST, None]:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            if stmt.value is None:
                return None
            value = stmt.value
            if isinstance(value, ast.Call):
                for k in value.keywords:
                    if k.arg == kwarg:
                        return k.value

        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                value = stmt.value
                if isinstance(value, ast.Call):
                    for k in value.keywords:
                        if k.arg == kwarg:
                            return k.value

    return None


def get_property_value_range(cls: ast.ClassDef, name: str) -> Union[ast.AST, None]:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            if stmt.value is None:
                return None

            return stmt.value

        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return stmt.value

    return None


def get_annotation_range(cls: ast.ClassDef, name: str) -> Union[ast.AST, None]:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            return stmt.annotation

    return None


_RESOLVER_DECORATORS = {"online", "offline", "realtime", "batch", "stream", "sink"}


def get_function_decorator_range(node: ast.FunctionDef) -> Union[ast.Name, None]:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id in _RESOLVER_DECORATORS:
            return decorator

    return None


def get_function_arg_values(node: ast.FunctionDef) -> List[Union[ast.arg, None]]:
    arg_values = []
    for stmt in node.args.args:
        if isinstance(stmt, ast.arg):
            arg_value = stmt
        else:
            arg_value = None
        arg_values.append(arg_value)
    return arg_values


def get_function_arg_annotations(node: ast.FunctionDef) -> List[Union[ast.AST, None]]:
    return [stmt.annotation for stmt in node.args.args]


def get_function_return_annotation(node: ast.FunctionDef) -> Union[RangeGQL, None]:
    if node.returns is not None:
        return node_to_range(node.returns)

    return None


class _ChalkFunctionReturnFinder(ast.NodeVisitor):
    def __init__(self):
        self.nodes = []

    def visit_Return(self, node: ast.FunctionDef) -> None:
        self.nodes.append(node)
        self.generic_visit(node)


def get_function_return_statement(node: ast.FunctionDef) -> List[Union[RangeGQL, None]]:
    returns = []
    return_finder = _ChalkFunctionReturnFinder()
    return_finder.visit(node)
    for return_stmt in return_finder.nodes:
        returns.append(node_to_range(return_stmt))
    return returns


def get_function_return_annotation_node(node: ast.FunctionDef) -> Union[ast.AST, None]:
    return node.returns
