"""
Retrieval-Augmented Generation (RAG) pipeline.
"""

import logging

from qdrant_client import QdrantClient

from langchain_openai import (
    ChatOpenAI,
    OpenAIEmbeddings,
)

from langchain_qdrant import QdrantVectorStore
from backend.app.prompts import SYSTEM_PROMPT
from backend.app.config import settings

# =====================================================
# Logging
# =====================================================

logger = logging.getLogger(__name__)

# =====================================================
# Embeddings
# =====================================================

_embeddings = OpenAIEmbeddings(
    model=settings.OPENAI_EMBEDDING_MODEL,
    api_key=settings.OPENAI_API_KEY,
)

# =====================================================
# LLM
# =====================================================

_llm = ChatOpenAI(
    model=settings.OPENAI_CHAT_MODEL,
    api_key=settings.OPENAI_API_KEY,
    temperature=0.2,
)

# =====================================================
# Qdrant Client
# =====================================================

_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

# =====================================================
# Validate Collection
# =====================================================

try:

    _client.get_collection(
        settings.QDRANT_COLLECTION
    )

    logger.info(
        "Connected to Qdrant collection."
    )

except Exception as e:

    logger.exception(
        "Unable to connect to Qdrant."
    )

    raise RuntimeError(
        f"Qdrant collection not available.\n{e}"
    )

# =====================================================
# Vector Store
# =====================================================

_vector_store = QdrantVectorStore(

    client=_client,

    collection_name=settings.QDRANT_COLLECTION,

    embedding=_embeddings,

)

# =====================================================
# Retriever
# =====================================================

_retriever = _vector_store.as_retriever(

    search_kwargs={

        "k": 5,

    }

)

# =====================================================
# Public Getters
# =====================================================

def get_llm():
    """
    Return singleton LLM.
    """

    return _llm


def get_embeddings():
    """
    Return singleton embeddings.
    """

    return _embeddings


def get_vector_store():
    """
    Return singleton vector store.
    """

    return _vector_store


def get_retriever():
    """
    Return singleton retriever.
    """

    return _retriever

# =====================================================
# Retrieve Context
# =====================================================

def retrieve_context(question: str):
    """
    Retrieve relevant documents from Qdrant.
    """

    logger.info("Searching knowledge base...")

    documents = _retriever.invoke(question)

    logger.info(
        "Retrieved %s document(s).",
        len(documents),
    )

    return documents


# =====================================================
# Build Context
# =====================================================

def build_context(documents) -> str:
    """
    Convert retrieved documents into a single context string.
    """

    if not documents:
        return ""

    context_parts = []

    for document in documents:

        context_parts.append(

            document.page_content.strip()

        )

    return "\n\n".join(context_parts)


# =====================================================
# Generate Response
# =====================================================

def generate_response(
    question: str,
    documents,
    history,
):
    """
    Generate the final response.
    """

    context = build_context(documents)

    if not context:

        return (
            "I couldn't find that information. "
            "Please contact our sales team."
        )

    logger.info("Generating response...")

    
    messages = [

    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }

    ]

# Add previous conversation
    messages.extend(history)

# Add current user message with retrieved context
    messages.append(

    {
        "role": "user",
        "content": f"""
    Context:

    {context}

    Current User Question:

    {question}

    Answer ONLY using the provided context and previous conversation if relevant.
    """,
    }

    )
    


    try:

        response = _llm.invoke(messages)

        logger.info("Response generated.")

        return response.content.strip()

    except Exception:

        logger.exception(
            "LLM generation failed."
        )

        return (
            "I'm sorry, I couldn't generate a response "
            "at the moment. Please try again."
        )