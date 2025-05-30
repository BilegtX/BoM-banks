import requests
from bs4 import BeautifulSoup
import pandas as pd

# ------------------------------
# Input URL and fetch HTML
# ------------------------------
takenURL = input("url link: ")

response = requests.get(takenURL)

if response.status_code != 200:
    print(f"❌ Failed to retrieve data. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
tables = soup.find_all('table')
print(f"✅ Found {len(tables)} tables.")

def convert_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': '', '\(': '-', '\)': ''}, regex=True)
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce')
    return df

def convert_percent_to_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': '', '%': ''}, regex=True)
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce') / 100
    return df

def modify_table_for_regular(df):
    df = df.drop(df.columns[0], axis=1)
    df.set_index(df.columns[0], inplace=True)
    df = convert_numeric(df)
    df.dropna(inplace=True)
    df.rename(columns={df.columns[0]: 2}, inplace=True)
    return df

def modify_table_for_ratio(df):
    df = df.drop(df.columns[1], axis=1)
    df.set_index(df.columns[0], inplace=True)
    df = convert_percent_to_numeric(df)
    df.drop(["МОНГОЛБАНКНААС ТОГТООСОН ЗОХИСТОЙ ХАРЬЦААНЫ ШАЛГУУР ҮЗҮҮЛЭЛТИЙН БИЕЛЭЛТ"], errors='ignore', inplace=True)
    df.index.names = [1]
    df.rename(columns={df.columns[0]: 2}, inplace=True)
    return df

# ------------------------------
# Table parsing logic
# ------------------------------

df1 = pd.DataFrame()
df1_5 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()

for i, table in enumerate(tables[4:8]):
    rows = []
    for row in table.find_all('tr'):
        columns = row.find_all(['th', 'td'])
        row_data = [col.text.strip() for col in columns]
        if (i in [0, 2] and len(row_data) == 3) or (i in [1, 3] and len(row_data) in [2, 3]):
            rows.append(row_data)

    df = pd.DataFrame(rows)
    if i == 0:
        df1 = df
    elif i == 1:
        df1_5 = df.rename(columns={df.columns[0]: 1, df.columns[1]: 2})
    elif i == 2:
        df2 = df
    elif i == 3:
        df3 = df

# ------------------------------
# Merge and transform
# ------------------------------
if not df1.empty and not df1_5.empty:
    df1 = pd.concat([df1, df1_5], ignore_index=True)

df1 = modify_table_for_regular(df1)
df2 = modify_table_for_regular(df2)
df3 = modify_table_for_ratio(df3)

merged_df = pd.concat([df1, df2, df3], ignore_index=False)
merged_df.rename(columns={merged_df.columns[0]: "Транс"}, inplace=True)
merged_df.dropna(inplace=True)

# ------------------------------
# Export to Excel
# ------------------------------
merged_df.to_excel("excels/trans_raw.xlsx", index=True)
print("✅ Data saved to trans_raw.xlsx")
