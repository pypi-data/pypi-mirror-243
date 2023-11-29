from typing import List, Type, Union

import numpy as np

from chalk.embeddings.provider import Provider
from chalk.features._vector import Vector
from chalk.utils.missing_dependency import missing_dependency_exception

try:
    import cohere
except ImportError:
    cohere = None

supported_models = [
    "embed-english-v3.0",
    "embed-multilingual-v3.0",
    "embed-english-light-v3.0",
    "embed-multilingual-light-v3.0",
]


class CohereProvider(Provider):
    def __init__(self, model: str) -> None:
        super().__init__(model)

        supported_models_str = ", ".join(f"'{model}'" for model in supported_models)
        assert (
            self.model in supported_models
        ), f"Unsupported model '{self.model}' for Cohere. The supported models are [{supported_models_str}]."

    def generate_embedding(self, input: Union[str, List[str]]) -> Union[Vector, List[Vector]]:
        if not cohere:
            raise missing_dependency_exception("chalkpy[cohere]")

        co = cohere.Client()
        text_input = [input] if isinstance(input, str) else input
        response = co.embed(texts=text_input, model=self.model, input_type="search_document")
        vectors = [Vector(np.array(embedding)) for embedding in response.embeddings]
        if isinstance(input, str):
            return vectors[0]
        return vectors

    def get_vector_class(self) -> Type[Vector]:
        if self.model in ["embed-english-v3.0", "embed-multilingual-v3.0"]:
            return Vector[1024]
        else:  # if self.model in ["embed-english-light-v3.0", "embed-multilingual-light-v3.0"]
            return Vector[384]
