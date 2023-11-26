# cache_handler.py
from typing import Any, Dict, List, Optional

class CacheHandler:
    def __init__(self):
        self.collections: Dict[str, Dict[str, Any]] = {}  # Mocked Firebase Store

    # Mocked Firestore operations
    def add_document(
        self, collection_name: str, document_id: str, data: Dict[str, Any]
    ) -> None:
        if collection_name not in self.collections:
            self.collections[collection_name] = {}
        self.collections[collection_name][document_id] = data

    def get_document(
        self, collection_name: str, document_id: str
    ) -> Optional[Dict[str, Any]]:
        return self.collections.get(collection_name, {}).get(document_id)

    def update_document(
        self, collection_name: str, document_id: str, data: Dict[str, Any]
    ) -> None:
        if (
            collection_name in self.collections
            and document_id in self.collections[collection_name]
        ):
            self.collections[collection_name][document_id].update(data)

    def delete_document(self, collection_name: str, document_id: str) -> None:
        if (
            collection_name in self.collections
            and document_id in self.collections[collection_name]
        ):
            del self.collections[collection_name][document_id]

    def list_collection(self, collection_name: str) -> List[Dict[str, Any]]:
        return list(self.collections.get(collection_name, {}).values())

    def query_collection(
        self, collection_name: str, query_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        # This is a simplistic query implementation that assumes all values are exact matches and uses equality check.
        # You can expand this to handle different types of queries (e.g., range checks, inequality, etc.).
        all_docs = self.list_collection(
            collection_name
        )  # Assuming this returns all documents in the collection
        if not query_params:
            return all_docs

        filtered_docs = [
            doc
            for doc in all_docs
            if all(doc.get(key) == value for key, value in query_params.items())
        ]
        return filtered_docs


    def clear_all_data(self) -> None:
        access_tokens_data = None
        # Clear all collections.
        self.collections.clear()

        # Clear all event logs.
        self.clear_all_event_logs()



# Create an instance of CacheHandler for use in tests
cache_handler = CacheHandler()
