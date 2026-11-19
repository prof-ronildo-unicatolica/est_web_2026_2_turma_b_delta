from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True, env_file=".env")

    PROJECT_NAME: str = "Sistema de Reservas - Core Service"
    API_V1_STR: str = "/api/v1"
    CORS_ALLOWED_ORIGINS: str = (
        "http://localhost:5173,http://127.0.0.1:5173"
    )

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @field_validator("SECRET_KEY")
    @classmethod
    def validar_chave_secreta(cls, value: str) -> str:
        if len(value.encode("utf-8")) < 32:
            raise ValueError("SECRET_KEY deve ter pelo menos 32 bytes.")
        return value

    # Configurações do PostgreSQL
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "hotel_db_dev"
    POSTGRES_PORT: str = "5432"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    # Configurações do MongoDB
    MONGODB_URL: str
    MONGODB_DB: str = "hotel_mongo_dev"

    # Configurações do RabbitMQ
    RABBITMQ_URL: str


settings = Settings()
