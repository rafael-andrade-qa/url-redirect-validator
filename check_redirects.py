import os
import requests
import json
import sys

def check_redirect(url_to_test, expected_redirect_url, expected_status_code):
    try:
        response = requests.get(url_to_test, allow_redirects=True)
        final_url = response.url
        status_code = response.status_code
        result = {
            "initial_url": url_to_test,
            "expected_redirect_url": expected_redirect_url,
            "actual_redirect_url": final_url,
            "expected_status_code": expected_status_code,
            "actual_status_code": status_code,
            "status": "Passed" if final_url == expected_redirect_url and status_code == expected_status_code else "Failed"
        }
        
        print("\n🔍 Testing URL:", url_to_test)
        print(f"➡️  Expected Redirect: {expected_redirect_url}")
        print(f"🔄 Actual Redirected URL: {final_url}")
        print(f"✅ Expected Status Code: {expected_status_code}")
        print(f"📋 Actual Status Code: {status_code}")
        if result["status"] == "Passed":
            print("🎉 Test Passed: Redirection and status code match!\n")
        else:
            print("❌ Test Failed: Mismatch in redirection or status code.\n")
            
        return result

    except requests.RequestException as e:
        print("🚨 Error accessing URL:", url_to_test)
        print("🛑 Exception:", e, "\n")
        return {
            "initial_url": url_to_test,
            "expected_redirect_url": expected_redirect_url,
            "actual_redirect_url": None,
            "expected_status_code": expected_status_code,
            "actual_status_code": None,
            "status": "Error",
            "error": str(e)
        }

def main(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    results = []
    for entry in data:
        result = check_redirect(entry['initial_url'], entry['expected_redirect_url'], entry['expected_status_code'])
        results.append(result)
    
    # Print summary to terminal
    passed = len([r for r in results if r["status"] == "Passed"])
    failed = len([r for r in results if r["status"] == "Failed"])
    errors = len([r for r in results if r["status"] == "Error"])
    
    print("\n📊 Summary Report")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"🚨 Errors: {errors}\n")
    
    os.makedirs("reports", exist_ok=True)
    
    with open("reports/results.json", "w") as report_file:
        json.dump(results, report_file, indent=4)
    
    print("📁 JSON report saved as './reports/results.json'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❗ Usage: python check_redirects.py <json_file_path>")
    else:
        main(sys.argv[1])
