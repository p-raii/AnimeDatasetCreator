import pandas as pd

# Load the CSV data
input_csv = "rare_extract.csv"  # Replace with your CSV file path
output_csv = "filter_rare.csv"  # Output file path

# Read the CSV into a DataFrame
df = pd.read_csv(input_csv)

# Filter rows where the 'favorites' column is empty or null
# filtered_df = df[df['favorites'].isnull() | (df['favorites'].str.strip() == '')]
filtered_df = df[~df['favorites'].isnull() & (df['favorites'].str.strip() != '')]


# Keep only the 'user_id' column
filtered_user_ids = filtered_df[['user_id']]

# Save the filtered user IDs to a new CSV
filtered_user_ids.to_csv(output_csv, index=False)

print(f"Filtered data saved to '{output_csv}'.")
