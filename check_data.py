import pandas as pd

# Define the path to your data file
FILE_PATH = "data/flipkart_product_review.csv"

def analyze_product_data(file_path: str):
    """
    Loads the product review CSV and prints a summary of its contents.
    """
    try:
        print(f"--- Analyzing Data from: {file_path} ---\n")

        # Load the dataset
        df = pd.read_csv(file_path)

        # 1. Display basic information
        print("1. Basic DataFrame Info:")
        df.info()
        print("\n" + "="*50 + "\n")

        # 2. Show the first 5 rows to see the structure
        print("2. First 5 Rows of Data:")
        print(df.head())
        print("\n" + "="*50 + "\n")

        # 3. List all unique product titles in the dataset
        print("3. Unique Product Titles Available in the Dataset:")
        unique_titles = df['product_title'].unique()
        for i, title in enumerate(unique_titles):
            print(f"   - {title}")
        print(f"\nFound {len(unique_titles)} unique products.")
        print("\n" + "="*50 + "\n")

    except FileNotFoundError:
        print(f"Error: The file was not found at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    analyze_product_data(FILE_PATH)