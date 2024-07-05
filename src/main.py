from gpt_vision_processor import process_document
from utils import load_document

def main():
    document_path = 'data/sample_documents/document1.pdf'
    content = load_document(document_path)
    processed_content = process_document(content)
    print(processed_content)

if __name__ == "__main__":
    main()
