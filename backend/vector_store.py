import math


class VectorStore:

    def __init__(self):
        self.items = []


    def add(self, chunk, embedding):
        self.items.append({
            "chunk": chunk,
            "embedding": embedding
        })


    def cosine_similarity(self, vector_a, vector_b):

        dot_product = sum(
            a * b
            for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = math.sqrt(
            sum(a * a for a in vector_a)
        )

        magnitude_b = math.sqrt(
            sum(b * b for b in vector_b)
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0

        return dot_product / (
            magnitude_a * magnitude_b
        )


    def search(self, query_embedding, top_k=5):

        results = []

        for item in self.items:

            score = self.cosine_similarity(
                query_embedding,
                item["embedding"]
            )

            results.append({
                "score": score,
                "chunk": item["chunk"]
            })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:top_k]