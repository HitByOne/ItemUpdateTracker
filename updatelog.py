import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re

# Define the path to your OneDrive-synced folder
ONEDRIVE_PATH = '/Users/ybkmykeyz/Library/CloudStorage/OneDrive-IntegratedSupplyNetwork/PCS/Python Files/Update Log'
LOG_FILE = os.path.join(ONEDRIVE_PATH, 'change_log.xlsx')

def log_changes_to_file(item_numbers, changes, name, change_options, notes):
    # Ensure the log file exists
    if not os.path.isfile(LOG_FILE):
        # Create an empty DataFrame if the file does not exist
        columns = ['Item Number', 'Date', 'Entered By', 'Price Change', 'Description Update',
                   'Discontinued', 'Quantity Adjustment', 'Category Change', 'Notes']
        df = pd.DataFrame(columns=columns)
        df.to_excel(LOG_FILE, index=False)

    # Load existing data
    df = pd.read_excel(LOG_FILE)

    # Prepare new data
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_rows = []
    for item in item_numbers:
        row = [item, date, name]
        for change_option in change_options:
            row.append('Yes' if change_option in changes else 'No')
        row.append(notes)
        new_rows.append(row)
    
    # Append new data
    new_df = pd.DataFrame(new_rows, columns=df.columns)
    df = pd.concat([df, new_df], ignore_index=True)

    # Write back to the Excel file
    df.to_excel(LOG_FILE, index=False)

# Streamlit app layout
st.title("Item Change Tracker")

item_numbers_input = st.text_area("Enter Item Numbers (space, comma, or newline separated)")

names = ["John Doe", "Jane Smith", "Mark Johnson", "Emily Davis"]
name = st.selectbox("Select Your Name", names)

change_options = [
    "Price Change",
    "Description Update",
    "Discontinued",
    "Quantity Adjustment",
    "Category Change"
]

changes = st.multiselect("Select Changes", change_options)

notes = st.text_area("Enter Additional Notes")

if st.button("Log Changes"):
    if item_numbers_input and changes and name:
        item_numbers = re.split(r'[,\s\n]+', item_numbers_input.strip())
        item_numbers = [i for i in item_numbers if i]
        if not item_numbers:
            st.error("No valid item numbers provided.")
        else:
            try:
                log_changes_to_file(item_numbers, changes, name, change_options, notes)
                st.success("Changes have been logged successfully.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Please enter item numbers, select changes, and select your name.")
