# In utils/data_ingestion.py

from langchain_astradb import AstraDBVectorStore
# --- NEW, STABLE IMPORT ---
from langchain_community.embeddings import HuggingFaceEmbeddings
from utils.data_converter import DataConverter
from config.config import AppConfig
from utils.custom_exception import CustomException
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DataIngestor:
    def __init__(self):
        self.vstore = self._initialize_vector_store()

    def _initialize_vector_store(self) -> AstraDBVectorStore:
        try:
            logger.info("Initializing vector store with HuggingFaceEmbeddings...")

            # --- USING THE STABLE EMBEDDING CLASS ---
            # This will download the model on its first run
            embedding_model = HuggingFaceEmbeddings(
                model_name=AppConfig.EMBEDDING_MODEL
            )

            vector_store = AstraDBVectorStore(
                embedding=embedding_model,
                collection_name=AppConfig.ASTRA_DB_COLLECTION_NAME,
                api_endpoint=AppConfig.ASTRA_DB_API_ENDPOINT,
                token=AppConfig.ASTRA_DB_APPLICATION_TOKEN,
                namespace=AppConfig.ASTRA_DB_KEYSPACE
            )
            logger.info("Successfully connected to Astra DB Vector Store.")
            return vector_store
        except Exception as e:
            raise CustomException("Failed to initialize Astra DB Vector Store.", e)

    def ingest_data(self):
        try:
            logger.info("Starting data ingestion process...")
            converter = DataConverter(file_path=AppConfig.DATA_FILE_PATH)
            documents = converter.to_documents()

            if not documents:
                logger.warning("No documents found to ingest. Aborting.")
                return

            logger.info(f"Ingesting {len(documents)} documents...")
            self.vstore.add_documents(documents)
            logger.info("Data ingestion completed successfully.")
        except Exception as e:
            raise CustomException("An error occurred during data ingestion.", e)


