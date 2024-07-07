import os
import json

def index_objects(pdf_folder, output_file):
    index = []

    for root, _, files in os.walk(pdf_folder):
        for file in files:
            if file.endswith(".png") or file.endswith(".json"):
                page_number = int(file.split('_')[2])
                object_type = "image" if file.endswith(".png") else "table"
                index.append({
                    "file_name": os.path.basename(root),
                    "page_number": page_number,
                    "object_type": object_type,
                    "object_reference": file,
                    "caption": None  # Captions can be added if extracted
                })

    with open(output_file, 'w') as f:
        json.dump(index, f, indent=4)

if __name__ == "__main__":
    pdf_folder = "data/sample_documents"
    output_file = "data/index.json"
    index_objects(pdf_folder, output_file)
