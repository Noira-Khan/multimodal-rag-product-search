import json
import os
import pandas as pd


# ---------- Configuration ----------

# ---------- Configuration ----------

CSV_PATH = "data/archive/styles_cleaned.csv"
IMAGE_FOLDER = "data/archive/images"
OUTPUT_FILE = "docs/product_metadata.json"

ID_COLUMN = "id"
NAME_COLUMN = "productDisplayName"


SEARCHABLE_FIELDS = {
    "Product Name": "productDisplayName",
    "Gender": "gender",
    "Category": "masterCategory",
    "Subcategory": "subCategory",
    "Article Type": "articleType",
    "Color": "baseColour",
    "Season": "season",
    "Year": "year",
    "Usage": "usage",
}


# ---------- Conversion ----------

def row_to_product(row):
    product_id = int(row[ID_COLUMN])

    document_lines = [
        f"{label}: {row[column]}"
        for label, column in SEARCHABLE_FIELDS.items()
        if column in row and pd.notna(row[column])
    ]

    return {
        "id": product_id,
        "image_path": os.path.join(
            IMAGE_FOLDER,
            f"{product_id}.jpg",
        ).replace("\\", "/"),
        "product_name": row[NAME_COLUMN],
        "document": "\n".join(document_lines),
    }


def create_product_catalog():
    df = pd.read_csv(CSV_PATH)

    products = [
        row_to_product(row)
        for _, row in df.iterrows()
    ]

    output_folder = os.path.dirname(OUTPUT_FILE)
    os.makedirs(output_folder, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            products,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"Saved {len(products)} products")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_product_catalog()