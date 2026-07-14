import os
import json


class Memory:

    def __init__(self):

        self.memory_folder = "memory"

        os.makedirs(self.memory_folder, exist_ok=True)

    # -----------------------------------
    # Get file path
    # -----------------------------------

    def _get_file_path(self, chat_id):

        return os.path.join(
            self.memory_folder,
            f"{chat_id}.json"
        )

    # -----------------------------------
    # Load history
    # -----------------------------------

    def load(self, chat_id):

        file_path = self._get_file_path(chat_id)

        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------------
    # Save history
    # -----------------------------------

    def save(self, chat_id, history):

        file_path = self._get_file_path(chat_id)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                history,
                f,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------------------
    # Add message
    # -----------------------------------

    def add(self, chat_id, role, content):

        history = self.load(chat_id)

        history.append(
            {
                "role": role,
                "content": content
            }
        )

        self.save(chat_id, history)

    # -----------------------------------
    # Return history
    # -----------------------------------

    def get_history(self, chat_id):

        return self.load(chat_id)

    # -----------------------------------
    # Clear history
    # -----------------------------------

    def clear(self, chat_id):

        file_path = self._get_file_path(chat_id)

        if os.path.exists(file_path):
            os.remove(file_path)

    # -----------------------------------
    # List chats
    # -----------------------------------

    def list_chats(self):

        chats = []

        for file in os.listdir(self.memory_folder):

            if file.endswith(".json"):
                chats.append(file.replace(".json", ""))

        return chats


memory = Memory()