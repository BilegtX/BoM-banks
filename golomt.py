import pandas as pd
takenUrl = input("URL link: ")

tables = pd.read_html(takenUrl)

# Define a function to convert strings to numeric values in the second column
def convert_third_column_to_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': '', '\(': '-', '\)': '',}, regex=True)  # Remove commas
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce')  # Convert to numeric
    return df

def convert_percent_to_numeric(df):
    df[df.columns[0]] = df[df.columns[0]].replace({',': '', '%': ''}, regex=True)  # Remove commas and percent signs
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce') / 100  # Convert to numeric and divide by 100
    return df


def modify_table_for_regular(df):
    df.set_index(df.columns[1], inplace=True)
    df = df.drop(labels=0, axis=1)
    df = convert_third_column_to_numeric(df)
    return df

def modify_table_for_ratio(df):
    print("this is second table")
    df.set_index(df.columns[0], inplace=True)
    df = df.drop(labels=1, axis=1)
    df = convert_percent_to_numeric(df)
    df.index.names = [1]
    return df


# Create a Pandas Excel writer using XlsxWriter as the engine
output_file = "excels/golomt_raw.xlsx"
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    for idx, i in enumerate(range(3, min(6, len(tables)))):
        df = tables[i]
        if idx == 0:
            df1 = modify_table_for_regular(df)
        elif idx == 2:
            df2 = modify_table_for_regular(df)
        elif idx == 1:
            df3 = modify_table_for_ratio(df)
        else:
            continue 
        
    # Merge the modified tables
    merged_df = pd.concat([df1, df2, df3], ignore_index=False)
    print(merged_df)
    
    merged_df.rename(columns={merged_df.columns[0]: "Голомт"}, inplace=True)
    merged_df = merged_df.dropna()

    # export the merged DataFrame to a different sheets
    merged_df.to_excel(writer, index=True)
print(f"Modified data has been saved to {output_file}")
