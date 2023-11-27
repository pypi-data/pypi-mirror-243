import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
# Use the application default credentials
from aipkgs_core import Singleton
from typing import Optional

env_keys_exist = False
try:
    json_credentials_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    env_keys_exist = True
except Exception:
    raise Exception("add GOOGLE_APPLICATION_CREDENTIALS to env")


@Singleton
class FirebaseSession:
    def __init__(self):
        self.__json_credentials_path = None
        self.__firebase_app: Optional[firebase_admin.App] = None
        self.__db: Optional[firebase_admin.firestore.firestore.Client] = None

    @property
    def firebase_app(self) -> Optional[firebase_admin.App]:
        return self.__firebase_app

    @property
    def firebase_db(self) -> Optional[firebase_admin.firestore.firestore.Client]:
        return self.__db

    # region client
    def __initialize_firebase(self, json_credentials_path: str):
        if (self.__firebase_app is not None) \
                and (self.__json_credentials_path == json_credentials_path):
            return

        self.__json_credentials_path = json_credentials_path
        cred = credentials.Certificate(self.__json_credentials_path)
        self.__firebase_app = firebase_admin.initialize_app(cred, {'storageBucket': 'instant-9101b.appspot.com'})
        self.__db = firestore.client()

    def initialize_firebase(self, json_credentials_path: str):
        self.__initialize_firebase(json_credentials_path=json_credentials_path)

    # endregion


def initialize_firebase() -> firebase_admin.App:
    if env_keys_exist:
        FirebaseSession.shared.initialize_firebase(json_credentials_path=json_credentials_path)
    return FirebaseSession.shared.firebase_app


def firebase_db() -> firebase_admin.firestore.firestore.Client:
    if FirebaseSession.shared.firebase_db:
        return FirebaseSession.shared.firebase_db


def stamp(dictionary):
    data = dictionary

    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
    data["timestamp"] = timestamp

    current_time = time.time()
    doc_ref = db.collection(u'fblr-scrpt').document(u'executions').collection(u'records').document(u'{}'.format(current_time))
    doc_ref.set(data, merge=True)
