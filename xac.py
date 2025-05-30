import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json

# Disable SSL certificate verification warning (only for development purposes)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_page_data(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Disable SSL verification by setting verify to False
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def extract_table_data_sda(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')
        table_data = []
        for table in tables:
            rows = table.find_all('tr')
            table_rows = []
            for row in rows:
                cols = row.find_all(['th', 'td'])
                table_cols = []
                for col in cols:
                    table_cols.append(col.text.strip())
                table_rows.append(table_cols)
            table_data.append(table_rows)
        print("I WAS HERE XDDDDD")
        return table_data
    except Exception as e:
        print(f"Exception occurred while extracting table data: {str(e)}")
        return None

def display_table_data(url):
    print("I WAS HERE 1")
    html = get_page_data(url)
    # print(html)
    if html:
        table_data = extract_table_data_sda(html)
        print("I WAS HERE 2")
    temp_df = pd.DataFrame(table_data[0][1:], columns=table_data[0][0])
    return temp_df

def read_data(data_file):
    # Read JSON data from the file
    with open(data_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract HTML content from the first element in the list (assuming there's only one element)
    html_content = data['html']

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all table rows (tr) within the table
    table_rows = soup.find_all('tr')

    # Extract data into lists
    categories = []
    amounts = []

    for row in table_rows:
        cols = row.find_all('td')
        if len(cols) == 3:  # Assuming each row has exactly 2 columns (label and amount)
            category = cols[0].text.strip()
            amount_str = cols[1].text.strip()
            if amount_str == '-':
                amount_str = np.nan
            elif amount_str:  # Check if amount_str is not empty
                if '(' in amount_str and ')' in amount_str:  # Check if the amount is in parentheses
                    amount_str = amount_str.replace('(', '').replace(')', '')  # Remove parentheses
                    negative = True
                else:
                    negative = False
                
                try:
                    amount = float(amount_str.replace(',', ''))
                except ValueError:
                    amount = None  # Handle cases where conversion fails gracefully
            else:
                amount = None  # Handle empty strings
            
            if negative:
                amount = -amount  # Make the amount negative
            categories.append(category)
            amounts.append(amount)

    # Create a DataFrame
    df = pd.DataFrame({
        'Category': categories,
        'Amount': amounts
    })

    return df


def convert_percent_to_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': '', '%': ''}, regex=True)  # Remove commas and percent signs
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce') / 100  # Convert to numeric and divide by 100
    return df



def modify_table_for_regular(df):
    df.set_index(df.columns[0], inplace=True)  
    df.fillna(0, inplace=True)
    df = df.dropna()
    df.index.names = [1]
    df.rename(columns={df.columns[0]: "ХАС"}, inplace=True)
    return df

def modify_table_for_ratio(df):
    print("this is third table **********************************************************************************************************************")
    df = df.drop(df.columns[1], axis=1, inplace=False)
    df.set_index(df.columns[0], inplace=True)  # Set the first column as the index
    df = convert_percent_to_numeric(df)
    df.loc["Нэгдүгээр зэрэглэлийн өөрийн хөрөнгө болон эрсдэлээр жигнэсэн активын зохистой харьцаа"] = df.loc["Нэгдүгээр зэрэглэлийн өөрийн хөрөнгө болон эрсдлээр жигнэсэн активын зохистой харьцаа"]
    df.loc["Өөрийн хөрөнгө болон эрсдэлээр жигнэсэн активын харьцаа"] = df.loc["Өөрийн хөрөнгө болон эрсдлээр жигнэсэн активын харьцаа"]
    df = df.drop(["Өөрийн хөрөнгө болон эрсдлээр жигнэсэн активын харьцаа", "Нэгдүгээр зэрэглэлийн өөрийн хөрөнгө болон эрсдлээр жигнэсэн активын зохистой харьцаа"])
    df.index.names = [1]
    df.rename(columns={df.columns[0]: "ХАС"}, inplace=True)
    return df


df1 = read_data('json/xac_df1.json')
df2 = read_data('json/xac_df2.json')
df3 = display_table_data('https://www.xacbank.mn/page/prudential-ratios')

print(df1)
df1 = modify_table_for_regular(df1.drop(index=34))
df2 = modify_table_for_regular(df2)
df3 = modify_table_for_ratio(df3)


merged_df = pd.concat([df1, df2,df3], ignore_index=False)

merged_df = merged_df.dropna()

merged_df.to_excel("excels/xac_raw.xlsx", index=True)


print("successfully!!!!!!!!1")