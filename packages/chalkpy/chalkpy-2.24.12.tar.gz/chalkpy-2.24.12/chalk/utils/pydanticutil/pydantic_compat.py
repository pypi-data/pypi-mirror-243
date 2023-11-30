from inspect import isclass
from typing import Any

# Unflagged import here because we want whatever the user imported
from pydantic import BaseModel as BaseBaseModel
from typing_extensions import TypeGuard


def is_pydantic_basemodel(type_: type) -> TypeGuard[BaseBaseModel]:
    """Check if a type is a Pydantic BaseModel."""

    from pydantic import BaseModel

    return isclass(type_) and issubclass(type_, BaseModel)


def is_pydantic_basemodel_instance(v: Any) -> bool:
    from pydantic import BaseModel

    return isinstance(v, BaseModel)


def is_pydantic_v1() -> bool:
    """
    True if pydantic is v1, else False
    """
    try:
        import pydantic.v1
    except:
        return True
    else:
        return False
