from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_MODEL: str
    EMBEDDING_MODEL: str
    UPLOAD_FOLDER: str
    QDRANT_PATH: str

    class Config:
        env_file = ".env"


settings = Settings()