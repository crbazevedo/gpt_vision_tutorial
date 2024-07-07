import fitz 
import os

def extract_objects(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            # img is a tuple, so extract the correct indices
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            x0 = max(float(img[2]), 0)
            y0 = max(float(img[4]), 0)
            x1 = min(float(img[3]), page.rect.width)
            y1 = min(float(img[5]), page.rect.height)

            bbox = fitz.Rect(x0, y0, x1, y1)
            if bbox.is_empty:
                continue

            # Save the image using the extracted image bytes
            img_path = os.path.join(output_dir, f"page_{page_num + 1}_img_{img_index + 1}.png")
            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)

            print(f"Extracted image: {img_path}")

    doc.close()
