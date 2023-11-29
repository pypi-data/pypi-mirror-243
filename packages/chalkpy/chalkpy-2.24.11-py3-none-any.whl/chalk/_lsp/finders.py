from __future__ import annotations

import ast
import inspect
from typing import Callable, Dict, List, Union

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


def get_decorator_kwarg_value_range(cls: ast.ClassDef, kwarg: str) -> ast.AST | None:
    for stmt in cls.decorator_list:
        if isinstance(stmt, ast.Call):
            for keyword in stmt.keywords:
                if keyword.arg == kwarg:
                    return keyword.value
    return None


def get_property_range(cls: ast.ClassDef, name: str) -> ast.AST | None:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            return stmt.target

        elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return target

    return None


def get_property_value_call_range(cls: ast.ClassDef, name: str, kwarg: str) -> ast.AST | None:
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


def get_property_value_range(cls: ast.ClassDef, name: str) -> ast.AST | None:
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


def get_annotation_range(cls: ast.ClassDef, name: str) -> ast.AST | None:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            return stmt.annotation

    return None


_RESOLVER_DECORATORS = {"online", "offline", "realtime", "batch", "stream", "sink"}


def get_function_decorator_range(node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> ast.AST | None:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id in _RESOLVER_DECORATORS:
            return decorator

    return None


def get_function_arg_values(node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Dict[str, ast.AST | None]:
    return {stmt.arg: stmt for stmt in node.args.args}


def get_function_arg_annotations(node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Dict[str, ast.AST | None]:
    return {stmt.arg: stmt.annotation for stmt in node.args.args}


class _ChalkFunctionReturnFinder(ast.NodeVisitor):
    def __init__(self):
        self.nodes = []

    def visit_Return(self, node: ast.Return) -> None:
        self.nodes.append(node)
        self.generic_visit(node)


def get_function_return_statement(node: ast.FunctionDef) -> List[ast.AST | None]:
    returns = []
    return_finder = _ChalkFunctionReturnFinder()
    return_finder.visit(node)
    for return_stmt in return_finder.nodes:
        returns.append(return_stmt)
    return returns


def get_function_return_annotation(node: ast.FunctionDef) -> ast.AST | RangeGQL | None:
    return node.returns


def get_missing_return_annotation(node: ast.FunctionDef, uri: str) -> RangeGQL | None:
    with open(uri, "r") as f:
        content = f.read()

    lines = content.split("\n")
    if node.args.args:
        line_no = node.args.args[-1].end_lineno
        col_offset = node.args.args[-1].end_col_offset + 1
    else:
        line_no = node.lineno
        col_offset = node.col_offset

    start_line = line_no - 1
    start_char = max(col_offset - 1, 0)

    for i in range(start_line, len(lines)):
        line = lines[i]
        start_char_in_line = start_char if i == start_line else 0
        for j in range(start_char_in_line, len(line)):
            if line[j] == ":":
                return RangeGQL(
                    start=PositionGQL(
                        line=i + 1,
                        character=j,
                    ),
                    end=PositionGQL(
                        line=i + 1,
                        character=j + 1,
                    ),
                )


def get_function_name(node: ast.FunctionDef, uri: str) -> RangeGQL | None:
    with open(uri, "r") as f:
        content = f.read()

    lines = content.split("\n")
    line_no = node.lineno
    col_offset = node.col_offset

    start_line = line_no - 1
    start_char = max(col_offset - 1, 0)

    found_def = False
    def_start_line_no = None
    def_start_col_offset = None
    for i in range(start_line, len(lines)):
        line = lines[i]
        start_char_in_line = start_char if i == start_line else 0
        for j in range(start_char_in_line, len(line)):
            if line[0:j] == "def":
                found_def = True
            if found_def:
                if def_start_line_no is None:
                    if not line[j].isspace():
                        def_start_line_no = i
                        def_start_col_offset = j
                if def_start_line_no is not None:
                    if line[j] == "(":
                        return RangeGQL(
                            start=PositionGQL(
                                line=def_start_line_no + 1,
                                character=def_start_col_offset + 1,
                            ),
                            end=PositionGQL(
                                line=i + 1,
                                character=j,
                            ),
                        )
