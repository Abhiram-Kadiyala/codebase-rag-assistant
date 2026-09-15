import os

from dotenv import load_dotenv
from google import genai
from google.genai import types



load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def create_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    return response.embeddings[0].values




def create_embeddings(texts: list[str]):
    contents = [
        types.Content(
            parts=[
                types.Part.from_text(text=text)
            ]
        )
        for text in texts
    ]

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=contents,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]