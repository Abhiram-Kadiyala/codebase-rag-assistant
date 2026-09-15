from embedding_service import create_embedding

text = """
def login(username, password):
    if username == "admin":
        return generate_token()
"""

embedding = create_embedding(text)

print("Embedding created successfully!")
print("Vector length:", len(embedding))
print("First 10 values:")
print(embedding[:10])