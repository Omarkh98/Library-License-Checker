"""
Helper functions
"""

import ast
import requests

from config.libs import LICENSE_NORMALIZATION_MAP

def normalize_license_text(license_str: str) -> str:
    try:
        if not license_str:
            return "Unknown"

        norm = license_str.strip().lower()
        for key in LICENSE_NORMALIZATION_MAP:
            if key in norm:
                return LICENSE_NORMALIZATION_MAP[key]
        return "Unknown"
    except Exception:
        return "Unknown"

def rate_license(license_name: str):
    trusted = ["MIT", "APACHE", "BSD", "PSF"]
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

def extract_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code_str = f.read()

    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        print("Syntax error while parsing:", e)
        return []

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return sorted(list(imports))

def read_code_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def print_license_report(results: list[dict]):
    print(f"{'Package':20} {'License':15} {'Rating'}")
    print("-" * 50)
    for res in results:
        print(f"{res['name']:20} {res['license']:15} {res['rating']}")