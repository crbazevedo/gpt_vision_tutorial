import fitz  # PyMuPDF
import pdfplumber
import os
import json

def extract_objects(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the PDF with pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extract text
            text = page.extract_text()
            if text:
                with open(os.path.join(output_dir, f'page_{i+1}.txt'), 'w') as text_file:
                    text_file.write(text)
            
            # Extract tables
            tables = page.extract_tables()
            tables_data = []
            for table_index, table in enumerate(tables):
                table_data = {
                    "page": i + 1,
                    "table_index": table_index + 1,
                    "columns": table[0],
                    "rows": table[1:],
                    "number_of_columns": len(table[0]),
                    "number_of_rows": len(table) - 1
                }
                tables_data.append(table_data)
                table_json_path = os.path.join(output_dir, f'tables_page_{i+1}_table_{table_index+1}.json')
                with open(table_json_path, 'w') as table_file:
                    json.dump(table_data, table_file, indent=4)
            
            # Open the same page with fitz for image extraction
            doc = fitz.open(pdf_path)
            fitz_page = doc.load_page(i)
            images = fitz_page.get_images(full=True)
            image_data = []
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Save the image using the extracted image bytes
                img_path = os.path.join(output_dir, f"page_{i+1}_img_{img_index + 1}.png")
                with open(img_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                image_data.append({
                    "image_path": img_path,
                    "xref": xref,
                    "width": base_image.get("width"),
                    "height": base_image.get("height"),
                    "colorspace": img[5],
                    "filter": img[8]
                })

            # Save metadata for the page
            page_metadata_path = os.path.join(output_dir, f"page_{i+1}_metadata.json")
            page_metadata = {
                "page_number": i + 1,
                "text_path": os.path.join(output_dir, f'page_{i+1}.txt') if text else None,
                "images": image_data,
                "tables": tables_data
            }
            with open(page_metadata_path, 'w') as meta_file:
                json.dump(page_metadata, meta_file, indent=4)

