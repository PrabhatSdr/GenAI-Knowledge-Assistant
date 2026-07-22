import os
from datetime import datetime

from config.settings import settings
from core.database import vector_store


class DocumentService:

    def __init__(self):
        self.upload_folder = settings.UPLOAD_FOLDER

        os.makedirs(
            self.upload_folder,
            exist_ok=True
        )

    def list_documents(self):
        """
        Return metadata of all uploaded PDFs.
        """

        documents = []

        for filename in os.listdir(self.upload_folder):

            file_path = os.path.join(
                self.upload_folder,
                filename
            )

            if not os.path.isfile(file_path):
                continue

            size = os.path.getsize(file_path)

            uploaded_time = datetime.fromtimestamp(
                os.path.getmtime(file_path)
            )

            documents.append(
                {
                    "filename": filename,
                    "size_bytes": size,
                    "size_mb": round(size / (1024 * 1024), 2),
                    "uploaded_at": uploaded_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )

        documents.sort(
            key=lambda x: x["uploaded_at"],
            reverse=True,
        )

        return documents

    def get_document_count(self):
        """
        Return total uploaded PDFs.
        """

        return len(self.list_documents())

    def get_document(self, filename):
        """
        Return one document.
        """

        for document in self.list_documents():

            if document["filename"] == filename:
                return document

        return None

    def delete_document(self, filename):
        """
        Delete uploaded PDF and its vectors.
        """

        file_path = os.path.join(
            self.upload_folder,
            filename,
        )

        if not os.path.exists(file_path):
            return False

        os.remove(file_path)

        vector_store.delete_document(filename)

        return True