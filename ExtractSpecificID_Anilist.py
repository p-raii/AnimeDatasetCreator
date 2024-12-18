import requests
import csv
import time

# Function to fetch user favorites
def fetch_user_favorites(user_id):
    url = "https://graphql.anilist.co"
    query = """
    query($id: Int) {
        User(id: $id) {
            favourites {
                anime {
                    nodes {
                        id
                    }
                }
            }
        }
    }
    """
    variables = {"id": user_id}
    try:
        response = requests.post(url, json={"query": query, "variables": variables})
        response.raise_for_status()
        data = response.json()
        return [anime["id"] for anime in data["data"]["User"]["favourites"]["anime"]["nodes"]]
    except Exception as e:
        print(f"Error fetching data for user ID {user_id}: {e}")
        return []

# Load user IDs from CSV
input_csv = "again_rare_in10.csv"  # Replace with the path to your CSV file
output_csv = "rare_extract11.csv"  # Output file path

user_ids = []
with open(input_csv, "r") as file:
    reader = csv.reader(file)
    user_ids = [row[0] for row in reader]  # Assumes one user ID per row

# Prepare data for output
result_data = []

# Fetch favorites for each user
for idx, user_id in enumerate(user_ids):
    print(f"Fetching favorites for user ID {user_id} ({idx + 1}/{len(user_ids)})...")
    favorites = fetch_user_favorites(user_id)
    result_data.append((user_id, ",".join(map(str, favorites))))
    time.sleep(1)  # Avoid rate limiting

# Save results to CSV
with open(output_csv, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["user_id", "favorites"])  # Header
    writer.writerows(result_data)

print(f"Favorites data saved to '{output_csv}'.")
