from repo_parser import clone_repository, read_code_files
from code_chunker import extract_python_chunks
from rag_service import index_chunks, search_code
from llm_service import generate_answer

import shutil


repo_url = "https://github.com/psf/requests.git"

repo_path = None

try:
    repo_path = clone_repository(repo_url)

    files = read_code_files(repo_path)

    chunks = []

    for file in files:
        if file["extension"] == ".py":
            file_chunks = extract_python_chunks(
                file["path"],
                file["content"]
            )

            chunks.extend(file_chunks)

    # Only index the first 40 chunks for testing
    test_chunks = chunks[:40]

    print("Indexing chunks:", len(test_chunks))

    index_chunks(test_chunks)

    question = "Where is SSL certificate verification handled?"

    results = search_code(
        question,
        top_k=5
    )

    print("\nQUESTION:")
    print(question)

    print("\nTOP RESULTS:\n")

    for i, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print(
            f"{i}. {chunk['file']} "
            f"-> {chunk['qualified_name']}"
        )

        print(
            "Similarity:",
            round(result["score"], 4)
        )

        print(
            f"Lines: "
            f"{chunk['start_line']}-"
            f"{chunk['end_line']}"
        )

        print("-" * 60)

    # Generate final answer using retrieved code
    answer = generate_answer(
        question,
        results
    )

    print("\nAI ANSWER:\n")
    print(answer)

finally:
    if repo_path:
        shutil.rmtree(
            repo_path,
            ignore_errors=True
        )