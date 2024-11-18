import requests
import json
import os
import argparse
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def generate_redirect_json(filter_string=None):
    base_url = "https://cdn.builder.io/api/v3/content/redirects"
    headers = {
        'Accept': 'application/json'
    }
    
    limit = 100
    offset = 0
    all_redirects = []
    
    while True:
        url = f"{base_url}?apiKey={API_KEY}&limit={limit}&offset={offset}"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print("❌ Error: Failed to retrieve data from Builder.io")
            return
        
        data = response.json()
        
        results = data.get('results', [])
        if not results:
            print("No more redirects found. Exiting...")
            break
        
        for entry in results:
            if entry.get("published") == "published":
                name = entry.get("name", "")
                
                if filter_string and filter_string not in name:
                    continue
                
                source_url = entry['data']['source']
                destination_url = entry['data']['destination']
                permanent = entry['data']['permanent']
                
                status_code = 301 if permanent else 302
                
                all_redirects.append({
                    'initial_url': source_url,
                    'redirected_url': destination_url,
                    'status_code': status_code
                })

        offset += len(results)
        
        if len(results) < limit:
            print("All pages fetched. Exiting...")
            break
    
    output_json = {'redirects': all_redirects}
    os.makedirs('./json', exist_ok=True)
    with open('./json/redirects.json', 'w') as json_file:
        json.dump(output_json, json_file, indent=4)
    
    print("✅ Redirect JSON generated and saved as './json/redirects.json'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate JSON of redirects from Builder.io API")
    parser.add_argument("filter_string", nargs="?", default=None, help="Optional string to filter 'name' field")
    args = parser.parse_args()
    
    generate_redirect_json(args.filter_string)
