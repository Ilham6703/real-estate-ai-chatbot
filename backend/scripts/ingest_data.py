


"""
Knowledge Base Ingestion Script

This script:

1. Reads PDFs
2. Crawls the website
3. Cleans website text
4. Splits documents
5. Generates Gemini embeddings
6. Uploads vectors into Qdrant

Run manually whenever website or PDFs change.
"""
from uuid import uuid4
import logging
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from backend.app.config import settings

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# =====================================================
# Configuration
# =====================================================

BASE_URL = "https://1beegha.com"

PDF_DIRECTORY = Path("backend/knowledge/pdfs")

CHUNK_SIZE = 1400
CHUNK_OVERLAP = 250

MAX_PAGES = 250

REQUEST_TIMEOUT = 20

REQUEST_DELAY = 0.20

visited_urls: set[str] = set()

# =====================================================
# Embeddings
# =====================================================

embeddings = OpenAIEmbeddings(
    model=settings.OPENAI_EMBEDDING_MODEL,
    api_key=settings.OPENAI_API_KEY,
)

# =====================================================
# Qdrant
# =====================================================

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    timeout=600,
)

# =====================================================
# Utilities
# =====================================================

def clean_text(text: str) -> str:
    """
    Remove excessive whitespace.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_url(url: str) -> str:
    """
    Normalize URLs.
    """

    url = url.split("#")[0]

    return url.rstrip("/")


def should_visit(url: str) -> bool:
    """
    Decide whether a page should be crawled.
    """

    parsed = urlparse(url)

    if not parsed.netloc.endswith("1beegha.com"):
        return False

    blocked = [

        "/wp-admin",
        "/wp-login",
        "/feed",
        "/privacy",
        "/terms",
        "/author/",
        "/tag/",
        "/search",
        "/cart",
        "/checkout",
        "/my-account",
        "/cdn-cgi",

        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".svg",
        ".webp",
        ".ico",
        ".zip",
        ".xml",

    ]

    lower = url.lower()

    return not any(item in lower for item in blocked)

# =====================================================
# PDFs
# =====================================================

def load_pdf_documents():

    logger.info("Loading PDFs...")

    documents = []

    if not PDF_DIRECTORY.exists():

        logger.warning("PDF directory not found.")

        return documents

    pdfs = sorted(PDF_DIRECTORY.glob("*.pdf"))

    for pdf in pdfs:

        try:

            loader = PyPDFLoader(str(pdf))

            docs = loader.load()

            for doc in docs:

                doc.metadata.update({

                    "type": "pdf",

                    "source": pdf.name,

                })

            documents.extend(docs)

            logger.info(f"Loaded {pdf.name}")

        except Exception as e:

            logger.error(f"{pdf.name}: {e}")

    logger.info(f"PDF pages: {len(documents)}")

    return documents

# =====================================================
# Website
# =====================================================

def crawl_page(url: str):

    url = normalize_url(url)

    if len(visited_urls) >= MAX_PAGES:
        return []

    if url in visited_urls:
        return []

    if not should_visit(url):
        return []

    visited_urls.add(url)

    logger.info(f"Crawling {url}")

    try:

        response = requests.get(

            url,

            timeout=REQUEST_TIMEOUT,

            headers={

                "User-Agent":
                "1Beegha-RAG-Bot/1.0"

            }

        )

        response.raise_for_status()

    except Exception:

        return []

    soup = BeautifulSoup(

        response.text,

        "html.parser",

    )

    for tag in soup([

        "script",

        "style",

        "noscript",

        "svg",

    ]):

        tag.decompose()

    text = clean_text(

        soup.get_text(separator=" ")

    )

    if len(text) < 100:

        return []

    documents = [

        Document(

            page_content=text,

            metadata={

                "source": url,

                "title": soup.title.string.strip()
                if soup.title
                else "",

                "type": "website",

            },

        )

    ]

    links = set()

    for anchor in soup.find_all(

        "a",

        href=True,

    ):

        href = normalize_url(

            urljoin(

                url,

                anchor["href"]

            )

        )

        if should_visit(href):

            links.add(href)

    time.sleep(REQUEST_DELAY)

    for link in sorted(links):

        documents.extend(

            crawl_page(link)

        )

    return documents


def load_website_documents():

    logger.info("Starting website crawl...")

    visited_urls.clear()

    docs = crawl_page(BASE_URL)

    logger.info(f"Website pages: {len(docs)}")

    return docs

# =====================================================
# Split Documents
# =====================================================

def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split documents into chunks suitable for retrieval.
    """

    logger.info("Splitting documents...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            "; ",
            ", ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    logger.info(f"Generated {len(chunks)} chunks.")

    return chunks


# =====================================================
# Embedding Dimension
# =====================================================

def get_embedding_dimension() -> int:
    """
    Determine embedding dimension automatically.

    This avoids hardcoding values such as 3072.
    """

    logger.info("Determining embedding dimension...")

    vector = embeddings.embed_query("Embedding dimension check")

    dimension = len(vector)

    logger.info(f"Embedding dimension: {dimension}")

    return dimension


# =====================================================
# Collection
# =====================================================

def collection_exists() -> bool:
    """
    Check whether the collection already exists.
    """

    collections = client.get_collections().collections

    return any(
        c.name == settings.QDRANT_COLLECTION
        for c in collections
    )


def recreate_collection():
    """
    Delete and recreate the collection.

    Since ingestion is an offline admin task,
    we always rebuild the knowledge base from scratch.
    """

    if collection_exists():

        logger.info("Deleting old collection...")

        client.delete_collection(
            settings.QDRANT_COLLECTION
        )

        logger.info("Old collection deleted.")

    dimension = get_embedding_dimension()

    logger.info("Creating collection...")

    client.create_collection(

        collection_name=settings.QDRANT_COLLECTION,

        vectors_config=VectorParams(

            size=dimension,

            distance=Distance.COSINE,

        ),

    )

    logger.info("Collection created successfully.")


# =====================================================
# Embedding Generation
# =====================================================

def generate_embeddings(chunks: list[Document]):
    """
    Generate embeddings for all chunks.

    Returns:
        list[(Document, embedding)]
    """

    logger.info("Generating embeddings...")

    total = len(chunks)

    results = []

    BATCH_SIZE = 50

    for start in range(0, total, BATCH_SIZE):

        end = min(start + BATCH_SIZE, total)

        logger.info(
            f"Embedding {start + 1}-{end} / {total}"
        )

        texts = [

            chunk.page_content

            for chunk in chunks[start:end]

        ]

        vectors = embeddings.embed_documents(texts)

        for doc, vector in zip(

            chunks[start:end],

            vectors,

        ):

            results.append(

                (

                    doc,

                    vector,

                )

            )

    logger.info("Embeddings generated.")

    return results

# =====================================================
# Upload to Qdrant
# =====================================================

def upload_embeddings(embedded_documents):
    """
    Upload embeddings to Qdrant in batches.
    """

    logger.info("Uploading vectors to Qdrant...")

    BATCH_SIZE = 100

    total = len(embedded_documents)

    for start in range(0, total, BATCH_SIZE):

        end = min(start + BATCH_SIZE, total)

        logger.info(
            f"Uploading {start + 1}-{end} / {total}"
        )

        points = []

        for document, vector in embedded_documents[start:end]:

            points.append(

                PointStruct(

                    id=str(uuid4()),

                    vector=vector,

                    payload={

                        "page_content": document.page_content,

                        **document.metadata,

                    },

                )

            )

        for attempt in range(3):

            try:

                client.upsert(

                    collection_name=settings.QDRANT_COLLECTION,

                    wait=True,

                    points=points,

                )

                break

            except Exception as e:

                logger.warning(

                    f"Retry {attempt + 1}/3 : {e}"

                )

                time.sleep(2)

        else:

            raise RuntimeError(

                "Failed to upload vectors."

            )

    logger.info("Upload completed successfully.")


# =====================================================
# Main
# =====================================================

def main():

    start_time = time.time()

    logger.info("=" * 60)
    logger.info("Starting Knowledge Base Ingestion")
    logger.info("=" * 60)

    # -----------------------------------------
    # Load Documents
    # -----------------------------------------

    pdf_documents = load_pdf_documents()

    website_documents = load_website_documents()

    documents = pdf_documents + website_documents

    logger.info(
        f"Total documents: {len(documents)}"
    )

    if not documents:

        logger.error("No documents found.")

        return

    # -----------------------------------------
    # Split
    # -----------------------------------------

    chunks = split_documents(documents)

    # -----------------------------------------
    # Collection
    # -----------------------------------------

    recreate_collection()

    # -----------------------------------------
    # Embeddings
    # -----------------------------------------

    embedded_documents = generate_embeddings(chunks)

    # -----------------------------------------
    # Upload
    # -----------------------------------------

    upload_embeddings(embedded_documents)

    elapsed = round(

        time.time() - start_time,

        2,

    )

    logger.info("=" * 60)
    logger.info("Knowledge Base Created Successfully")
    logger.info(f"Time Taken : {elapsed} seconds")
    logger.info(f"Pages Crawled : {len(visited_urls)}")
    logger.info(f"Chunks : {len(chunks)}")
    logger.info("=" * 60)


if __name__ == "__main__":

    main()