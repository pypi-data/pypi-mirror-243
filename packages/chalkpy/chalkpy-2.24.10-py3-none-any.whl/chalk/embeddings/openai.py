from typing import List, Type, Union

import numpy as np

from chalk.embeddings.provider import Provider
from chalk.features._vector import Vector
from chalk.utils.missing_dependency import missing_dependency_exception

try:
    import openai
except ImportError:
    openai = None


class OpenAIProvider(Provider):
    def __init__(self, model: str) -> None:
        super().__init__(model)

        if self.model != "text-embedding-ada-002":
            raise ValueError(
                f"Unsupported model '{self.model}' for OpenAI. The supported models are ['text-embedding-ada-002']."
            )

    def generate_embedding(self, input: Union[str, List[str]]) -> Union[Vector, List[Vector]]:
        if not openai:
            raise missing_dependency_exception("chalkpy[openai]")

        response = openai.embeddings.create(input=input, model=self.model)
        vectors = [Vector(np.array(entry.embedding)) for entry in response.data]
        if isinstance(input, str):
            return vectors[0]
        return vectors

    def get_vector_class(self) -> Type[Vector]:
        return Vector[1536]
