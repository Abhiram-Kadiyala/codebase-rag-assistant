import shutil

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from repo_parser import clone_repository, read_code_files
from code_chunker import (
    extract_python_chunks,
    extract_generic_chunks
)
from rag_service import store_chunks, search_code
from llm_service import generate_answer


app = FastAPI(
    title="Codebase RAG Assistant API",
    description="Analyze GitHub repositories and ask questions about their code.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Stores information about the currently analyzed repository
current_repository = {
    "url": None,
    "files": [],
    "chunks": [],
    "languages": {}
}


class RepositoryRequest(BaseModel):
    repo_url: str


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Codebase RAG Assistant API is running",
        "repository_loaded": current_repository["url"] is not None
    }


@app.post("/analyze")
def analyze_repository(request: RepositoryRequest):

    repo_path = None

    try:
        print(f"Cloning repository: {request.repo_url}")

        repo_path = clone_repository(
            request.repo_url
        )

        print("Reading source files...")

        files = read_code_files(
            repo_path
        )

        if len(files) == 0:
            raise HTTPException(
                status_code=400,
                detail="No supported source code files were found."
            )

        chunks = []
        languages = {}

        for file in files:

            extension = file["extension"]

            languages[extension] = (
                languages.get(extension, 0) + 1
            )

            # Python gets function/method-aware parsing
            if extension == ".py":

                file_chunks = extract_python_chunks(
                    file["path"],
                    file["content"]
                )

            # Other supported languages use generic overlapping chunks
            else:

                file_chunks = extract_generic_chunks(
                    file["path"],
                    file["content"]
                )

            chunks.extend(file_chunks)

        if len(chunks) == 0:
            raise HTTPException(
                status_code=400,
                detail="No code chunks could be extracted."
            )

        print(
            f"Found {len(files)} files "
            f"and {len(chunks)} code chunks."
        )

        print("Preparing repository for search...")

        store_chunks(chunks)

        print("Repository ready.")

        current_repository["url"] = request.repo_url
        current_repository["files"] = files
        current_repository["chunks"] = chunks
        current_repository["languages"] = languages

        return {
            "success": True,
            "repository": request.repo_url,
            "total_files": len(files),
            "total_chunks": len(chunks),
            "languages": languages,
            "message": "Repository analyzed and indexed successfully."
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Analyze error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if repo_path:
            shutil.rmtree(
                repo_path,
                ignore_errors=True
            )


@app.post("/ask")
def ask_question(request: QuestionRequest):

    if current_repository["url"] is None:
        raise HTTPException(
            status_code=400,
            detail="Please analyze a repository first."
        )

    try:
        print(f"Question: {request.question}")

        results = search_code(
            request.question,
            top_k=5
        )

        if len(results) == 0:
            raise HTTPException(
                status_code=404,
                detail="No relevant code was found."
            )

        answer = generate_answer(
            request.question,
            results
        )

        sources = []

        for result in results:

            chunk = result["chunk"]

            sources.append({
                "file": chunk["file"],
                "name": chunk["qualified_name"],
                "type": chunk["type"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "similarity": round(
                    result["score"],
                    4
                ),
                "code": chunk["code"]
            })

        return {
            "success": True,
            "repository": current_repository["url"],
            "question": request.question,
            "answer": answer,
            "sources": sources
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Ask error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/repository")
def repository_info():

    if current_repository["url"] is None:
        return {
            "loaded": False
        }

    return {
        "loaded": True,
        "repository": current_repository["url"],
        "total_files": len(
            current_repository["files"]
        ),
        "total_chunks": len(
            current_repository["chunks"]
        ),
        "languages": current_repository["languages"]
    }