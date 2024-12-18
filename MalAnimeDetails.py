import requests
import csv
import time
import pandas as pd

file = open("anime_list5.csv", "w", encoding="UTF-8", newline="")
writer = csv.writer(file)
needed_anime = pd.read_csv(
    "Top_1000_List_with_num_fav.csv",
    names=["MalId", "AnilistId", "MalFavs", "AniFavs"],
    dtype=int,
)
needed_anime_list = dict(zip(needed_anime["MalId"], needed_anime["AnilistId"]))
needed_anime_mal_ids = set(needed_anime_list.keys())


page = 355783
while True:
    response = requests.get("https://api.jikan.moe/v4/users", {"page": page}).json()

    if "status" in response:
        if response["status"] == "429":
            print("Rate limit hit. Waiting for 10 seconds...")
            time.sleep(10)
            continue
    if "data" not in response:
        print("Data not present page. Waiting for 10 seconds...")
        time.sleep(10)
        page += 1
        continue

    users = response["data"]
    limit = len(users)
    index = 0
    while True:
        print("page no:", page)
        user = users[index]
        username = user["username"]
        print(username)
        response = requests.get(
            f"https://api.jikan.moe/v4/users/{username}/favorites"
        ).json()

        if "status" in response:
            if response["status"] == "429":
                print("Rate limit hit. Waiting for 10 seconds...")
                time.sleep(10)
                continue
        if "data" not in response:
            print("Data not present username. Waiting for 10 seconds...")
            time.sleep(10)
            break
        favourites = response["data"]
        if favourites["anime"]:
            anime_list = favourites["anime"]
            anime_mal_ids = set()
            for anime in anime_list:
                anime_mal_ids.add(anime["mal_id"])
            print("anime_mal_ids", anime_mal_ids)
            needed_anime_ids_userList = anime_mal_ids.intersection(needed_anime_mal_ids)
            print("needed_anime_ids_userList", needed_anime_ids_userList)
            if len(needed_anime_ids_userList) > 5:
                writer.writerow(
                    [
                        username,
                        (",").join(
                            (
                                str(needed_anime_list[mal_id])
                                for mal_id in needed_anime_ids_userList
                            )
                        ),
                    ]
                )
                file.flush()

        index += 1
        if index >= limit:
            break
    page += 1
    if page == 300000:
        break
