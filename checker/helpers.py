"""

"""

import re
import ast
import requests

def normalize_license_text(raw_license: str):
    # Try to find SPDX-style license mentions
    spdx_patterns = [
        "MIT", "Apache[- ]?2.0", "BSD[- ]?3[- ]?Clause", "BSD[- ]?2[- ]?Clause", 
        "GPL[- ]?v?3", "GPL[- ]?v?2", "LGPL[- ]?v?3", "MPL[- ]?2.0", "AGPL[- ]?v?3"
    ]
    
    for pattern in spdx_patterns:
        match = re.search(pattern, raw_license, re.IGNORECASE)
        if match:
            # Normalize format (e.g., turn "BSD 3-Clause" into "BSD-3-Clause")
            return match.group(0).upper().replace(" ", "-")
    
    return "Unknown"

def rate_license(license_name: str):
    trusted = ["MIT", "APACHE", "BSD"]
    caution = ["LGPL", "MPL"]
    risky = ["GPL", "AGPL", "UNKNOWN", "OTHER"]

    license_upper = license_name.upper()

    if any(t in license_upper for t in trusted):
        return "✅ Trusted"
    elif any(c in license_upper for c in caution):
        return "⚠️ Caution"
    elif any(r in license_upper for r in risky):
        return "❌ Risky"
    else:
        return "⚠️ Unknown"
    
def fetch_license_from_pypi(package_name: str) -> str:
    FALLBACK_PYPI_URL = "https://pypi.org/pypi"
    try:
        url = f"{FALLBACK_PYPI_URL}/{package_name}/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            license_str = data.get("info", {}).get("license", "").strip()
            if license_str:
                return normalize_license_text(license_str)
    except Exception:
        pass
    return "Unknown"

def extract_imports(code_str):
    tree = ast.parse(code_str)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return list(imports)

def read_code_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def print_license_report(results: list[dict]):
    print(f"{'Package':20} {'License':15} {'Rating'}")
    print("-" * 50)
    for res in results:
        print(f"{res['name']:20} {res['license']:15} {res['rating']}")