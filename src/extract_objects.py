import fitz  # PyMuPDF
import pdfplumber
import os
import json

def extract_objects(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            with open(os.path.join(output_dir, f'page_{i+1}.txt'), 'w') as text_file:
                text_file.write(text)
            
            tables = page.extract_tables()
            with open(os.path.join(output_dir, f'tables_page_{i+1}.json'), 'w') as table_file:
                json.dump(tables, table_file)
            
            for j, img in enumerate(page.images):
                img_obj = page.within_bbox((img["x0"], img["top"], img["x1"], img["bottom"])).to_image()
                img_obj.save(os.path.join(output_dir, f'image_page_{i+1}_{j+1}.png'))

if __name__ == "__main__":
    pdf_path = "path_to_pdf"
    output_dir = "output_directory"
    extract_objects(pdf_path, output_dir)
