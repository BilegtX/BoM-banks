import requests
import pandas as pd
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
            amount_str = cols[1].text.strip().replace(',', '').replace('(', '').replace(')', '')  # Remove commas from numbers
            if amount_str:  # Check if amount_str is not empty
                try:
                    amount = float(amount_str)
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

    return df


def convert_percent_to_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': '', '%': ''}, regex=True)  # Remove commas and percent signs
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce') / 100  # Convert to numeric and divide by 100
    return df



def modify_table_for_regular(df):
    df.set_index(df.columns[0], inplace=True)  
    df.fillna(0, inplace=True)
    df.loc["Эрсдэлийн сангийн зардал"] = df.loc["Эрсдлийн сангийн зардал"]
    df.loc["Эрсдэлийн сангийн дараах цэвэр орлого"] = df.loc["Эрсдлийн сангийн дараах цэвэр орлого"]
    df.loc["Бусад эрсдэлийн сангийн зардал"] = df.loc["Бусад эрсдлийн сангийн зардал"]
    df.loc["Үйл ажиллагааны бусад зардал"] = df.loc["Үйл ажиллагааны зардал"]
    df.loc["Татварын өмнөх ашиг, алдагдал"] = df.loc["Татварын өмнөх ашиг"]
    df.loc["Татварын дараах ашиг, алдагдал "] = df.loc["Тайлант хугацааны ашиг"]
    df.loc["Бусад орлого"] = df.loc["Бусад дэлгэрэнгүй орлого"]
    df.loc["Тайлант хугацааны нийт орлогын дүн"] = df.loc["Нийт дэлгэрэнгүй орлого, татварын дараах байдлаар"]
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
        "Эрсдлийн сангийн дараах цэвэр орлого",
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
        "Хураамж, шимтгэлийн зардал",
        "Үйл ажиллагааны бусад зардал",
        "Бусад зардал, гарз",
        "Татварын өмнөх ашиг, алдагдал",
        "Орлогын татварын зардал",
        "Татварын дараах ашиг, алдагдал ",
        "Бусад орлого",
        "Тайлант хугацааны нийт орлогын дүн"
    ]
    df = df.loc[indexes_to_keep]
    
    df = df.dropna()
    df.index.names = [1]
    df.rename(columns={df.columns[0]: "ХАС"}, inplace=True)
    return df

df2 = read_data('json/xac_df2.json')

df2 = modify_table_for_regular(df2)

merged_df = pd.concat([df2 ], ignore_index=False)

merged_df.to_excel("excels/xac_simple.xlsx", index=True)