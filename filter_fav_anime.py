import pandas as pd

# Load the CSV file
input_file = "updated_user_data.csv"  # Replace with your file path
output_file = "final_anidata.csv"

# Read the CSV into a DataFrame
df = pd.read_csv(input_file)

# Define a function to count the number of Anime IDs in a row
def count_anime_ids(anime_ids):
    return len(str(anime_ids).split(","))  # Split by ", " to count IDs

# Filter the rows where the number of Anime IDs is 5 or more
filtered_df = df[df["Favourites"].apply(count_anime_ids) >= 5]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv(output_file, index=False)

print(f"Filtered data saved to {output_file}")
