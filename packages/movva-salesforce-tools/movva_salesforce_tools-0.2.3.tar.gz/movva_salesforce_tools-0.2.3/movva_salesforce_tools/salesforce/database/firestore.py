from google.cloud import firestore
from datetime import datetime


class MovvaFirestore:

    def __init__(self, collection_name) -> None:
        self.collection_name = collection_name
        self.client = None

        self.collection = None

    def create_client(self, google_project=None):
        if google_project:
            try:
                self.client = firestore.Client(google_project)
            except Exception as e:
                print(f'Impossible to connect to Firestore. Reason: {e}')

        self.client = firestore.Client()
        return self.client

    def fetch_collection(self):
        self.collection = self.client.collection(self.collection_name)
        return self.collection

    def store_message_tokenid_relation(
        self,
        mc_token_id: str,
        rapidpro_message_id: str
    ):
        document_reference = self.collection.document(mc_token_id)
        document_reference.set({
            'rapidpro_message_id': rapidpro_message_id,
            'mc_token_id': mc_token_id,
            'created_at': datetime.now()})

        print('Document has been stored successfully in Firestore!')
        return True

    def fetch_message_tokenid_relation(self, rapidpro_message_id: str):
        document = self.collection.document(rapidpro_message_id)
        document.get()
        if document.exists:
            data = document.to_dict()
            return data

        print('!!Document not found on firestore!!')
        return None
