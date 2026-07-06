from config.settings import settings

print("LLM Model:", settings.OLLAMA_MODEL)
print("Embedding Model:", settings.EMBEDDING_MODEL)
print("Upload Folder:", settings.UPLOAD_FOLDER)
print("Qdrant Path:", settings.QDRANT_PATH)