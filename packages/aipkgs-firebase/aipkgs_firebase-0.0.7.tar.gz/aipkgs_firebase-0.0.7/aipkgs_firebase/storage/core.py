# Documentation
# https://firebase.google.com/docs/firestore

from datetime import datetime
import threading
from typing import Dict, List

import firebase_admin

from aipkgs_firebase import helpers


def collection_ref(
        collection_name: str,
) -> firebase_admin.firestore.firestore.CollectionReference:
    return helpers.firebase_db().collection("{}".format(collection_name))


def document_ref(
        collection_name: str, document_id: str
) -> firebase_admin.firestore.firestore.DocumentReference:
    doc_ref = collection_ref(collection_name=collection_name).document(
        document_id=document_id
    )
    return doc_ref


def document_exists(collection_name: str, document_id: str) -> bool:
    doc_ref = document_ref(
        collection_name=collection_name, document_id=document_id)
    doc = doc_ref.get()

    if doc.exists:
        return True

    return False


def get_document(
        collection_name: str, document_id: str
) -> firebase_admin.firestore.firestore.DocumentSnapshot:
    doc_ref = document_ref(
        collection_name=collection_name, document_id=document_id)
    doc = doc_ref.get()

    return doc


def get_document_realtime(
        collection_name: str, document_id: str, callback):
    doc_ref = document_ref(
        collection_name=collection_name, document_id=document_id)

    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        callback(doc_snapshot, changes, read_time)
        callback_done.set()

    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)

    return doc_watch


def get_documents(
        collection_name: str, filters: Dict[str, any] = None
) -> List[firebase_admin.firestore.firestore.DocumentSnapshot]:
    col_ref = collection_ref(collection_name=collection_name)
    if filters:
        for key, value in filters.items():
            col_ref = col_ref.where(f"{key}", "==", value)

    docs = col_ref.get()

    return docs


def create_document_from_data(
        dictionary_data: dict, collection_name: str, document_id: str = None
) -> bool:
    data = dictionary_data

    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %I:%M:%S %p")
    data["timestamp"] = firebase_admin.firestore.SERVER_TIMESTAMP
    data["created_at"] = timestamp

    # current_time = time.time()
    if document_id is not None:
        if not document_exists(
                collection_name=collection_name, document_id=document_id
        ):
            doc_ref = document_ref(
                collection_name=collection_name, document_id=document_id
            )
            doc_ref.set(data, merge=True)
            return True
    else:
        # doc_ref = collection_ref(collection_name=collection_name).add(data)  # document(_id or None u'{}'.format(current_time))
        doc_ref = collection_ref(
            collection_name=collection_name
        ).document()  # document(_id or None u'{}'.format(current_time))
        doc_ref.set(data, merge=False)
        return True

    return False


def update_document_with_data(
        dictionary_data: dict, collection_name: str, document_id: str
):
    data = dictionary_data

    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %I:%M:%S %p")
    data["updated_at"] = timestamp

    if document_id is not None:
        if document_exists(collection_name=collection_name, document_id=document_id):
            doc_ref = document_ref(
                collection_name=collection_name, document_id=document_id
            )
            doc_ref.update(field_updates=data)


def remove_document(collection_name: str, document_id: str):
    if document_id is not None:
        if document_exists(collection_name=collection_name, document_id=document_id):
            doc_ref = document_ref(
                collection_name=collection_name, document_id=document_id
            )
            doc_ref.delete()


def remove_documents(collection_name: str):
    documents = get_documents(collection_name=collection_name)
    for document in documents:
        remove_document(collection_name=collection_name,
                        document_id=document.id)
