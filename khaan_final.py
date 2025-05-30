import json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
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
    html_content = data[0]['body']

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
        if len(cols) == 2:  # Assuming each row has exactly 2 columns (label and amount)
            category = cols[0].text.strip()
            amount_str = cols[1].text.strip().replace(',', '')  # Remove commas from numbers
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

    # Display the DataFrame
    # print(df)
    return df

def read_data_ratio(data):
    # Read JSON data from the file
    with open(data, 'r') as file:
        data = json.load(file)
    
    # Extract HTML content from the first element in the list (assuming there's only one element)
    html_content = data[0]['body']

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
            herggui_str = cols[1].text.strip()
            amount_str = cols[2].text.strip().replace(',', '')  # Remove commas from numbers
            if amount_str:  # Check if amount_str is not empty
                try:
                    amount = convert_percent_to_numeric(amount_str)
                except ValueError:
                    amount = None  # Handle cases where conversion fails gracefully
            else:
                amount = None  # Handle empty strings
            categories.append(category)
            herggui.append(herggui_str)
            amounts.append(amount)

    # Create a DataFrame
    df = pd.DataFrame({
        'Category': categories,
        'herggui': herggui,
        'Amount': amounts
    })

    # Display the DataFrame
    # print(df)
    return df


def modify_table_for_regular(df, index):
    df.set_index(df.columns[0], inplace=True)  # Set the second column as the index
    df = df.dropna()

    df.loc["Бусад орлого"] = df.loc["Бусад дэлгэрэнгүй орлого/зардал"]
    indexes_to_keep = [
                "Хүүгийн орлого",
                "Монголбанкинд байршуулсан хөрөнгийн",
                "Банк, санхүүгийн байгууллагад байршуулсан хөрөнгийн",
                "Үнэт цаасны",
                "Зээлийн",
                "Бусад хүүгийн орлого",
                "Хүүгийн зардал",
                "Харилцахад төлсөн хүү",
                "Хадгаламжинд төлсөн хүү",
                "Зээлийн хүүгийн зардал",
                "Үнэт цаасны хүүгийн зардал",
                "Бусад хүүгийн зардал",
                "Хүүгийн цэвэр орлого",
                "Эрсдэлийн сангийн зардал",
                "Эрсдэлийн сангийн дараах цэвэр орлого",
                "Бусад орлого",
                "Хүүгийн бус орлого",
                "Арилжааны орлого",
                "Ханш, үнэлгээний тэгшитгэлийн орлого",
                "Банкны бүтээгдэхүүнтэй холбоотой үйлчилгээний хураамж, шимтгэлийн орлого",
                "Бусад хүүгийн бус орлого",
                "Бусад орлого, олз",
                "Бусад зардал",
                "Хүүгийн бус зардал",
                "Бусад эрсдэлийн сангийн зардал",
                "Арилжааны зардал",
                "Ханш, үнэлгээний тэгшитгэлийн зардал",
                "Хураамж, шимтгэлийн зардал",
                "Үйл ажиллагааны бусад зардал",
                "Бусад зардал, гарз",
                "Татварын өмнөх ашиг, алдагдал",
                "Орлогын татварын зардал",
                "Татварын дараах ашиг, алдагдал",
                "Бусад орлого",
                "Тайлант хугацааны нийт орлогын дүн"
    ]
    df = df.loc[indexes_to_keep]
    return df

output_file = "excels/khaan_simple.xlsx"
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df2 = read_data(f'json/khaan_df134.json')

    df2 = modify_table_for_regular(df2, 1)


    merged_df = pd.concat([df2], ignore_index=False)
    merged_df.index.names = [1]
    merged_df.rename(columns={merged_df.columns[0]: "ХААН"}, inplace=True)
    merged_df = merged_df.dropna()
    merged_df.to_excel(writer, index=True)


print("successfully!!!!!!!!1")
