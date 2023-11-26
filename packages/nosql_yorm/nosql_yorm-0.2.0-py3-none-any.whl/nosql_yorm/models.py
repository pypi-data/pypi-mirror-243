from __future__ import annotations
import random
import string

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from datetime import datetime
from firebase_admin import firestore
from pydantic import BaseModel, Field
from nosql_yorm.cache import cache_handler
from nosql_yorm.config import get_config, initialize_firebase
import re
import inflect

# Define the regex pattern for a Firestore ID
FIRESTORE_ID_PATTERN = re.compile(r"^[a-z0-9]{20}$")


p = inflect.engine()

T = TypeVar("T", bound="BaseFirebaseModel")

# Initialize Firebase and Firestore client
initialize_firebase()
db = firestore.client()
# print the file location where this is being called from

class BaseFirebaseModel(BaseModel, Generic[T]):
    id: Optional[str] = Field(default_factory=lambda: None)
    __collection_name__: str = ""
    created_at: Optional[datetime] = Field(default_factory=lambda: None)
    updated_at: Optional[datetime] = Field(default_factory=lambda: None)

    @classmethod
    def _get_collection_name(cls):
        value =  cls.__collection_name__ or p.plural(cls.__name__)
        return value

    @classmethod
    def get_by_id(
        cls: Type[T], doc_id: str, read_write_to_cache: Optional[bool] = None
    ) -> Optional[T]:
        collection_name = cls._get_collection_name()
        if read_write_to_cache is None:
            read_write_to_cache = get_config().get("read_write_to_cache", False)

        if read_write_to_cache:
            doc_data = cache_handler.get_document(collection_name, doc_id)
            return cls(**doc_data) if doc_data else None
        else:
            doc_ref = db.collection(collection_name).document(doc_id)
            doc = doc_ref.get()
            data = doc.to_dict()
            # exclude id from data
            if data:
                data.pop("id", None)
            return cls(id=doc.id, **data) if doc.exists else None

    @classmethod
    def get_by_ids(
        cls: Type[T], doc_ids: List[str], read_write_to_cache: Optional[bool] = None
    ) -> List[T]:
        collection_name = cls._get_collection_name()
        documents = []
        if read_write_to_cache is None:
            read_write_to_cache = get_config().get("read_write_to_cache", False)

        if read_write_to_cache:
            # Fetch documents from the test cache
            for doc_id in doc_ids:
                doc_data = cache_handler.get_document(collection_name, doc_id)
                if doc_data:
                    documents.append(cls(**doc_data))
        else:
            # Fetch documents from Firestore
            docs_refs = [
                db.collection(collection_name).document(doc_id) for doc_id in doc_ids
            ]
            docs = db.get_all(docs_refs)
            for doc in docs:
                data = doc.to_dict()
                if data:
                    data.pop("id", None)  # Exclude the ID from the data if it's there
                    documents.append(cls(id=doc.id, **data))

        return documents

    @classmethod
    def get_page(
        cls: Type[T],
        page: int = 1,
        page_size: int = 10,
        query_params: Optional[Dict[str, Any]] = None,
        array_contains: Optional[Dict[str, Any]] = None,
        read_write_to_cache: Optional[bool] = None,
    ) -> List[T]:
        collection_name = cls._get_collection_name()
        start = (page - 1) * page_size
        end = start + page_size
        if read_write_to_cache is None:
            read_write_to_cache = get_config().get("read_write_to_cache", False)

        if read_write_to_cache:
            # Handle the test mode logic with query_params and array_contains filtering
            all_docs = cache_handler.query_collection(
                collection_name, query_params
            )
            if array_contains:
                all_docs = [
                    doc
                    for doc in all_docs
                    if all(
                        doc.get(key) and value in doc.get(key)
                        for key, value in array_contains.items()
                    )
                ]
            return [
                cls(**doc) for doc in all_docs[start:end]
            ]  # Paginate after filtering
        else:
            # The existing non-test mode logic to query Firebase
            query = db.collection(collection_name)
            if query_params:
                for key, value in query_params.items():
                    if isinstance(value, list):
                        query = query.where(key, "in", value)
                    else:
                        query = query.where(key, "==", value)
            if array_contains:
                for key, value in array_contains.items():
                    query = query.where(key, "array_contains", value)
            docs = query.offset(start).limit(page_size).stream()
            return [
                cls(
                    id=doc.id,
                    **(lambda d: {k: v for k, v in d.items() if k != "id"})(
                        doc.to_dict()
                    ),
                )
                for doc in docs
            ]

    @classmethod
    def get_all(cls: Type[T], read_write_to_cache: Optional[bool] = None) -> List[T]:
        collection_name = cls._get_collection_name()
        if read_write_to_cache is None:
            read_write_to_cache = get_config().get("read_write_to_cache", False)

        if read_write_to_cache:
            all_docs = cache_handler.list_collection(collection_name)
            return [cls(**doc) for doc in all_docs]
        else:
            docs = db.collection(collection_name).stream()

            return [
                cls(
                    id=doc.id,
                    **(lambda d: {k: v for k, v in d.items() if k != "id"})(
                        doc.to_dict()
                    ),
                )
                for doc in docs
            ]

    def save(
        self, generate_new_id: bool = False, read_write_to_cache: Optional[bool] = None
    ) -> None:
        collection_name = self._get_collection_name()
        if read_write_to_cache is None:
            read_write_to_cache = get_config().get("read_write_to_cache", False)

        if read_write_to_cache:
            document_id = (
                self.id or self.generate_fake_firebase_id()
            )  # Implement this method or provide a fake ID
            cache_handler.add_document(collection_name, document_id, self.dict())
            self.id = document_id
        else:
            collection_name = (
                self.__fields__["collection_name"].default
                if "collection_name" in self.__fields__
                and self.__fields__["collection_name"].default
                else p.plural(self.__class__.__name__)
            )

            # If the ID doesn't exist, doesn't match the Firebase pattern, or if we want to generate a new one
            if not self.id or generate_new_id:
                data_to_save = self.dict(exclude={"id", "created_at", "updated_at"})
                data_to_save["created_at"] = firestore.SERVER_TIMESTAMP
                data_to_save["updated_at"] = firestore.SERVER_TIMESTAMP

                # Add a new document to the Firestore collection
                _, new_doc_ref = db.collection(collection_name).add(data_to_save)
                # Set the ID from the new document reference
                self.id = new_doc_ref.id
            else:
                data_to_save = self.dict()
                data_to_save["updated_at"] = firestore.SERVER_TIMESTAMP

                # Get the document reference and update it with the new data
                doc_ref = db.collection(collection_name).document(self.id)
                doc_ref.set(data_to_save, merge=True)

    def delete(self, read_write_to_cache: Optional[bool] = None) -> None:
        collection_name = self._get_collection_name()
        if read_write_to_cache is None:
            read_write_to_cache = get_config().get("read_write_to_cache", False)

        if read_write_to_cache:
            cache_handler.delete_document(collection_name, self.id)
        else:
            doc_ref = db.collection(collection_name).document(self.id)
            doc_ref.delete()

    def merge(
        self,
        update_data: Dict[str, Any],
        overwrite_id: bool = False,
        exclude_props: List[str] = [],
        read_write_to_cache: Optional[bool] = None,
    ) -> None:
        if read_write_to_cache is None:
            read_write_to_cache = get_config().get("read_write_to_cache", False)

        # Update the instance properties
        for key, value in update_data.items():
            if key not in exclude_props:
                setattr(self, key, value)
                
        # Log the merge or update to the cache if in test mode
        if read_write_to_cache:
            collection_name = self._get_collection_name()
            cache_handler.update_document(collection_name, self.id, self.dict())
        else:
            # Default properties that shouldn't be overwritten
            default_exclude = (
                ["id", "created_at"] if not overwrite_id else ["created_at"]
            )

            # Combine default excludes with user provided excludes
            exclude_props.extend(default_exclude)

            # Update the instance properties
            for key, value in update_data.items():
                if key not in exclude_props:
                    setattr(self, key, value)

    @staticmethod
    def generate_fake_firebase_id() -> str:
        """Generate a random ID similar to Firestore's document IDs."""
        id_length = 20  # Typical Firestore ID length
        return "".join(
            random.choices(string.ascii_lowercase + string.digits, k=id_length)
        )
