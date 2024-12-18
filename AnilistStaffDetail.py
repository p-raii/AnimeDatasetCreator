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
      name
      favourites {
        staff {
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
    page = 800
    per_page = 50
    unique_rows = set()

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User ID", "Staff ID"])

        while len(unique_rows) < total_users:
            variables = {
                "page": page,
                "perPage": per_page
            }

            response = requests.post(url, json={"query": query, "variables": variables})

            # Handle rate limit
            if response.status_code == 429:
                print("Rate limit hit. Waiting for 60 seconds...")
                time.sleep(60)
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
                    
                    if "favourites" in user and "staff" in user["favourites"]:
                        for staff in user["favourites"]["staff"]["nodes"]:
                            staff_id = staff["id"]

                            unique_row = (user_id, staff_id)
                            if unique_row not in unique_rows:
                                unique_rows.add(unique_row)
                                writer.writerow([user_id,staff_id])

                page += 1
            else:
                print("Unexpected API response structure:", data)
                break
    print(page)

# Fetch users starting from a specific user ID
fetch_users_from_id(total_users=1000000, csv_filename="users_favourite1.csv")
