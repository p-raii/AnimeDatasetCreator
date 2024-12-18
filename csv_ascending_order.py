import pandas as pd

# Load the CSV file without headers
csv_file = "anilist_all_data.csv"  # Replace with your file's path

# Read the CSV file into a DataFrame without headers
df = pd.read_csv(csv_file, header=None)

# Sort the DataFrame by the first column (column 0) in ascending order
sorted_df = df.sort_values(by=0, ascending=True)

# Save the sorted DataFrame to a new CSV file
sorted_df.to_csv("anilist_data.csv", index=False, header=False)

print("Data sorted successfully into 'mal_anime_list_sorted.csv'")
