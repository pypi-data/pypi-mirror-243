from abc import ABC, abstractmethod
from typing import List, Type, Union

from chalk.features._vector import Vector


class Provider(ABC):
    def __init__(self, model: str) -> None:
        super().__init__()
        self.model = model

    @abstractmethod
    def generate_embedding(self, input: Union[str, List[str]]) -> Union[Vector, List[Vector]]:
        pass

    @abstractmethod
    def get_vector_class(self) -> Type[Vector]:
        pass
