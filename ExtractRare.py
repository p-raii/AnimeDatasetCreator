import requests
import csv
import time
import pandas as pd

# GraphQL endpoint
url = "https://graphql.anilist.co"
df = pd.read_csv("Less_Than_100.csv")
rare_dict = dict(zip(df["anime"], df["appear"]))

# GraphQL query
query = """
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
"""


def fetch_users_from_id(desired_id, csv_filename):
    page = 55923
    per_page = 50

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User ID"])
        file.flush()

        while 1:
            variables = {"page": page, "perPage": per_page}

            response = requests.post(url, json={"query": query, "variables": variables})
            

            # Handle rate limit
            if response.status_code == 429:
                print("Rate limit hit. Waiting for 60 seconds...")
                time.sleep(20)
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
            if (
                data
                and "data" in data
                and "Page" in data["data"]
                and "users" in data["data"]["Page"]
            ):
                users = data["data"]["Page"]["users"]


                for user in users:
                    user_id = user["id"]
                    # change to sets
                    # fav_animes = set(user["favourites"]["anime"]["nodes"])
                    fav_animes = {node["id"] for node in user["favourites"]["anime"]["nodes"]}
                    all_needed_animes = set(rare_dict.keys())
                    #taking the common animes
                    anime_needed_in_userList = fav_animes.intersection(all_needed_animes)
                    # checking to see if anime_needed_in_userlist is empty
                    if anime_needed_in_userList:
                        writer.writerow([user_id])
                        file.flush()
                        
                        for anime in anime_needed_in_userList:
                            rare_dict[anime] += 1
                            if rare_dict[anime] == 100:
                                rare_dict.pop(anime)
                if(user["id"]>=desired_id):
                    break
                page += 1
            else:
                print("Unexpected API response structure:", data)
                break
    print(page)
    #new rarefile
    with open("newrare.csv", mode="w", newline="") as file:
      writerr = csv.writer(file)
      file.flush()

      # Write headers
      writerr.writerow(["Anime", "Appear"]) 
      for key, value in rare_dict.items():  # Iterate through key-value pairs
          writerr.writerow([key, value])
          file.flush()



# Fetch users starting from a specific user ID
fetch_users_from_id(desired_id=7500000, csv_filename="rare_user6.csv")
