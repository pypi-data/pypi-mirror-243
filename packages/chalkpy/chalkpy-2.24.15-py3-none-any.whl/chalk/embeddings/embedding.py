from typing import Any, Callable, List, Optional, Type

from chalk.embeddings.get_provider import get_provider
from chalk.features.feature_field import Feature
from chalk.features.feature_set import Features
from chalk.features.feature_wrapper import unwrap_feature
from chalk.features.resolver import OnlineResolver, Resolver
from chalk.serialization.parsed_annotation import ParsedAnnotation


def embedding(
    input: Callable[[], Any],
    provider: str,
    model: str,
    name: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Any:
    """Specify an embedding feature.

    Parameters
    ----------
    input
        The input for the embedding. This argument is callable
        to allow for forward references to features of the same
        class.
    provider
        The AI provider to use for the embedding.
    model
        The model to generate the embedding.
    """
    embedding_feature = Feature(name=name, owner=owner, tags=tags)
    previous_hook = embedding_feature.hook

    def hook(features: Type[Features]) -> None:
        if previous_hook:
            previous_hook(features)

        embedding_provider = get_provider(provider, model)

        # Manually set the dimensions of the Vector when using embedding
        embedding_feature.typ = ParsedAnnotation(underlying=embedding_provider.get_vector_class())

        def resolver_factory():
            input_content = unwrap_feature(input())
            assert input_content.typ, "The embedding input must have type str"
            assert (
                input_content.namespace == embedding_feature.namespace
            ), f"The embedding input must be from namespace {embedding_feature.namespace}"

            def fn(input_string):
                return embedding_provider.generate_embedding(input_string)

            return OnlineResolver(
                function_definition="",
                filename="",
                fqn=f"__chalk__embedding__.{embedding_feature.fqn}",
                doc=None,
                inputs=[input_content],
                state=None,
                output=Features[embedding_feature],
                fn=fn,
                environment=None,
                tags=embedding_feature.tags,
                machine_type=None,
                default_args=[None],
                owner=embedding_feature.owner,
                timeout=None,
                cron=None,
                when=None,
                data_sources=None,
                max_staleness=None,
            )

        Resolver.add_to_deferred_registry(resolver_factory)

    embedding_feature.hook = hook

    return embedding_feature
