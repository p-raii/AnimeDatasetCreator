import pandas as pd

# Load your CSV file into a DataFrame
df = pd.read_csv('rare_extract11.csv')

# Filter out rows where 'favorites' is null or empty
filtered_df = df[~df['favorites'].isnull() & (df['favorites'].str.strip() != '')]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('output_rare11.csv', index=False)
