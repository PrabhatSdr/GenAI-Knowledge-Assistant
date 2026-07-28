import os

from config.settings import settings
from core.database import vector_store
from services.metadata_service import MetadataService


class DocumentService:

    def __init__(self):

        self.upload_folder = settings.UPLOAD_FOLDER
        self.metadata = MetadataService()

    def list_documents(self, chat_id=None):

        return self.metadata.list_documents(chat_id=chat_id)

    def get_document_count(self, chat_id=None):

        return self.metadata.document_count(chat_id=chat_id)

    def get_document(self, filename):

        return self.metadata.get_document(filename)

    def delete_document(self, filename):

        file_path = os.path.join(
            self.upload_folder,
            filename
        )

        if not os.path.exists(file_path):
            return False

        os.remove(file_path)

        vector_store.delete_document(filename)

        self.metadata.delete_document(filename)

        return True