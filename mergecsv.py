import pandas as pd

# Load the two CSV files
csv_file1 = "anilist_anime_list.csv"  # Replace with your first file's path
csv_file2 = "final_rare.csv"  # Replace with your second file's path

# Read the CSV files into DataFrames
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)

# Merge the two DataFrames
# By default, this combines them row-wise (like stacking one file on top of the other)
merged_df = pd.concat([df1, df2], ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv("final.csv", index=False)

print("CSV files merged successfully into 'final_rare.csv'")
