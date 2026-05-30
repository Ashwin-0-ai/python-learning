# prepare_bundeslaender

import pandas as pd 
df = pd.read_excel(
    r"D:\Mission_Blitzkreig\SnowFlake\data\02-bundeslaender.xlsx",
    sheet_name="Bundesländer_mit_Haupstädten",
    skiprows=2,
    header = None
)

# Manually setting the column name 
df.columns = ['state_name', 'area_km2', 'population_total', 'population_male','population_female', 'population_density']

# Keeping only the relevent rows 
df_states =df[df['state_name'].str.match(r'^\d{2}\s', na=False)].copy()

# Removing the prefixes from the state_name 
df_states['state_name'] = df_states['state_name'].str.replace(r'^\d{2}\s',' ', regex=True)

# Reset index
df_states = df_states.reset_index(drop=True)

print(df_states)
print(f"\nShape :{df_states.shape}")

# Save as CSV 
df_states.to_csv(r"D:\Mission_Blitzkreig\SnowFlake\data\02-bundeslaender.csv", index=False)

print("DataFrame saved as CSV successfully.")