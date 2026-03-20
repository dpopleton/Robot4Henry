import chromadb
from config.settings import CHROMA_PATH, LONG_TERM_RETRIEVE_COUNT


class LongTermMemory:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(
            name="memories"
        )

    def store(self, text: str, metadata: dict = {}):
        import uuid
        # Ensure all metadata values are ChromaDB-safe types
        safe_metadata = {
            k: str(v) if v is not None else ""
            for k, v in metadata.items()
        }
        self.collection.add(
            documents=[text],
            metadatas=[safe_metadata],
            ids=[str(uuid.uuid4())]
        )

    def retrieve(self, query: str, n_results: int = LONG_TERM_RETRIEVE_COUNT) -> list:
        # Return empty if nothing stored yet
        if self.collection.count() == 0:
            return []
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count())
        )
        return results["documents"][0]

    def count(self) -> int:
        return self.collection.count()