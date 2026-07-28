import json
import os

from datetime import datetime
from hashlib import sha256


class MetadataService:
    """
    Handles metadata storage for uploaded documents.
    """

    METADATA_FOLDER = "metadata"
    METADATA_FILE = "documents.json"

    def __init__(self):

        # Resolve path relative to this file so it works regardless of cwd
        self.metadata_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            self.METADATA_FOLDER,
        )

        self.metadata_file = os.path.join(
            self.metadata_folder,
            self.METADATA_FILE,
        )

        os.makedirs(self.metadata_folder, exist_ok=True)

    # ----------------------------------------
    # Internal Helpers
    # ----------------------------------------

    def load_metadata(self):

        if not os.path.exists(self.metadata_file):
            return []

        with open(
            self.metadata_file,
            "r",
            encoding="utf-8",
        ) as f:

            try:
                records = json.load(f)
            except json.JSONDecodeError:
                # Corrupted file - start fresh rather than crash
                return []

        # Backfill: records persisted before per-chat scoping have no
        # chat_id; treat them as belonging to the "default" chat so
        # they remain visible when the user is in the default chat.
        for record in records:
            record.setdefault("chat_id", "default")

        return records

    def save_metadata(self, documents):

        with open(
            self.metadata_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                documents,
                f,
                indent=4,
                ensure_ascii=False,
            )

    # ----------------------------------------
    # Hash
    # ----------------------------------------

    def calculate_hash(self, file_path):

        hasher = sha256()

        with open(file_path, "rb") as f:

            while True:

                chunk = f.read(8192)

                if not chunk:
                    break

                hasher.update(chunk)

        return hasher.hexdigest()

    # ----------------------------------------
    # Queries
    # ----------------------------------------

    def list_documents(self, chat_id=None):

        docs = self.load_metadata()

        if chat_id is None:
            return docs

        return [
            d
            for d in docs
            if d.get("chat_id") == chat_id
        ]

    def document_count(self, chat_id=None):

        return len(
            self.list_documents(chat_id=chat_id)
        )

    def exists_by_filename(self, filename):

        docs = self.load_metadata()

        return any(
            d["filename"] == filename
            for d in docs
        )

    def exists_by_hash(self, file_hash):

        docs = self.load_metadata()

        return any(
            d["hash"] == file_hash
            for d in docs
        )

    def get_document(self, filename):

        docs = self.load_metadata()

        for doc in docs:

            if doc["filename"] == filename:
                return doc

        return None

    # ----------------------------------------
    # CRUD
    # ----------------------------------------

    def add_document(
        self,
        filename,
        size_bytes,
        chunks,
        characters,
        original_filename=None,
        chat_id="default",
    ):

        docs = self.load_metadata()

        docs.append(
            {
                "filename": filename,
                "original_filename": original_filename,
                "size_bytes": size_bytes,
                "characters": characters,
                "chunks": chunks,
                "chat_id": chat_id,
                "uploaded_at": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
        )

        self.save_metadata(docs)

    def delete_document(self, filename):

        docs = self.load_metadata()

        docs = [
            d
            for d in docs
            if d["filename"] != filename
        ]

        self.save_metadata(docs)
