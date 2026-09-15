import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question, results):

    context_parts = []

    for result in results:
        chunk = result["chunk"]

        context_parts.append(
            f"""
FILE: {chunk["file"]}
FUNCTION: {chunk["qualified_name"]}
LINES: {chunk["start_line"]}-{chunk["end_line"]}

CODE:
{chunk["code"]}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a senior software engineer helping a developer understand a codebase.

Answer the user's question using ONLY the code context provided below.

Important instructions:
- Be concise but useful.
- Mention the exact file path.
- Mention the function or method name.
- Mention relevant line numbers.
- Explain what the code is doing.
- Do not invent information that is not in the provided code.
- If the context does not contain enough information, say so.

USER QUESTION:
{question}

CODE CONTEXT:
{context}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text