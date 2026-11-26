"""A cheap, deterministic embedding so tests can use a real ChromaDB without
downloading or running its embedding model."""
import hashlib

from chromadb import Documents, EmbeddingFunction, Embeddings


class FakeEmbedding(EmbeddingFunction):
    """Bag of hashed words: texts sharing words land near each other, which
    is enough for retrieve() to return something sensible."""
    DIMENSIONS = 32

    def __init__(self):
        pass

    def __call__(self, input: Documents) -> Embeddings:
        vectors = []
        for text in input:
            v = [0.0] * self.DIMENSIONS
            for word in text.lower().split():
                h = int(hashlib.md5(word.encode()).hexdigest(), 16)
                v[h % self.DIMENSIONS] += 1.0
            v[0] += 0.001  # never all zeros
            vectors.append(v)
        return vectors

    @staticmethod
    def name() -> str:
        return "qbot-test-fake"

    def get_config(self) -> dict:
        return {}

    @staticmethod
    def build_from_config(config: dict) -> "FakeEmbedding":
        return FakeEmbedding()
