"""
File name: main.py

Description: This is the entry point for the Library License Checker tool. It orchestrates the workflow:
1. Parses input or detects packages.
2. Retrieves license information.
3. Rates each license based on trust level.
4. Outputs results to console or report files.

Goal: Designed to be CLI-invokable or tool-callable from an LLM orchestration system.
"""

from helpers import (read_code_file,
                     extract_imports,
                     print_license_report,
                     parse_requirements_text)

from license_api import check_imported_packages_licenses

def main(file_path: str):
    code_str = read_code_file(file_path)
    imports = extract_imports(code_str)
    print("Found imports:", imports)

    results = check_imported_packages_licenses(imports)
    print_license_report(results)

if __name__ == "__main__":
    main("requirements.txt")
    packages = parse_requirements_text("sample_requirements_test.txt")