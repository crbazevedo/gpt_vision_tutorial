import os
import json

def index_objects(directory, metadata_path):
    index = {
        "images": [],
        "tables": []
    }

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.png'):
                parts = file.split('_')
                if len(parts) >= 3 and parts[0] == 'page':
                    try:
                        page_number = int(parts[1])
                        index["images"].append({
                            "file": os.path.join(root, file),
                            "page": page_number
                        })
                    except ValueError:
                        print(f"Skipping file {file} due to unexpected filename format")
            elif file.endswith('.json'):
                parts = file.split('_')
                if len(parts) == 3 and parts[0] == 'tables' and parts[1].startswith('page'):
                    try:
                        page_number = int(parts[1].replace('page', '').replace('.json', ''))
                        table_number = int(parts[2].replace('table', '').replace('.json', ''))
                        with open(os.path.join(root, file), 'r') as table_file:
                            table_content = json.load(table_file)
                        index["tables"].append({
                            "file": os.path.join(root, file),
                            "page": page_number,
                            "table": table_number,
                            "content": table_content
                        })
                    except (ValueError, json.JSONDecodeError) as e:
                        print(f"Skipping file {file} due to error: {e}")
                elif len(parts) == 2 and parts[0] == 'tables' and parts[1].startswith('page'):
                    try:
                        page_number = int(parts[1].replace('page', '').replace('.json', ''))
                        with open(os.path.join(root, file), 'r') as table_file:
                            table_content = json.load(table_file)
                        index["tables"].append({
                            "file": os.path.join(root, file),
                            "page": page_number,
                            "table": None,
                            "content": table_content
                        })
                    except (ValueError, json.JSONDecodeError) as e:
                        print(f"Skipping file {file} due to error: {e}")

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    metadata["extractedImages"] = index["images"]
    metadata["extractedTables"] = index["tables"]

    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)

