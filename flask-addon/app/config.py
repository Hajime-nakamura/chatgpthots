import os

class Config:
    CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*")
    APP_NAME = os.getenv("APP_NAME", "flask-addon")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    VECTOR_DIM = int(os.getenv("VECTOR_DIM", "384"))
    MAX_CORPUS = int(os.getenv("MAX_CORPUS", "100000"))
