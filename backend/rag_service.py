import re

from embedding_service import (
    create_embedding,
    create_embeddings
)

from vector_store import VectorStore


vector_store = VectorStore()

all_chunks = []


def prepare_chunk_text(chunk):
    return f"""
File: {chunk["file"]}
Type: {chunk["type"]}
Name: {chunk["qualified_name"]}

Code:
{chunk["code"]}
"""


def store_chunks(chunks):
    """
    Store parsed chunks without embedding the whole repository.
    """
    global all_chunks

    all_chunks = chunks

    print(
        f"Stored {len(all_chunks)} chunks "
        "for hybrid retrieval."
    )


def tokenize(text):
    return set(
        re.findall(
            r"[a-zA-Z_][a-zA-Z0-9_]+",
            text.lower()
        )
    )


def lexical_search(question, top_k=25):
    """
    Cheap first-stage search.
    """

    query_words = tokenize(question)

    scored_chunks = []

    for chunk in all_chunks:

        searchable_text = (
            chunk["file"]
            + " "
            + chunk["qualified_name"]
            + " "
            + chunk["code"]
        )

        chunk_words = tokenize(searchable_text)

        overlap = len(
            query_words.intersection(chunk_words)
        )

        # Give function/file names slightly more importance
        name_words = tokenize(
            chunk["qualified_name"]
            + " "
            + chunk["file"]
        )

        name_overlap = len(
            query_words.intersection(name_words)
        )

        score = overlap + (name_overlap * 3)

        scored_chunks.append(
            {
                "score": score,
                "chunk": chunk
            }
        )

    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return [
        item["chunk"]
        for item in scored_chunks[:top_k]
    ]


def search_code(question, top_k=5):

    if not all_chunks:
        return []

    # Stage 1: cheap shortlist
    candidates = lexical_search(
        question,
        top_k=25
    )

    texts = [
        prepare_chunk_text(chunk)
        for chunk in candidates
    ]

    # Stage 2: semantic embeddings
    embeddings = create_embeddings(texts)

    query_embedding = create_embedding(
        question
    )

    vector_store.items = []

    for chunk, embedding in zip(
        candidates,
        embeddings
    ):
        vector_store.add(
            chunk,
            embedding
        )

    return vector_store.search(
        query_embedding,
        top_k
    )