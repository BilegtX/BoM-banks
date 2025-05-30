import pandas as pd
# takenUrl = input("URL link: ")

takenUrl = "https://golomtbank.com/investor-relations/season-report"

tables = pd.read_html(takenUrl)
def convert_third_column_to_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': ''}, regex=True)  # Remove commas
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce')  # Convert to numeric
    return df

def convert_percent_to_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': '', '%': ''}, regex=True)  # Remove commas and percent signs
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce') / 100  # Convert to numeric and divide by 100
    return df


def modify_table_for_regular(df, index):
    df.set_index(df.columns[1], inplace=True)
    df = df.drop(labels=0, axis=1)
    df = convert_third_column_to_numeric(df)
    if index == 2:
        print("this is third table")
        df.fillna(0, inplace=True)

        df.loc["Монголбанкинд байршуулсан хөрөнгийн"] = df.loc["Монгол банканд байршуулсан хөрөнгийн"]
        df.loc["Бусад эрсдэлийн сангийн зардал"] = df.loc["Бусад эрсдлийн сангийн зардал"] 
        df.loc["Хураамж, шимтгэлийн зардал"] = df.loc["Хураамж шимтгэлийн зардал"]

        df.loc["Бусад орлого"] = df.loc["Бусад дэлгэрэнгүй орлого"]
        df.loc["Нийт дэлгэрэнгүй орлого"] = df.loc["Тайлант хугацааны нийт орлогын дүн"]
    
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
                    "Хураамж шимтгэлийн зардал",
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


# Create a Pandas Excel writer using XlsxWriter as the engine
output_file = "excels/golomt_simple.xlsx"
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    for i in range(0, min(3, len(tables))):
        df = tables[i]
        if i == 2:
            df2 = modify_table_for_regular(df, i)
        else:
            continue 
    
    merged_df = pd.concat([df2], ignore_index=False)
    merged_df.rename(columns={merged_df.columns[0]: "Голомт"}, inplace=True)
    
    # export the merged DataFrame to a different sheets
    merged_df.to_excel(writer, index=True)
print(f"Modified data has been saved to {output_file}")
