# In utils/data_converter.py

import pandas as pd
from typing import List
from langchain_core.documents import Document
from utils.custom_exception import CustomException
from utils.logger import setup_logger

# Initialize a logger for this module
logger = setup_logger(__name__)

class DataConverter:
    """
    A class to read a CSV file and convert its rows into LangChain Document objects.
    """
    def __init__(self, file_path: str):
        """
        Initializes the DataConverter.

        Args:
            file_path (str): The path to the input CSV file.
        """
        self.file_path = file_path
        logger.info(f"DataConverter initialized for file: {self.file_path}")

    def to_documents(self) -> List[Document]:
        """
        Reads the CSV, extracts relevant columns, and converts each row
        into a LangChain Document object.

        Returns:
            List[Document]: A list of LangChain Document objects.

        Raises:
            CustomException: If the file is not found, required columns are missing,
                             or another error occurs during conversion.
        """
        try:
            logger.info(f"Reading CSV from {self.file_path}...")
            # Use 'usecols' to only load the columns we need, saving memory
            df = pd.read_csv(self.file_path, usecols=["product_title", "review"])
            df.dropna(subset=["review"], inplace=True) # Remove rows where review is missing
            logger.info(f"Successfully loaded {len(df)} rows from CSV.")

            # Use the much faster df.to_dict('records') instead of iterrows()
            docs = [
                Document(
                    page_content=row['review'],
                    metadata={"product_name": row["product_title"]}
                )
                for row in df.to_dict('records')
            ]

            logger.info(f"Successfully converted {len(docs)} rows to Document objects.")
            return docs

        except FileNotFoundError as e:
            raise CustomException(f"CSV file not found at path: {self.file_path}", e)
        except KeyError as e:
            raise CustomException(f"Missing a required column in the CSV file: {e}", e)
        except Exception as e:
            raise CustomException("An unexpected error occurred during data conversion.", e)