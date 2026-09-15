# Codebase RAG Assistant

An AI-powered developer onboarding tool that helps users understand unfamiliar codebases using Retrieval-Augmented Generation (RAG).

Users can paste a public GitHub repository URL, analyze the repository, and ask natural-language questions such as:

- Where is authentication handled?
- How is SSL verification implemented?
- Where are API requests made?
- How is error handling structured?

The system retrieves the most relevant code snippets and generates grounded answers with file names, function names, line numbers, and source code references.

---

## Live Demo

Frontend:

https://codebase-rag-assistant-s7lm.vercel.app

Backend API:

https://codebase-rag-assistant-lrgh.onrender.com

Swagger API Docs:

https://codebase-rag-assistant-lrgh.onrender.com/docs

---

## Problem Statement

Onboarding new developers into a large, undocumented codebase often takes significant engineering time.

Developers may spend hours manually searching through files, functions, classes, and routes just to understand where important logic is implemented.

The Codebase RAG Assistant solves this by allowing developers to ask natural-language questions directly about a GitHub repository.

Instead of manually searching the entire codebase, the system retrieves the most relevant source code and uses an LLM to generate a grounded explanation.

---

## Features

- Analyze public GitHub repositories
- Natural-language questions about source code
- Python function and method-level parsing
- Generic chunking for multiple programming languages
- Hybrid lexical + semantic retrieval
- Gemini embeddings
- Vector similarity search
- AI-generated code explanations
- Exact file references
- Function and method names
- Line number references
- Retrieved source-code snippets
- Similarity scores
- Responsive developer-focused web interface
- Publicly deployed frontend and backend

---

## Supported Languages

The repository scanner currently supports:

- Python
- JavaScript
- JSX
- TypeScript
- TSX
- Java
- C
- C++
- C#
- Go
- PHP
- Ruby

Python files receive structure-aware parsing using Python AST.

Other supported languages currently use overlapping source-code chunks.

---

## Architecture

```text
Public GitHub Repository
          ↓
     Shallow Git Clone
          ↓
    Source File Scanner
          ↓
      Code Chunking
          ↓
 ┌─────────────────────┐
 │ Python AST Parsing  │
 │ Generic Chunking    │
 └─────────────────────┘
          ↓
   Store Code Chunks
          ↓
      User Question
          ↓
  Lexical Shortlisting
          ↓
 Gemini Code Embeddings
          ↓
 Cosine Similarity Search
          ↓
 Top Relevant Code Chunks
          ↓
       Gemini LLM
          ↓
 Answer + File References
 + Functions + Line Numbers
 + Source Code