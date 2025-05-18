"""

"""

def parse_requirements_text(file_path: str):
    packages = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                pkg = line.split("==")[0].split(">=")[0].split("<=")[0]
                packages.append(pkg)
    return packages