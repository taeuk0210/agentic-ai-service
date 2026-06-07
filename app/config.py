from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    # App configration

    APP_ENV: str
    APP_LOG_PATH: str
    APP_LOG_COUNT: int
    EMBEDDING_MODEL: str
    EMBEDDING_DEVICE: str
    EMBEDDING_BATCH: int

    # Docker configuration

    COMPOSE_PROFILES: str

    # etcd configuration

    ETCD_PORT: int

    # Redis configration

    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_DATA_PATH: str

    # Minio configuration

    MINIO_PORT: int
    MINIO_HOST: str
    MINIO_CONSOLE_PORT: int
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_DATA_PATH: str

    # Milvus configuration

    MILVUS_PORT: int
    MILVUS_HOST: str
    MILVUS_WEBUI_PORT: int
    MILVUS_DATA_PATH: str

    # Weaviate configuration

    WEAVIATE_PORT: int
    WEAVIATE_HOST: str
    WEAVIATE_GRPC_PORT: int
    WEAVIATE_DATA_PATH: str

    # vLLM configuration

    VLLM_PORT: int
    VLLM_HOST: str
    VLLM_TIMEOUT: int
    HF_TOKEN: str
    VLLM_API_KEY: str
    VLLM_MODEL: str
    VLLM_GPU_UTIL: float
    VLLM_MAX_LEN: int
    VLLM_MAX_SEQS: int
    VLLM_KV_DTYPE: str
    VLLM_QUANTIZATION: str
    VLLM_DTYPE: str

    # .env configuration

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


config = AppConfig()
