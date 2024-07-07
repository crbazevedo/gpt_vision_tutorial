import json
import fitz  # PyMuPDF
from openai import OpenAI
from dotenv import load_dotenv
from pdf2image import convert_from_path
from PIL import Image
import os
import base64

load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def convert_pdf_to_images(pdf_path, max_size=(1024, 1024), max_file_size=20*1024*1024):
    pages = convert_from_path(pdf_path, 300)
    image_paths = []
    for i, page in enumerate(pages):
        image_path = f"page_{i + 1}.png"
        page.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save the image and check its size
        page.save(image_path, 'PNG')
        while os.path.getsize(image_path) > max_file_size:
            # If the image is still too large, reduce its size by adjusting the quality
            with Image.open(image_path) as img:
                img.thumbnail((img.width // 2, img.height // 2), Image.Resampling.LANCZOS)
                img.save(image_path, 'PNG', quality=85)
                
        image_paths.append(image_path)
    return image_paths

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_metadata_from_page(image_base64):
    prompt = f"""
    Extract the following metadata from the text on this page:
    - Title
    - Authors
    - Institutions
    - Number of Images (including their descriptions or captions)
    - List of Image Captions (for each image detected, if no caption is present, describe the image in relation to the rest of the page contents)
    - Number of Tables
    - List of Table Descriptions (including column and row labels, number of columns, number of rows, and a brief description for each table)
    - Summary of the Page

    Respond in JSON format.

    Example:
    ```json
    {{
      "Title": "Machine Learning Operations for Accelerator Control",
      "Authors": ["Tiamiceli (Lead-Accelerator AI/ML Group, Accelerator Controls Department, FNAL)"],
      "Institutions": ["Fermi Research Alliance, LLC"],
      "Number of Images": 2,
      "Image Captions": [
        "A diagram showing the workflow of the accelerator control system.",
        "A chart comparing the performance metrics of different machine learning models."
      ],
      "Number of Tables": 1,
      "Table Descriptions": [
        {{
          "Description": "Performance metrics of various machine learning models",
          "Column Labels": ["Model", "Accuracy", "Precision", "Recall"],
          "Row Labels": ["Model A", "Model B", "Model C"],
          "Number of Columns": 4,
          "Number of Rows": 3
        }}
      ],
      "Page Summary": "This page discusses the implementation of machine learning operations in accelerator control, detailing the workflow and performance metrics of different models."
    }}
    ```
    """

    response = client.chat.completions.create(model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a data extraction assistant."},
        {"role": "user",
         "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
            ]}
    ])

    content = response.choices[0].message.content

    # Clean the response to remove Markdown formatting
    if content.startswith("```json"):
        content = content[7:]  # Remove the leading ```json
    if content.endswith("```"):
        content = content[:-3]  # Remove the trailing ```

    return content

def coalesce(*values):
    return next((value for value in values if value), None)

def extract_metadata(pdf_path):
    print(f"Converting PDF to images: {pdf_path}")
    image_paths = convert_pdf_to_images(pdf_path)
    metadata_list = []

    for image_path in image_paths:
        print(f"Processing image: {image_path}")
        image_base64 = encode_image_to_base64(image_path)
        page_metadata = extract_metadata_from_page(image_base64)
        print(f"Extracted metadata from image {image_path}: {page_metadata}")
        metadata_list.append(json.loads(page_metadata))

    final_metadata = {
        "Title": coalesce(*[md.get("Title") for md in metadata_list]),
        "Authors": coalesce(*[md.get("Authors") for md in metadata_list]),
        "Institutions": coalesce(*[md.get("Institutions") for md in metadata_list]),
        "Number of Pages": len(metadata_list),
        "Number of Images": sum(md.get("Number of Images", 0) for md in metadata_list),
        "Number of Tables": sum(md.get("Number of Tables", 0) for md in metadata_list),
        "Image Captions": [img_caption for md in metadata_list for img_caption in md.get("Image Captions", [])],
        "Table Descriptions": [table_desc for md in metadata_list for table_desc in md.get("Table Descriptions", [])],
        "Page Summaries": [md.get("Page Summary") for md in metadata_list],
    }

    print(f"Final metadata: {final_metadata}")
    return final_metadata

if __name__ == "__main__":
    pdf_path = "path_to_pdf"
    metadata = extract_metadata(pdf_path)
    with open("metadata.json", "w") as f:
        f.write("{\n")
        for key, value in metadata.items():
            f.write(f'  "{key}": {json.dumps(value)},\n')
        f.write("}\n")
