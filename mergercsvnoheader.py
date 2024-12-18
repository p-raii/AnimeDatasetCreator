import pandas as pd

# Load the two CSV files without headers
csv_file1 = "1.17.csv"  # Replace with your first file's path
csv_file2 = "mal_anime_list.csv"  # Replace with your second file's path

# Read the CSV files into DataFrames without headers
df1 = pd.read_csv(csv_file1, header=None)
df2 = pd.read_csv(csv_file2, header=None)

# Merge the two DataFrames row-wise
merged_df = pd.concat([df1, df2], ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv("1.17.csv", index=False, header=False)

print("CSV files merged successfully into 'mal_anime_list4.csv'")
