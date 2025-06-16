import os
import requests
import json
import sys
import time
import re
from urllib.parse import urljoin, urlparse

def normalize_url(url):
    """Normaliza a URL removendo barras finais e garantindo esquema consistente."""
    if not url:
        return None
    parsed = urlparse(url)
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")
    return normalized

def substitute_wildcard(path: str, token: str = "wildcard") -> str:
    return path.replace("*", token) if path else path

def check_redirect(url_to_test, expected_redirect_url, expected_status_code):
    try:
        response = requests.get(url_to_test, allow_redirects=False)
        status_code = response.status_code
        redirect_url = response.headers.get("Location")

        if redirect_url and not redirect_url.startswith("http"):
            redirect_url = urljoin(url_to_test, redirect_url)

        # Normaliza URLs para comparação precisa
        expected_normalized = normalize_url(expected_redirect_url)
        actual_normalized = normalize_url(redirect_url)

        status = (
            "Passed"
            if actual_normalized == expected_normalized and status_code in expected_status_code
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

def estimate_time_per_url(url_sample, base_url):
    """Calcula o tempo médio por URL com base em uma amostra."""
    start_time = time.time()
    for entry in url_sample:
        initial_url = urljoin(base_url, substitute_wildcard(entry["initial_url"]))
        requests.get(initial_url, allow_redirects=False)
    end_time = time.time()
    avg_time = (end_time - start_time) / len(url_sample)
    return avg_time

def main(json_file_path, base_url):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    total_urls = len(data["redirects"])
    url_sample = data["redirects"][:5] if total_urls >= 5 else data["redirects"]
    avg_time_per_url = estimate_time_per_url(url_sample, base_url)
    estimated_total_time = avg_time_per_url * total_urls

    print(f"\n⏱️ Estimativa de tempo total: {estimated_total_time:.2f} segundos ({estimated_total_time / 60:.2f} minutos)\n")

    results = []
    failed_tests = []

    for entry in data["redirects"]:
        initial_url = urljoin(base_url, substitute_wildcard(entry["initial_url"]))
        expected_redirect_url = urljoin(base_url, substitute_wildcard(entry["redirected_url"]))

        expected_status_code = [301, 308] if entry["permanent"] else [302, 307]
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
