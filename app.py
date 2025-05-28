"""
File name: app.py

Description: Streamlit web application for checking software licenses of Python packages
imported in an uploaded Python (.py) file.

Features:
- Upload a Python file and extract imported package names.
- Fetch license information for each detected package using the license API.
- Display package names, their licenses, and ratings in a table.
- Provide option to download the results as an Excel spreadsheet.
"""

import streamlit as st
import pandas as pd
import tempfile
import os
import io

from helpers import extract_imports
from license_api import fetch_license

st.set_page_config(page_title = "Library License Checker", layout = "centered")

st.title("Library License Checker")

uploaded_file = st.file_uploader("Upload a Python (.py) file", type = ["py"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".py") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name
    st.success("File uploaded successfully!")

    with st.spinner("Extracting Imports..."):
        packages  = extract_imports(temp_path)

    if not packages:
        st.warning("No packages found in this file.")
    else:
        st.subheader("Detected packages and license Info")
        results = []
        for pkg in packages:
            res = fetch_license(pkg)
            results.append(res)

            result_table = [
                {"Package": r["name"], "License": r["license"], "Rating": r["rating"]}
                for r in results
            ]
        st.table(result_table)

        df = pd.DataFrame(result_table)

        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine = "xlsxwriter") as writer:
            df.to_excel(writer, index = False, sheet_name = "Licenses")

        st.download_button(
            label = "📥 Download results as Excel",
            data = excel_buffer.getvalue(),
            file_name = "license_check_results.xlsx",
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    os.remove(temp_path)