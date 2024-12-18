import requests
import csv
import time
import pandas as pd
# GraphQL endpoint
url = "https://graphql.anilist.co"

# GraphQL query
query = '''
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    users {
      id
      favourites {
        anime {
          nodes {
            id
          }
        }
      }
    }
  }
}
'''

def fetch_users_from_id(total_users, csv_filename):
    page = 34518
    per_page = 50
    unique_rows = set()
    unique_anime_ids = pd.DataFrame(columns=["anime_id"])

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User ID", "Anime ID"])

        while len(unique_rows) < total_users:
            variables = {
                "page": page,
                "perPage": per_page
            }

            response = requests.post(url, json={"query": query, "variables": variables})

            # Handle rate limit
            if response.status_code == 429:
                print("Rate limit hit. Waiting for 60 seconds...")
                time.sleep(10)
                continue
            if response.status_code != 200:
                print(f"Error: HTTP {response.status_code} - {response.text}")
                print(page)
                page += 1
                continue
            
            # Parse response
            try:
                data = response.json()
            except ValueError:
                print("Error: Failed to parse JSON")
                break

            # Validate API response
            if data and "data" in data and "Page" in data["data"] and "users" in data["data"]["Page"]:
                users = data["data"]["Page"]["users"]

                for user in users:
                    user_id = user["id"]

                    # Process only users with ID >= start_user_id
                    
                    if "favourites" in user and "anime" in user["favourites"]:
                        for anime in user["favourites"]["anime"]["nodes"]:
                          anime_id = anime["id"]

                        

                          unique_row = (user_id, anime_id)
                          if unique_row not in unique_rows:
                            unique_rows.add(unique_row)
                            writer.writerow([user_id, anime_id])

                page += 1
            else:
                print("Unexpected API response structure:", data)
                break
    print(page)

# Fetch users starting from a specific user ID
fetch_users_from_id(total_users=50, csv_filename="try.csv")
