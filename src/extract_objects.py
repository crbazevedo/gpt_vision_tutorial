import fitz  # PyMuPDF
import os

def extract_objects(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            print(f"Image {img_index}: {img}")  # Print the img variable to see its content
            print(f"xref: {img[0]}")
            print(f"smask: {img[1]}")
            print(f"width: {img[2]}")
            print(f"height: {img[3]}")
            print(f"bpc: {img[4]}")
            print(f"colorspace: {img[5]}")
            print(f"alt_colorspace: {img[6]}")
            print(f"name: {img[7]}")
            print(f"filter: {img[8]}")
            print(f"dpi: {img[9]}")

            try:
                x0 = 0
                y0 = 0
                x1 = float(img[2])  # width
                y1 = float(img[3])  # height
            except ValueError as e:
                print(f"Skipping image {img_index} due to ValueError: {e}")
                continue  # Skip this image if it has non-numeric coordinates

            bbox = fitz.Rect(x0, y0, x1, y1)
            if bbox.is_empty:
                continue

            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Save the image using the extracted image bytes
            img_path = os.path.join(output_dir, f"page_{page_num + 1}_img_{img_index + 1}.png")
            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)

            print(f"Extracted image: {img_path}")

    doc.close()
