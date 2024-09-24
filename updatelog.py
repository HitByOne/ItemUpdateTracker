import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os
import re

# Define the path to your OneDrive-synced folder
ONEDRIVE_PATH = '/Users/ybkmykeyz/Library/CloudStorage/OneDrive-IntegratedSupplyNetwork/PCS/Python Files/'
DB_FILE = os.path.join(ONEDRIVE_PATH, 'team_log.db')

# Ensure the database and table exist
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_number TEXT,
        date TEXT,
        entered_by TEXT,
        price_change TEXT,
        description_update TEXT,
        discontinued TEXT,
        quantity_adjustment TEXT,
        category_change TEXT,
        notes TEXT
    )
''')
conn.commit()

def log_changes_to_db(item_numbers, changes, name, change_options, notes):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for item in item_numbers:
        row = [item, date, name] + ['Yes' if option in changes else 'No' for option in change_options] + [notes]
        cursor.execute('''
            INSERT INTO changes (item_number, date, entered_by, price_change, description_update,
                discontinued, quantity_adjustment, category_change, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row)
    conn.commit()

# Streamlit app layout using columns to make fields wider
st.title("Item Change Tracker")
cols1 = st.columns((1,1))  # Adjust the tuple values to change the relative width of columns
item_numbers_input = cols1[0].text_area("Enter Item Numbers (space, comma, or newline separated)", height=300)
names = ["John Doe", "Jane Smith", "Mark Johnson", "Emily Davis"]
name = cols1[1].selectbox("Select Your Name", names)

cols2 = st.columns((1,1))
change_options = ["Price Change", "Description Update", "Discontinued", "Quantity Adjustment", "Category Change"]
changes = cols2[0].multiselect("Select Changes", change_options)
notes = cols2[1].text_area("Enter Additional Notes", height=300)

if st.button("Log Changes"):
    if item_numbers_input and changes and name:
        item_numbers = re.split(r'[,\s\n]+', item_numbers_input.strip())
        item_numbers = [i for i in item_numbers if i]
        if not item_numbers:
            st.error("No valid item numbers provided.")
        else:
            try:
                log_changes_to_db(item_numbers, changes, name, change_options, notes)
                st.success("Changes have been logged successfully.")
                # Load and display the updated log
                df = pd.read_sql_query("SELECT * FROM changes", conn)
                st.subheader("Updated Change Log")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Please enter item numbers, select changes, and select your name.")
