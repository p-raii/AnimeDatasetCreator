import pandas as pd

# Load your CSV file
input_file = "first_one1.csv"  # Replace with your actual file path
output_file = "demo.csv"

# Read the CSV into a DataFrame
df = pd.read_csv(input_file)

# Group by 'userId' and aggregate 'aniId' into a list
grouped_df = df.groupby("User ID")["Anime ID"].apply(list).reset_index()

# (Optional) Convert the list of aniId into a comma-separated string
grouped_df["Anime ID"] = grouped_df["Anime ID"].apply(lambda x: ", ".join(map(str, x)))

# Save the result to a new CSV file
grouped_df.to_csv(output_file, index=False)

print(f"File merged successfully! Saved to {output_file}")
