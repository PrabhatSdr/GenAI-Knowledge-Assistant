import json
import os


class Memory:

    def __init__(self):
        self.memory_folder = "memory"
        os.makedirs(self.memory_folder, exist_ok=True)

    # -----------------------------------
    # Get file path
    # -----------------------------------

    def _get_file(self, chat_id: str):
        return os.path.join(
            self.memory_folder,
            f"{chat_id}.json"
        )

    # -----------------------------------
    # Load history
    # -----------------------------------

    def get_history(self, chat_id: str):

        file = self._get_file(chat_id)

        if not os.path.exists(file):
            return []

        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------------
    # Save one message
    # -----------------------------------

    def add(self, chat_id, role, content):

        history = self.get_history(chat_id)

        history.append(
            {
                "role": role,
                "content": content
            }
        )

        with open(
            self._get_file(chat_id),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                history,
                f,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------------------
    # List every chat
    # -----------------------------------

    def list_chats(self):

        chats = []

        for filename in os.listdir(self.memory_folder):

            if filename.endswith(".json"):

                chat_id = filename.replace(".json", "")

                history = self.get_history(chat_id)

                chats.append(
                    {
                        "chat_id": chat_id,
                        "messages": len(history)
                    }
                )

        return chats

    # -----------------------------------
    # Load one chat
    # -----------------------------------

    def load_chat(self, chat_id):

        return self.get_history(chat_id)

    # -----------------------------------
    # Delete one chat
    # -----------------------------------

    def delete_chat(self, chat_id):

        file = self._get_file(chat_id)

        if os.path.exists(file):
            os.remove(file)
            return True

        return False


memory = Memory()