import json
import os
import pandas as pd




CSV_PATH = r"data\archive\styles_cleaned.csv"
IMAGE_FOLDER = r"data\archive\images"
OUTPUT_FILE = r"docs\product_metadata.json"

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



def row_to_product(row):

    # Get product ID
    product_id = int(row["id"])

    # Create empty list
    document_lines = []

    # Loop through each metadata field
    for label, column in SEARCHABLE_FIELDS.items():

        # Check if column exists and value is not empty
        if column in row and pd.notna(row[column]):

            line = label + ": " + str(row[column])

            document_lines.append(line)

    # Create image path
    image_path = os.path.join(
        IMAGE_FOLDER,
        str(product_id) + ".jpg"
    )

    image_path = image_path.replace("\\", "/")

    # Join all metadata lines into one document
    document = "\n".join(document_lines)

    # Create product dictionary
    product = {}

    product["id"] = product_id
    product["image_path"] = image_path
    product["product_name"] = row["productDisplayName"]
    product["document"] = document

    return product


def create_product_catalog():

    # Read CSV file
    df = pd.read_csv(CSV_PATH)

    # Create empty list
    products = []

    # Process each row
    for index, row in df.iterrows():

        product = row_to_product(row)

        products.append(product)

    # Create output folder if missing
    output_folder = os.path.dirname(OUTPUT_FILE)

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    # Save JSON file
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

    # Print results
    print("Saved", len(products), "products")
    print("Output file:", OUTPUT_FILE)


if __name__ == "__main__":

    create_product_catalog()