import os
import requests
import json
import sys
from urllib.parse import urljoin, urlparse

def normalize_path(url):
    """Remove a barra final do caminho da URL, se existir."""
    parsed = urlparse(url)
    return parsed.path.rstrip('/')

def check_redirect(url_to_test, expected_redirect_url, expected_status_code):
    try:
        response = requests.get(url_to_test, allow_redirects=False)
        status_code = response.status_code
        redirect_url = response.headers.get("Location")

        if redirect_url and not redirect_url.startswith("http"):
            redirect_url = urljoin(url_to_test, redirect_url)

        # Normalizar caminhos para comparação
        expected_path = normalize_path(expected_redirect_url)
        actual_path = normalize_path(redirect_url or "")

        status = (
            "Passed"
            if expected_path == actual_path and status_code == expected_status_code
            else "Failed"
        )

        result = {
            "initial_url": url_to_test,
            "expected_redirect_url": expected_redirect_url,
            "actual_redirect_url": redirect_url,
            "expected_status_code": expected_status_code,
            "actual_status_code": status_code,
            "status": status,
        }

        print("\n🔍 Testing URL:", url_to_test)
        print(f"➡️  Expected Redirect: {expected_redirect_url}")
        print(f"🔄 Actual Redirected URL: {redirect_url or 'None (no redirection)'}")
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
            "error": str(e),
        }

def main(json_file_path, base_url):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    results = []
    failed_tests = []

    for entry in data["redirects"]:
        initial_url = urljoin(base_url, entry["initial_url"])
        expected_redirect_url = urljoin(base_url, entry["redirected_url"])
        expected_status_code = entry["status_code"]

        result = check_redirect(initial_url, expected_redirect_url, expected_status_code)
        results.append(result)

        if result["status"] != "Passed":
            failed_tests.append(result)

    passed = len([r for r in results if r["status"] == "Passed"])
    failed = len(failed_tests)
    errors = len([r for r in results if r["status"] == "Error"])

    print("\n📊 Summary Report")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"🚨 Errors: {errors}\n")

    os.makedirs("reports", exist_ok=True)

    with open("reports/results.json", "w") as report_file:
        json.dump(results, report_file, indent=4)
    print("📁 JSON report saved as './reports/results.json'.")

    if failed_tests:
        with open("reports/failed_tests.json", "w") as failed_file:
            json.dump(failed_tests, failed_file, indent=4)
        print("📁 Failed tests report saved as './reports/failed_tests.json'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❗ Usage: python check_redirects.py <json_file_path> <base_url>")
    else:
        json_file_path = sys.argv[1]
        base_url = sys.argv[2]
        main(json_file_path, base_url)
