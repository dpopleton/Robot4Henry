import uuid
import chromadb
from config.settings import CHROMA_PATH, LONG_TERM_RETRIEVE_COUNT


class LongTermMemory:
    def __init__(self, chroma_path: str = CHROMA_PATH, embedding_function=None):
        """``embedding_function`` defaults to ChromaDB's own model; tests
        pass a cheap fake so they run fast and offline."""
        self.client = chromadb.PersistentClient(path=chroma_path)
        kwargs = {"embedding_function": embedding_function} if embedding_function else {}
        self.collection = self.client.get_or_create_collection(
            name="memories", **kwargs
        )

    @staticmethod
    def _safe_metadata(metadata: dict | None) -> dict:
        # ChromaDB only takes str/int/float/bool values
        return {
            k: str(v) if v is not None else ""
            for k, v in (metadata or {}).items()
        }

    def store(self, text: str, metadata: dict | None = None):
        self.collection.add(
            documents=[text],
            metadatas=[self._safe_metadata(metadata)],
            ids=[str(uuid.uuid4())]
        )

    def replace_session(self, session_id: str, texts: list, metadata: dict | None = None):
        """Make ``texts`` the only memories from ``session_id``.

        Whatever the session stored before is deleted first, so re-resting a
        session (after a crash part-way through rest, R-108) replaces its
        memories rather than adding a second set. Deleting matters as well
        as the stable ids: the model can word a re-run differently, or
        list fewer memories. Ids are ``<session_id>-<n>``.
        """
        self.collection.delete(where={"session_id": session_id})
        if not texts:
            return
        meta = self._safe_metadata({**(metadata or {}), "session_id": session_id})
        self.collection.add(
            documents=list(texts),
            metadatas=[dict(meta) for _ in texts],
            ids=[f"{session_id}-{i}" for i in range(len(texts))],
        )

    def retrieve(self, query: str, n_results: int = LONG_TERM_RETRIEVE_COUNT) -> list:
        # Return empty if nothing stored yet
        if self.collection.count() == 0:
            return []
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count())
        )
        docs = results.get("documents", [])
        return docs[0] if docs else []

    def count(self) -> int:
        return self.collection.count()
