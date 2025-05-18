from checker.helpers import (read_code_file,
                             extract_imports,
                             print_license_report)

from checker.license_api import check_imported_packages_licenses

def main(file_path: str):
    code_str = read_code_file(file_path)
    imports = extract_imports(code_str)
    print("Found imports:", imports)

    results = check_imported_packages_licenses(imports)
    print_license_report(results)

if __name__ == "__main__":
    main("requirements.txt")
    # packages = parse_requirements_text("sample_requirements_test.txt")
    # print("Parsed Packages: ", packages)

    # print("\n")

    # for pkg in packages:
    #     result = fetch_license(pkg)
    #     print(f'{result["name"]} ➜ {result["license"]} ➜ {result["rating"]}')

