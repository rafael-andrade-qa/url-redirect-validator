# URL Redirect Validator
This project is an automation tool for validating URL redirects and expected status codes. It includes two main scripts: `generate_redirect_json.py`, which creates a JSON of redirects from lists of URLs and status codes, and `check_redirects.py`, which tests the specified redirects and generates a report with the results.

## Project Structure

```bash
📦url-redirect-validator
 ┣ 📂json
 ┃ ┗ 📜redirects.json
 ┣ 📂reports
 ┃ ┣ 📜failed_tests.txt
 ┃ ┗ 📜results.json
 ┣ 📜.env
 ┣ 📜.env-example
 ┣ 📜.gitignore
 ┣ 📜check_redirects.py
 ┣ 📜generate_redirect_json.py
 ┣ 📜README.md
 ┗ 📜requirements.txt
```

## Requirements

- Python 3.x
- [Requests](https://pypi.org/project/requests/) library

## Setting up a Virtual Environment

1. Check if Python is installed: Open your terminal and run the following command to check if Python is installed:

   ```bash
   python3 --version
   ```

   ```bash
   python --version
   ```

    Note: if python is not installed, download and install [here](https://www.python.org/downloads/).

2. Run the following command to create a virtual environment named `venv`:

   ```bash
   python3 -m venv venv
   ```

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment using the command:

   ```bash
   source venv/bin/activate
   ```

   ```bash
   .\venv\Scripts\activate
   ```
    The command to exit a virtual environment (venv) in Python is: `deactivate`

## Installing Dependencies

- Install the dependencies listed in the `requirements.txt` file using the following command:

   ```bash
   pip3 install -r requirements.txt
   ```

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Generate Redirect JSON with `generate_redirect_json.py`

The `generate_redirect_json.py` script generates a JSON file with redirects to be validated by the `check_redirects.py` script.

#### Command

   ```bash
   python3 generate_redirect_json.py "<optional_filter_string>"
   ```

   ```bash
   python generate_redirect_json.py "<optional_filter_string>"
   ```

#### Example of Generated File

The above command will generate a `redirects.json` file with the following structure:

```bash
[
    {
        "initial_url": "https://example.com",
        "expected_redirect_url": "https://example.com/home",
        "expected_status_code": 301
    },
    ...
]
```

This file will be saved in the `./jsons` folder as `redirects.json`.

### Validate Redirects with `check_redirects.py`

The `check_redirects.py` script reads a JSON file containing a list of redirects, tests whether each initial URL redirects to the expected destination URL with the correct HTTP status code, and handles both absolute and relative redirects. It generates a summary of test results, categorizing them as passed, failed, or errors, and saves the results in `reports/results.json`. Additionally, failed tests are logged in a separate file, `reports/failed_tests.txt`, for further review.

#### Command

   ```bash
   python3 check_redirects.py <json_file_path> <base_url>"
   ```

   ```bash
   python check_redirects.py <json_file_path> <base_url>"
   ```

#### Terminal Output Example

Example output:

```bash
🔍 Testing URL: https://example.com
➡️  Expected Redirect: https://example.com/home
🔄 Actual Redirected URL: https://example.com/home
✅ Expected Status Code: 301
📋 Actual Status Code: 301
🎉 Test Passed: Redirection and status code match!
...
📊 Summary Report
✅ Passed: 3
❌ Failed: 1
🚨 Errors: 0
📁 JSON report saved as './reports/results.json'.
```

The final report with details for each redirect will be saved in `reports/results.json`.
