import warnings
from typing import Any, Tuple, Union

from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.filter import Filter
from chalk.features.underscore import (
    SUPPORTED_UNDERSCORE_OPS_BINARY,
    SUPPORTED_UNDERSCORE_OPS_UNARY,
    Underscore,
    UnderscoreAttr,
    UnderscoreBinaryOp,
    UnderscoreCall,
    UnderscoreItem,
    UnderscoreRoot,
    UnderscoreUnaryOp,
)

try:
    import polars as pl
except:
    pl = None


SUPPORTED_ARITHMETIC_OPS = {"+", "-", "*", "/", "//", "%", "**"}


def parse_underscore_in_context(exp: Underscore, context: Any, is_pydantic: bool = False) -> Any:
    """
    Parse a (potentially underscore) expression passed in under some "context".
    """
    parsed_exp = _parse_underscore_in_context(
        exp=exp,
        context=context,
        is_pydantic=is_pydantic,
    )
    assert not isinstance(parsed_exp, Underscore)
    return parsed_exp


def _parse_underscore_in_context(exp: Any, context: Any, is_pydantic: bool) -> Any:
    # Features of the dataframe are to be written as a dictionary of the fqn split up mapped to
    # the original features. The dictionary is represented immutably here.
    if not isinstance(exp, Underscore):
        # Recursive call hit non-underscore, deal with later
        return exp

    elif isinstance(exp, UnderscoreRoot):
        return context

    elif isinstance(exp, UnderscoreAttr):
        parent_context = _parse_underscore_in_context(exp=exp._chalk__parent, context=context, is_pydantic=is_pydantic)
        attr = exp._chalk__attr
        from chalk.features.dataframe import DataFrame

        if isinstance(parent_context, DataFrame) and is_pydantic:
            if attr not in parent_context._underlying.schema:
                warnings.warn(
                    f"Attribute {attr} not found in dataframe schema. Returning None. Found expression {exp}."
                )
                return None

            return attr
        else:
            return getattr(parent_context, attr)

    elif isinstance(exp, UnderscoreItem):
        parent_context = _parse_underscore_in_context(exp=exp._chalk__parent, context=context, is_pydantic=is_pydantic)
        key = exp._chalk__key
        return parent_context[key]

    elif isinstance(exp, UnderscoreCall):
        raise NotImplementedError(
            f"Calls on underscores in DataFrames is currently unsupported. Found expression {exp}"
        )

    elif isinstance(exp, UnderscoreBinaryOp):
        if exp._chalk__op in SUPPORTED_UNDERSCORE_OPS_BINARY:
            left = _parse_underscore_in_context(exp=exp._chalk__left, context=context, is_pydantic=is_pydantic)
            right = (
                _parse_underscore_in_context(exp=exp._chalk__right, context=context, is_pydantic=is_pydantic)
                if isinstance(exp._chalk__right, Underscore)
                else exp._chalk__right
            )

            if exp._chalk__op in SUPPORTED_ARITHMETIC_OPS:
                return _eval_arithmetic_expression(left, right, exp._chalk__op)
            else:
                return _eval_expression(left, right, exp._chalk__op)

    elif isinstance(exp, UnderscoreUnaryOp):
        if exp._chalk__op in SUPPORTED_UNDERSCORE_OPS_UNARY:
            operand = _parse_underscore_in_context(exp=exp._chalk__operand, context=context, is_pydantic=is_pydantic)
            return eval(f"{exp._chalk__op} operand", globals(), {"operand": operand})

    raise NotImplementedError(f"Unrecognized underscore expression {exp}")


def _unwrap_and_validate_features(left: FeatureWrapper, right: FeatureWrapper) -> Tuple[Feature, Feature]:
    if isinstance(left, FeatureWrapper) and isinstance(right, FeatureWrapper):
        f_left = unwrap_feature(left)
        f_right = unwrap_feature(right)

        if f_left.root_namespace != f_right.root_namespace:
            raise TypeError(
                f"{f_left} and {f_right} belong to different namespaces. Operations can only be performed on features of the same namespace."
            )

        return f_left, f_right
    raise TypeError(f"Operations between {type(left).__name__} and {type(right).__name__} are not supported")


def _eval_expression(left: Union[FeatureWrapper, Filter], right: Any, op: str):
    try:
        if op == ">":
            return left.__gt__(right)
        elif op == "<":
            return left.__lt__(right)
        elif op == ">=":
            return left.__ge__(right)
        elif op == "<=":
            return left.__le__(right)
        elif op == "==":
            return left.__eq__(right)
        elif op == "!=":
            return left.__ne__(right)
        elif op == "&":
            return left.__and__(right)
        elif op == "|":
            return left.__or__(right)
        elif op == "__getitem__":
            return left.__getitem__(right)
        elif op == "__getattr__":
            return left.__getattr__(right)
    except:
        raise NotImplementedError(
            f"Operation {op} not implemented for {type(left).__name__} and {type(right).__name__}"
        )


def _eval_arithmetic_expression(
    left: Union[FeatureWrapper, float, int], right: Union[FeatureWrapper, float, int], op: str
):
    if pl is None:
        raise NotImplementedError(
            f"Operation {op} not implemented for {type(left).__name__} and {type(right).__name__}"
        )

    if isinstance(left, FeatureWrapper) and isinstance(right, FeatureWrapper):
        f_left, f_right = _unwrap_and_validate_features(left, right)
        left_col = pl.col(str(f_left))
        right_col = pl.col(str(f_right))
    elif isinstance(left, FeatureWrapper):
        left_col = unwrap_feature(left)
        right_col = right
    else:
        left_col = left
        right_col = right

    if op == "+":
        return left_col + right_col
    elif op == "-":
        return left_col - right_col
    elif op == "*":
        return left_col * right_col
    elif op == "/":
        return left_col / right_col
    elif op == "//":
        return left_col // right_col
    elif op == "%":
        return left_col % right_col
    elif op == "**":
        return left_col**right_col

    raise NotImplementedError(f"{op} is not implemented")
