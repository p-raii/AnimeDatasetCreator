import requests
import csv
import time
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
import threading
import random

def read_value(file_name):
    try:
        with open(file_name, "r") as file:
            return int(file.read().strip()) # Read and remove any surrounding whitespace
    except FileNotFoundError:
        return None  # Return None if the file doesn't exist

def update_value(filename, value):
    with open(filename, "w") as file:
        file.write(str(value))

file = open("final_staff11.csv", "a", encoding="UTF-8", newline="")
writer = csv.writer(file)
needed_staff = pd.read_csv("StaffNames.csv", names=["StaffName", "AnilistId"])
needed_staff_list = dict(zip(needed_staff["StaffName"], needed_staff["AnilistId"]))
needed_staff_names = set(needed_staff_list.keys())
page = read_value("page.txt")
user_file_no = 0
user_files = [
    "users.csv",
    "users1.csv",
    "users2.csv",
    "users3.csv",
    "users4.csv",
    "users5.csv",
    "users6.csv",
    "users7.csv",
]

lock = threading.Lock()
semaphore = threading.Semaphore(3)

def multi_print(string, variable=""):
    with lock:
        print(string, variable)


def save_unique_name(username):
    with lock:
        global user_files
        global user_file_no
        with open(user_files[user_file_no], "a", encoding="UTF-8", newline="") as f:
            csv_userNames_writer = csv.writer(f)
            csv_userNames_writer.writerow([username])
            f.flush()
        user_file_no = (user_file_no + 1) % 8


def save_unique_row(username, needed_staff_names_userList):
    writer.writerow(
        [
            username,
            (",").join(
                (
                    str(needed_staff_list[staff_name])
                    for staff_name in needed_staff_names_userList
                )
            ),
        ]
    )
    file.flush()


def get_user_favs(username):
    status = semaphore.acquire(blocking=False)
    if not status:
        semaphore.acquire()
        time.sleep(1)
    try:
        try:
            response = requests.get(
            f"https://api.jikan.moe/v4/users/{username}/favorites"
        ).json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error fetching page {page}: {e}. Retrying after 10 seconds...")
            time.sleep(10)
            return
        # response = requests.get(
        #     f"https://api.jikan.moe/v4/users/{username}/favorites"
        # ).json()
    finally:
        semaphore.release()
    return response


def save_user_favorites(username):
    global page
    global user_file_no
    global file
    save_unique_name(username)

    while True:
        multi_print("page:", page)
        multi_print(username)
        response = get_user_favs(username)
        if response== None:
            continue

        if "status" in response:
            if response["status"] == "429":
                multi_print("Rate limit hit. Waiting for 10 seconds...")
                time.sleep(10)
                continue
        if "data" not in response:
            multi_print("Data not present username. Waiting for 20 seconds...")
            seconds = random.randrange(7, 22)
            time.sleep(10)
            break
        favourites = response["data"]
        if favourites["people"]:
            staff_List = favourites["people"]
            staff_names = set()
            for staff in staff_List:
                staff_names.add(staff["name"])
            multi_print("staff_names", staff_names)
            needed_staff_names_userList = staff_names.intersection(needed_staff_names)
            multi_print("needed staff names", needed_staff_names_userList)
            if len(needed_staff_names_userList) > 3:
                save_unique_row(username, needed_staff_names_userList)
            break
        else:
            break


def main():
    global page
    global user_files

    page_iteration_count = 0
    while True:
        try:
            response = requests.get("https://api.jikan.moe/v4/users", {"page": page}, timeout=10).json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error fetching page {page}: {e}. Retrying after 10 seconds...")
            time.sleep(10)
            continue
        # response = requests.get("https://api.jikan.moe/v4/users", {"page": page}).json()

        if "status" in response:
            if response["status"] == "429":
                multi_print(response)
                multi_print("Rate limit hit. Waiting for 1 seconds...")
                time.sleep(1)
                continue
        if "data" not in response:
            multi_print("response")
            multi_print("Data not present page. Waiting for 1 seconds...")
            time.sleep(1)
            page += 1
            continue

        users = response["data"]
        userNames = {user["username"] for user in users}

        for f in user_files:
            users_list = pd.read_csv(f, names=["UserNames"], dtype=str)
            AllUserNames = set(users_list["UserNames"])
            userNames = userNames.difference(AllUserNames)
            del users_list

        if userNames:
            pool = ThreadPool(6)

            for name, thread in enumerate(pool._pool):
                thread.name = str(name)
            pool.map(save_user_favorites, userNames)
            pool.close()

        page_iteration_count += 1
        page += 1
        update_value("page.txt", page)


if __name__ == "__main__":
    main()
