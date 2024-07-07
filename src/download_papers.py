import os
import argparse
import requests
from datetime import datetime
from tqdm import tqdm

CROSSREF_API_URL = "https://api.crossref.org/works"
UNPAYWALL_API_URL = "https://api.unpaywall.org/v2"

def query_crossref(query, rows=10, start_date=None, end_date=None):
    params = {
        'query': query,
        'rows': rows,
        'filter': []
    }
    if start_date:
        params['filter'].append(f'from-pub-date:{start_date}')
    if end_date:
        params['filter'].append(f'until-pub-date:{end_date}')
    
    params['filter'] = ",".join(params['filter'])
    
    response = requests.get(CROSSREF_API_URL, params=params, verify=False)
    response.raise_for_status()
    return response.json()['message']['items']

def download_pdf_from_unpaywall(doi, email, download_dir):
    url = f"{UNPAYWALL_API_URL}/{doi}?email={email}"
    response = requests.get(url, verify=False)
    response.raise_for_status()
    data = response.json()
    pdf_url = data.get('best_oa_location', {}).get('url_for_pdf')
    if pdf_url:
        response = requests.get(pdf_url, verify=False)
        response.raise_for_status()
        filename = doi.replace("/", "_") + ".pdf"
        with open(os.path.join(download_dir, filename), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"No PDF found for DOI: {doi}")

def main(query, max_results, download_dir, start_date, end_date, email):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    items = query_crossref(query, rows=max_results, start_date=start_date, end_date=end_date)
    for item in tqdm(items):
        doi = item['DOI']
        try:
            download_pdf_from_unpaywall(doi, email, download_dir)
        except Exception as e:
            print(f"Failed to download {doi}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download papers using CrossRef and Unpaywall APIs")
    parser.add_argument('query', type=str, help='Search query')
    parser.add_argument('--max_results', type=int, default=10, help='Maximum number of results to download')
    parser.add_argument('--start_date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end_date', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('--download_dir', type=str, default='downloaded_papers', help='Directory to download papers')
    parser.add_argument('--email', type=str, required=True, help='Email address required by Unpaywall API')
    
    args = parser.parse_args()
    
    main(args.query, args.max_results, args.download_dir, args.start_date, args.end_date, args.email)
