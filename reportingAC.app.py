#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# GitHub raw file URL (Replace with your actual URL)
GITHUB_EXCEL_URL = "https://github.com/sergiobk201/reportingWDApp/raw/main/delivered_reports.xlsx"

@st.cache_data  # Cache to avoid downloading the file multiple times
def load_data():
    response = requests.get(GITHUB_EXCEL_URL)
    response.raise_for_status()  # Stop if there's an error
    return pd.read_excel(BytesIO(response.content))

# Load the Excel file from GitHub
df = load_data()

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
