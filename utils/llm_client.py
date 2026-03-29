"""
Shared LLM Client Factory
===========================
Creates either an OpenAI or Azure OpenAI client based on environment variables.

Usage:
    from utils.llm_client import get_client, get_model

    client = get_client()
    model = get_model()  # Returns deployment name for Azure, model name for OpenAI

Environment Variables:
    For OpenAI (default):
        OPENAI_API_KEY          - Your OpenAI API key

    For Azure OpenAI:
        USE_AZURE_OPENAI=true   - Enable Azure OpenAI
        AZURE_OPENAI_API_KEY    - Your Azure OpenAI API key
        AZURE_OPENAI_ENDPOINT   - Your Azure endpoint (e.g. https://myresource.openai.azure.com/)
        AZURE_OPENAI_API_VERSION - API version (default: 2024-12-01-preview)
        AZURE_OPENAI_DEPLOYMENT - Deployment name for chat model (default: gpt-4o-mini)
        AZURE_OPENAI_EMBEDDING_DEPLOYMENT - Deployment name for embedding model (default: text-embedding-3-small)
"""

import os

from openai import AzureOpenAI, OpenAI


def is_azure() -> bool:
    """Check if Azure OpenAI should be used."""
    return os.environ.get("USE_AZURE_OPENAI", "").lower() in ("true", "1", "yes")


def get_client() -> OpenAI | AzureOpenAI:
    """Create and return the appropriate OpenAI client."""
    if is_azure():
        return AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        )
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_model() -> str:
    """Return the chat model name or Azure deployment name."""
    if is_azure():
        return os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    return "gpt-4o-mini"


def get_embedding_model() -> str:
    """Return the embedding model name or Azure deployment name."""
    if is_azure():
        return os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
    return "text-embedding-3-small"
