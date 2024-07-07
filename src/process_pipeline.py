import os
import json
from extract_metadata import extract_metadata
from extract_objects import extract_objects
from index_objects import index_objects

def process_pdfs(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pdf_file in os.listdir(input_dir):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, pdf_file)
            metadata = extract_metadata(pdf_path)
            metadata_path = os.path.join(output_dir, f'{pdf_file[:-4]}_metadata.json')
            with open(metadata_path, 'w') as meta_file:
                json.dump(metadata, meta_file)
            
            extract_objects(pdf_path, os.path.join(output_dir, pdf_file[:-4]))
            
            # Index the extracted objects and update the metadata
            index_objects(os.path.join(output_dir, pdf_file[:-4]), metadata_path)

def main(query, max_results, start_date, end_date, email, skip_download):
    download_dir = 'data/sample_documents'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Step 1: Download Papers (only if not skipping)
    if not skip_download:
        from download_papers import main as download_papers
        download_papers(query, max_results, download_dir, start_date, end_date, email)
    
    # Step 2: Process PDFs to extract metadata and objects
    process_pdfs(download_dir, download_dir)
    
    # Step 3: Index the extracted objects
    index_objects(download_dir, os.path.join(download_dir, "index.json"))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process the entire PDF pipeline")
    parser.add_argument('query', type=str, help='Search query')
    parser.add_argument('--max_results', type=int, default=10, help='Maximum number of results to download')
    parser.add_argument('--start_date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end_date', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('--email', type=str, required=True, help='Email address required by Unpaywall API')
    parser.add_argument('--skip_download', action='store_true', help='Skip downloading PDFs if they are already downloaded')
    
    args = parser.parse_args()
    
    main(args.query, args.max_results, args.start_date, args.end_date, args.email, args.skip_download)
