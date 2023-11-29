from chalk.embeddings.cohere import CohereProvider
from chalk.embeddings.openai import OpenAIProvider
from chalk.embeddings.provider import Provider


def get_provider(provider: str, model: str) -> Provider:
    if provider == "openai":
        return OpenAIProvider(model)
    elif provider == "cohere":
        return CohereProvider(model)
    raise ValueError("Unsupported embedding provider: {provider}. The supported providers are ['openai', 'cohere'].")
