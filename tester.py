import pandas as pd

# Load Excel files using the first column as index
khaan = pd.read_excel('excels/khaan_simple.xlsx', index_col=0)
golomt = pd.read_excel('excels/golomt_simple.xlsx', index_col=0)
state = pd.read_excel('excels/state_simple.xlsx', index_col=0)
trans = pd.read_excel('excels/trans_simple.xlsx', index_col=0)
xac = pd.read_excel('excels/xac_simple.xlsx', index_col=0)

# Reset index to ignore index alignment
khaan.reset_index(drop=False, inplace=True)
golomt.reset_index(drop=False, inplace=True)
state.reset_index(drop=False, inplace=True)
trans.reset_index(drop=False, inplace=True)
xac.reset_index(drop=False, inplace=True)

# Concatenate horizontally without using index alignment
merged_df = pd.concat([khaan, golomt, state, trans, xac], axis=1)

# Save to a new Excel file
merged_df.to_excel('excels/merged_bank_data.xlsx', index=True)
