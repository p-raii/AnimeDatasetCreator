import pandas as pd

def extract_user_and_anime_ids(input_file, output_file):
    # Load the CSV
    df = pd.read_csv(input_file)

    # Select only the 'User ID' and 'Anime ID' columns
    filtered_df = df[['User ID', 'Anime ID']]

    # Save the filtered data to a new CSV file
    filtered_df.to_csv(output_file, index=False)

# Example usage:
input_csv = 'first_one.csv'  # Replace with your input CSV file
output_csv = 'first_one1.csv'  # Replace with your desired output CSV file
extract_user_and_anime_ids(input_csv, output_csv)
