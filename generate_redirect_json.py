import json
import os
import sys

def load_json_list(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_redirect_json(urls_json, redirect_urls_json, status_codes_json):
    urls = load_json_list(urls_json)
    redirect_urls = load_json_list(redirect_urls_json)
    status_codes = load_json_list(status_codes_json)
    
    if len(urls) != len(redirect_urls) or len(urls) != len(status_codes):
        print("❌ Error: All lists must have the same length.")
        return
    
    data = []
    for initial_url, expected_redirect_url, expected_status_code in zip(urls, redirect_urls, status_codes):
        data.append({
            "initial_url": initial_url,
            "expected_redirect_url": expected_redirect_url,
            "expected_status_code": expected_status_code
        })

    with open("jsons/check_redirects/redirects.json", "w") as file:
        json.dump(data, file, indent=4)
    
    print("✅ JSON file 'jsons/check_redirects/redirects.json' created successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("❗ Usage: python generate_redirect_json.py <urls_json> <redirect_urls_json> <status_codes_json>")
    else:
        generate_redirect_json(sys.argv[1], sys.argv[2], sys.argv[3])
