import json
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from openpyxl import load_workbook

def converter(x):
    return float(x.strip('%'))/100

def convert_percent_to_numeric(x):
    x = x.replace(',', '').replace('%', '')  # Remove commas and percent signs
    x = pd.to_numeric(x, errors='coerce') / 100  # Convert to numeric and divide by 100
    return x

def read_data(data):
    # Read JSON data from the file
    with open(data, 'r') as file:
        data = json.load(file)
    
    # Extract HTML content from the first element in the list (assuming there's only one element)
    html_content = data["data"]['content']

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all table rows (tr) within the table
    table_rows = soup.find_all('tr')

    # Extract data into lists
    categories = []
    amounts = []
    negative = False
    for row in table_rows:
        cols = row.find_all('td')

        if len(cols) == 4:  
            category = cols[1].text.strip()
            amount_str = cols[3].text.strip()
        elif len(cols) == 3:  
            category = cols[0].text.strip()
            amount_str = cols[2].text.strip()
        else:
            continue  # Skip rows that don't have 3 or 4 columns

        if amount_str == '-':
            amount = np.nan
        elif amount_str:  # Check if amount_str is not empty
            negative = False
            if '(' in amount_str and ')' in amount_str:  # Check if the amount is in parentheses
                amount_str = amount_str.replace('(', '').replace(')', '')  # Remove parentheses
                negative = True
            
            try:
                amount = float(amount_str.replace(',', ''))
                if negative:
                    amount = -amount  # Make the amount negative
            except ValueError:
                amount = None  # Handle cases where conversion fails gracefully
        else:
            amount = None  # Handle empty strings

        categories.append(category)
        amounts.append(amount)

    # Create a DataFrame
    df = pd.DataFrame({
        'Category': categories,
        'Amount': amounts
    })

    # Display the DataFrame
    return df

def read_data_ratio(data):
    # Read JSON data from the file
    with open(data, 'r') as file:
        data = json.load(file)
    
    # Extract HTML content from the first element in the list (assuming there's only one element)
    html_content = data["data"]['content']

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all table rows (tr) within the table
    table_rows = soup.find_all('tr')

    # Extract data into lists
    categories = []
    herggui = []
    amounts = []

    for row in table_rows:
        cols = row.find_all('td')
        if len(cols) == 3:  # Assuming each row has exactly 3 columns (label, herggui, and amount)
            category = cols[0].text.strip()
            amount_str = cols[2].text.strip().replace(',', '')  # Remove commas from numbers
            if amount_str:  # Check if amount_str is not empty
                try:
                    amount = convert_percent_to_numeric(amount_str)
                except ValueError:
                    amount = None  # Handle cases where conversion fails gracefully
            else:
                amount = None  # Handle empty strings
            categories.append(category)
            amounts.append(amount)

    # Create a DataFrame
    df = pd.DataFrame({
        'Category': categories,
        'Amount': amounts
    })

    # Display the DataFrame
    # print(df)
    return df


def modify_table_for_regular(df):
    df.set_index(df.columns[0], inplace=True)  # Set the second column as the index
    df.fillna(0, inplace=True)
    df = df.dropna()
    return df

def modify_table_for_ratio(df):
    print("this is third table **********************************************************************************************************************")
    df.set_index(df.columns[0], inplace=True)  # Set the first column as the index
    return df


output_file = "excels/state_raw.xlsx"
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df1_2 = read_data(f'json/state.json')
    df3 = read_data_ratio(f'json/state.json')


    df1_2 = modify_table_for_regular(df1_2)
    df3 = modify_table_for_ratio(df3)

    merged_df = pd.concat([df1_2, df3], ignore_index=False)
    print(merged_df)
    merged_df.index.names = [1]
    merged_df.rename(columns={merged_df.columns[0]: "Төрийн банк"}, inplace=True)
    merged_df = merged_df.dropna()
    merged_df.to_excel(writer, index=True)


print("successfully!!!!!!!!1")
