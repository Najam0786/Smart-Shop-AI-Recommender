import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def get_env_variable(var_name: str) -> str:
    """
    Gets an environment variable or raises an error if it's not found.
    This ensures the application fails fast if a required variable is missing.
    """
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Error: Environment variable '{var_name}' not found. Please set it in your .env file.")
    return value

class AppConfig:
    """
    Centralized configuration for the application.

    Loads sensitive data from environment variables and defines application constants.
    """
    # Secrets loaded securely from the .env file
    ASTRA_DB_API_ENDPOINT: str = get_env_variable("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN: str = get_env_variable("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEYSPACE: str = get_env_variable("ASTRA_DB_KEYSPACE")
    GROQ_API_KEY: str = get_env_variable("GROQ_API_KEY")
    HUGGINGFACEHUB_API_TOKEN: str = get_env_variable("HUGGINGFACEHUB_API_TOKEN")
    FLASK_SECRET_KEY: str = get_env_variable("FLASK_SECRET_KEY")

    # Application constants (non-sensitive values)
    EMBEDDING_MODEL: str = "BAAI/bge-base-en-v1.5"
    RAG_MODEL: str = "llama-3.1-8b-instant"

    # Data and Vector Store settings
    DATA_FILE_PATH: str = "data/flipkart_product_review.csv"
    ASTRA_DB_COLLECTION_NAME: str = "flipkart_reviews"

    # RAG Chain settings
    RAG_TEMPERATURE: float = 0.5
    RAG_RETRIEVER_K: int = 3