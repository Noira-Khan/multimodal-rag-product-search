import pandas as pd

def load_data(file_path="multimodal-rag-product-search/data/archive/styles.csv"):
    """
    Load data from a CSV file.

    Args:
        file_path (str): The path to the CSV file."""
    try:
        data=pd.read_csv(file_path, on_bad_lines="warn") # Handle bad lines by warning and skipping(on_bad_lines=skip) them
        print(f"data loaded successfully from {file_path}")
        return data
    except Exception as e:
        print(f"error loading data from {file_path}: {e}")
        return None
if __name__ == "__main__":
        df = load_data()

if df is not None:
        print(df.head())

