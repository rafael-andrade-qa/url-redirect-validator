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
        
        print(f"\n🌐 Fetching data from: {url}")
        
        try:
            response = requests.get(
                url,
                headers=headers,
                allow_redirects=False,
                verify=False
            )
            
            if response.status_code != 200:
                print(f"❌ Error: Failed to retrieve data. Status Code: {response.status_code}")
                return
            
            print("\n📋 Response Headers:")
            for key, value in response.headers.items():
                print(f"   {key}: {value}")

            data = response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error during request: {e}")
            return

        results = data.get('results', [])
        if not results:
            print("\n✅ No more redirects found. Exiting...\n")
            break
        
        print(f"\n🔎 Found {len(results)} entries. Filtering...\n")
        for entry in results:
            if entry.get("published") == "published":
                name = entry.get("name", "")
                
                if filter_string and filter_string not in name:
                    print(f"⚠️ Skipping '{name}' (does not match filter).")
                    continue
                
                source_url = entry['data']['source']
                destination_url = entry['data']['destination']
                permanent = entry['data']['permanent']
                
                all_redirects.append({
                    'initial_url': source_url,
                    'redirected_url': destination_url,
                    'permanent': permanent
                })

        offset += len(results)
        
        if len(results) < limit:
            print("\n📦 All pages fetched. Exiting...\n")
            break
    
    output_json = {'redirects': all_redirects}
    os.makedirs('./json', exist_ok=True)
    with open('./json/redirects.json', 'w') as json_file:
        json.dump(output_json, json_file, indent=4)
    
    print("\n🎉 Redirect JSON successfully generated!")
    print("📂 File saved at: './json/redirects.json'\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate JSON of redirects from Builder.io API")
    parser.add_argument("filter_string", nargs="?", default=None, help="Optional string to filter 'name' field")
    args = parser.parse_args()
    
    generate_redirect_json(args.filter_string)
