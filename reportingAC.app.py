#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:03:17 2024

@author: sergiobarrientoskellemberger
"""

import pandas as pd
import requests
from io import BytesIO

# Replace with your actual raw GitHub URL
excel_url = "https://github.com/sergiobk201/reportingWDApp/raw/main/delivered_reports.xlsx"

# Download the file
response = requests.get(excel_url)
response.raise_for_status()  # Check for errors

# Read the Excel file into Pandas
df = pd.read_excel(BytesIO(response.content))

# Convert 'Fields' column into sets for easier comparison
df["Fields"] = df["Fields"].apply(lambda x: set(str(x).split("\n")))

# Extract unique fields for selection
all_fields = sorted(set().union(*df['Fields']))

# Sidebar for selecting fields
st.sidebar.title("Select fields you want in the report")
selected_fields = st.sidebar.multiselect("Select Fields to Match", all_fields)

# Function to find matching reports
def find_matching_reports(df, input_fields, threshold=75):
    matching_reports = []
    input_field_count = len(input_fields)

    for _, report in df.iterrows():
        matching_fields = input_fields.intersection(report['Fields'])
        match_percentage = (len(matching_fields) / input_field_count) * 100 if input_field_count > 0 else 0

        if match_percentage >= threshold:
            matching_reports.append({'Report': report['Report'], 'Match Percentage': match_percentage})

    return pd.DataFrame(matching_reports)

# Show results when fields are selected
if selected_fields:
    st.write("### Matching Reports")
    selected_fields_set = set(selected_fields)
    results = find_matching_reports(df, selected_fields_set)

    if not results.empty:
        st.dataframe(results)
    else:
        st.write("No reports match the selected criteria.")
else:
    st.write("Select fields from the sidebar to see matching results.")
