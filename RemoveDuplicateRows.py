import pandas as pd

# Load the CSV file
input_file = "1.17.csv"  # Replace with your file path
output_file = "union_output.csv"

# Read the CSV into a DataFrame
df = pd.read_csv(input_file)

# Perform a union by dropping duplicates based on the first column
unique_df = df.drop_duplicates(subset=df.columns[0])

# Save the result to a new CSV file
unique_df.to_csv(output_file, index=False)

print(f"Union result saved to {output_file}")
