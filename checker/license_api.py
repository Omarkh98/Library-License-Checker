"""

"""

import os
import requests
from dotenv import load_dotenv
from checker.helpers import (normalize_license_text,
                             rate_license,
                             fetch_license_from_pypi)

load_dotenv()

API_KEY = os.getenv("LIBRARIES_IO_API_KEY")
BASE_URL = "https://libraries.io/api"

def fetch_license(package_name: str, platform = "pypi"):
    url = f"{BASE_URL}/{platform}/{package_name}?api_key={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            norm = data.get("normalized_licenses")
            if norm and isinstance(norm, list) and len(norm) > 0 and norm[0] != "Other":
                license_name = norm[0]
            else:
                raw_license = data.get("licenses")
                license_name = normalize_license_text(raw_license) if raw_license else "Unknown"

            if license_name == "Unknown":
                license_name = fetch_license_from_pypi(package_name)

            return {
                "name": package_name,
                "license": license_name,
                "rating": rate_license(license_name),
            }
        else:
            return {
                "name": package_name,
                "license": "Unknown",
                "rating": rate_license("Unknown"),
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "name": package_name,
            "license": "Unknown",
            "rating": rate_license("Unknown"),
            "error": str(e)
        }
    
def check_imported_packages_licenses(imports: list[str]) -> list[dict]:
    results = []
    for package in imports:
        license_info = fetch_license(package)
        results.append(license_info)
    return results