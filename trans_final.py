import requests
from bs4 import BeautifulSoup
import pandas as pd

takenURL = 'https://transbank.mn/about-us/financial-information/quarterly-financial-statements'
response = requests.get(takenURL)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    
    df = []
    for idx, table in enumerate(tables):
        if idx == 2:  # Assuming the target table is the third table (index 2)
            rows = []
            for row in table.find_all('tr'):
                columns = row.find_all(['th', 'td'])
                row_data = [column.text.strip() for column in columns]
                if (idx in [0, 2] and len(row_data) == 3) or (i in [1, 3] and len(row_data) in [2, 3]):
                    rows.append(row_data)
            df2 = pd.DataFrame(rows)
            break


def convert_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': ''}, regex=True)  # Remove commas
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce')  # Convert to numeric
    return df
def convert_percent_to_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': '', '%': ''}, regex=True)  # Remove commas and percent signs
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce') / 100  # Convert to numeric and divide by 100
    return df


def modify_table_for_regular(df, index):
    df = df.drop([df.columns[0]], axis=1, inplace=False)
    df = df.drop([14, 16, 15])
    df.set_index(df.columns[0], inplace=True)  # Set column as the index
    df = convert_numeric(df)
    df.to_excel("psdave.xlsx", index=True)
    if index == 1:
        print("this is second table **********************************************************************************************************************")
        df.fillna(0, inplace=True)
        # print(df.loc[["Арилжааны зардал"], [2]])

        df.loc["Хүүгийн орлого"] = df.loc["Хүүний орлого"]
        df.loc["Хүүгийн зардал"] = df.loc["Хүүний зардал"]
        df.loc["Хүүгийн бус орлого"] = df.loc["Хүүний бус орлого"]
        df.loc["Хүүгийн бус зардал"] = df.loc["Хүүний бус зардал"]
        df.loc["Монголбанкинд байршуулсан хөрөнгийн"] = df.loc["Монголбанканд байршуулсан хөрөнгийн"]
        df.loc["Бусад хүүгийн орлого"] = df.loc["Бусад хүүний орлого"]
        df.loc["Бусад хүүгийн зардал"] = df.loc["Бусад хүүний зардал"]
        df.loc["Хадгаламжинд төлсөн хүү"] = df.loc["Хадгаламжид төлсөн хүү"]
        df.loc["Зээлийн хүүгийн зардал"] = df.loc["Зээлийн хүүний зардал"]
        df.loc["Үнэт цаасны хүүгийн зардал"] = df.loc["Үнэт цаасны хүүний зардал"]
        df.loc["Эрсдлийн сангийн зардал"] = df.loc["Эрсдэлийн сангийн зардал"]


        df.loc["Хүүгийн цэвэр орлого"] = df.loc["Цэвэр хүүний орлого (1-2)"]
        df.loc["Эрсдэлийн сангийн дараах цэвэр орлого"] = df.loc["Эрсдэлийн сангийн дараах цэвэр орлого (3-4)"]
        
        df.loc["Бусад орлого, олз"] = df.loc["Бусад  орлого, олз"]
        df.loc["Бусад хүүгийн бус орлого"] = df.loc["Бусад хүүний бус орлого"]

        df.loc["Татварын өмнөх ашиг, алдагдал"] = df.loc["Татварын өмнөх ашиг (5+6-7)"]
        df.loc["Орлогын татварын зардал"] = df.loc["Орлогын албан татварын зардал"]
        df.loc["Татварын дараах ашиг, алдагдал"] = df.loc["Татварын дараах ашиг (8-9)"]
        df.loc["Бусад орлого"] = df.loc["Бусад дэлгэрэнгүй орлого"]
        indexes_to_keep = [
            "Хүүгийн орлого","Монголбанкинд байршуулсан хөрөнгийн", "Банк, санхүүгийн байгууллагад байршуулсан хөрөнгийн", "Үнэт цаасны",
            "Зээлийн", "Бусад хүүгийн орлого", "Хүүгийн зардал", "Харилцахад төлсөн хүү", "Хадгаламжинд төлсөн хүү",
            "Зээлийн хүүгийн зардал", "Үнэт цаасны хүүгийн зардал", "Бусад хүүгийн зардал", "Хүүгийн цэвэр орлого", "Эрсдэлийн сангийн зардал",
            "Эрсдэлийн сангийн дараах цэвэр орлого", "Бусад орлого", "Хүүгийн бус орлого", "Арилжааны орлого",
            "Ханш, үнэлгээний тэгшитгэлийн орлого",
            "Банкны бүтээгдэхүүнтэй холбоотой үйлчилгээний хураамж, шимтгэлийн орлого", "Бусад хүүгийн бус орлого", "Бусад орлого, олз", "Бусад зардал", "Хүүний бус зардал",
            "Бусад эрсдэлийн сангийн зардал", "Арилжааны зардал","Ханш, үнэлгээний тэгшитгэлийн зардал", "Хураамж, шимтгэлийн зардал",
            "Үйл ажиллагааны бусад зардал", "Бусад зардал, гарз", "Татварын өмнөх ашиг, алдагдал", "Орлогын татварын зардал",
            "Татварын дараах ашиг, алдагдал","Бусад орлого", "Тайлант хугацааны нийт дэлгэрэнгүй орлогын дүн"
        ]
        df = df.loc[indexes_to_keep]
    
    df = df.dropna()
    df.rename(columns={df.columns[0]: 2}, inplace=True)
    return df



df2 = modify_table_for_regular(df2, 1)
merged_df = pd.concat([df2], ignore_index=False)

merged_df.rename(columns={merged_df.columns[0]: "Транс"}, inplace=True)


merged_df.to_excel("excels/trans_simple.xlsx", index=True)





