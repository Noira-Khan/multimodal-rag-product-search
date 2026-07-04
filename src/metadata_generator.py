"""
==========================================================
Metadata Generator
Multimodal Retail Assistant (Myntra AI)
==========================================================

Purpose
-------
Reads the cleaned Myntra CSV dataset and generates a
structured JSON file that will later be used by the
RAG pipeline.

Input
-----
data/styles_cleaned.csv

Output
------
docs/product_metadata.json

This script only needs to be executed once whenever the
dataset changes.

Author: Noira Khan
==========================================================
"""

from pathlib import Path
import json
import pandas as pd


# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "data" / "styles_cleaned.csv"

OUTPUT_FILE = BASE_DIR / "docs" / "product_metadata.json"


# ----------------------------------------------------------
# Fields used in semantic search
# ----------------------------------------------------------

SEARCHABLE_FIELDS = {
    "Brand": "brandName",
    "Product Name": "productDisplayName",
    "Gender": "gender",
    "Category": "masterCategory",
    "Subcategory": "subCategory",
    "Article Type": "articleType",
    "Colour": "baseColour",
    "Season": "season",
    "Usage": "usage",
    "Year": "year",
}


# ----------------------------------------------------------
# Convert dataframe row into product dictionary
# ----------------------------------------------------------

def row_to_product(row):

    product_id = int(row["id"])

    document_lines = []

    for label, column in SEARCHABLE_FIELDS.items():

        if column in row and pd.notna(row[column]):

            document_lines.append(
                f"{label}: {row[column]}"
            )

    document = "\n".join(document_lines)

    product = {

        "id": product_id,

        "product_name": row.get(
            "productDisplayName",
            "Unknown Product"
        ),

        "brand": row.get(
            "brandName",
            "Unknown"
        ),

        "gender": row.get(
            "gender",
            ""
        ),

        "category": row.get(
            "masterCategory",
            ""
        ),

        "subcategory": row.get(
            "subCategory",
            ""
        ),

        "article_type": row.get(
            "articleType",
            ""
        ),

        "colour": row.get(
            "baseColour",
            ""
        ),

        "season": row.get(
            "season",
            ""
        ),

        "usage": row.get(
            "usage",
            ""
        ),

        "year": row.get(
            "year",
            ""
        ),

        "image_path": f"data/images/{product_id}.jpg",

        "document": document
    }

    return product


# ----------------------------------------------------------
# Create Metadata JSON
# ----------------------------------------------------------

def create_product_catalog():

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV not found:\n{CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    products = []

    for _, row in df.iterrows():

        products.append(
            row_to_product(row)
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            products,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("=" * 60)
    print("Metadata generation completed.")
    print(f"Products : {len(products)}")
    print(f"Output   : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":

    create_product_catalog()
    