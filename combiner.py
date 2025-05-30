import pandas as pd

khaan = pd.read_excel('excels/khaan_simple.xlsx')
golomt = pd.read_excel('excels/golomt_simple.xlsx')
state = pd.read_excel('excels/state_simple.xlsx')
trans = pd.read_excel('excels/trans_simple.xlsx')
xac = pd.read_excel('excels/xac_simple.xlsx')

# Reset index to numeric index to avoid index alignment issues
khaan.reset_index(drop=True, inplace=True)
golomt.reset_index(drop=True, inplace=True)
state.reset_index(drop=True, inplace=True)
trans.reset_index(drop=True, inplace=True)
xac.reset_index(drop=True, inplace=True)

# Merge ignoring the index
merged_df = pd.concat([khaan, golomt, state, trans, xac], axis=1)

# Save to Excel
merged_df.to_excel('excels/all_bank_simple.xlsx', index=False)
