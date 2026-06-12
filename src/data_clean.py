import pandas as pd

file_path = "multimodal-rag-product-search/data/archive/styles.csv"
output_path = "multimodal-rag-product-search/data/archive/styles_cleaned.csv"


def inspect_data(path):
    """Load the CSV and display a quick summary."""

    # Some rows in this dataset contain an extra comma.
    df = pd.read_csv(path, on_bad_lines="warn")

    print("Data types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    return df


def clean_data(df):
    """Clean text, numeric values, duplicates, and missing data."""

    print("\nOriginal shape:", df.shape)

    # Removing unnecessary whitespace from text columns.
    text_columns = df.select_dtypes(include=["object", "string"]).columns

    for column in text_columns:
        df[column] = (df[column].astype("string").str.strip().str.replace(r"\s+", " ", regex=True))

    # Invalid numeric values will become missing values.
    df["id"] =pd.to_numeric(df["id"], errors="coerce")
    df["year"] =pd.to_numeric(df["year"], errors="coerce")

    df = df.drop_duplicates()

    # Removing rows where either of these important fields is missing.
    df =df.dropna(subset=["id", "productDisplayName"])

    df["id"] = df["id"].astype("int64")

    # Capital-I Int64 supports missing integer values.
    df["year"] = df["year"].astype("Int64")

    print("Cleaned shape:", df.shape)

    # Remove rows missing essential product information
    df = df.dropna(subset=["id", "productDisplayName"])

        # Fill missing categorical values
    columns_to_fill = ["baseColour", "season", "usage"]

    for column in columns_to_fill:
        df[column] = df[column].fillna("Unknown")

        # Keep missing years allowed
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        df["year"] = df["year"].astype("Int64")

    return df


df = inspect_data(file_path)
cleaned_df = clean_data(df)

cleaned_df.to_csv(output_path, index=False)

print("\nCleaned data saved to:", output_path)
