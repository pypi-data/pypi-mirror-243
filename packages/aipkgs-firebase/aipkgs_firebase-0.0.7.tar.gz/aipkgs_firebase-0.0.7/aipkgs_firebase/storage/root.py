from typing import Dict, List

from aipkgs_firebase.storage import core, helpers


class Root:

    collection_name = ""

    def __init__(self, collection_name: str = None) -> None:
        self.collection_name = collection_name

    def exists(self, document_id: str) -> bool:
        return core.document_exists(
            collection_name=self.collection_name, document_id=document_id
        )

    def get_document(self, document_id: str) -> dict:
        return helpers.get_document(
            collection_name=self.collection_name, document_id=document_id
        )

    def get_document_realtime(self, document_id: str, callback):
        def temp_callback(document):
            callback(document)
        return helpers.get_document_realtime(
            collection_name=self.collection_name, document_id=document_id, callback=temp_callback
        )

    def get_document_changes_realtime(self, document_id: str, callback):
        def temp_callback(document, changes, read_time):
            callback(document, changes, read_time)

        return helpers.get_document_changes_realtime(
            collection_name=self.collection_name, document_id=document_id, callback=temp_callback
        )

    def get_documents_changes_realtime(self, document_id: str, callback):
        def temp_callback(doc_snapshot, changes, read_time):
            callback(doc_snapshot, changes, read_time)

        return helpers.get_documents_changes_realtime(
            collection_name=self.collection_name, document_id=document_id, callback=temp_callback
        )

    def get_documents(self, filters: Dict[str, any] = None) -> List[dict]:
        return helpers.get_documents(
            collection_name=self.collection_name, filters=filters
        )

    def create(self, dictionary: dict, document_id: str = None) -> bool:
        return core.create_document_from_data(
            dictionary_data=dictionary,
            collection_name=self.collection_name,
            document_id=document_id,
        )

    def update(self, dictionary: dict, document_id: str):
        core.update_document_with_data(
            dictionary_data=dictionary,
            collection_name=self.collection_name,
            document_id=document_id,
        )

    def remove(self, document_id: str):
        core.remove_document(
            collection_name=self.collection_name, document_id=document_id
        )

    def remove_all(self):
        core.remove_documents(
            collection_name=self.collection_name)
