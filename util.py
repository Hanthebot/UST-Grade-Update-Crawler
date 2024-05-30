import json
import os

def save_userData(userData):
    with open("userData.json", "w", encoding = "utf-8") as file:
        json.dump(userData, file, indent=4)

def load_manifest():
    if not os.path.exists("manifest.json"):
        # Set default value if data.json does not exist
        # CHANGE the data below accordingly
        manifest = {
            "bot_token": "", #<telegram-bot-token:string>
            "bot_id": "", #<telegram-bot-id:string>
            "owner": 0 #<owner-id:int>
        }
        print("Creating manifest.json...")
        # Load data from manifest.json
        with open("manifest.json", "w", encoding = "utf-8") as file:
            json.dump(manifest, file, indent=4)
    else:
        # Load data from data.json
        with open("manifest.json", "r", encoding = "utf-8") as file:
            manifest = json.load(file)
    return manifest

def load_userData():
    # Check whether data.json exists
    if not os.path.exists("userData.json"):
        # Set default value if data.json does not exist
        userData = {
            "firstTime": True,
            "semPreference": "2023-24 Spring",
            "duration": 1800,
            "data": {
                "COMP2211": "A++"
            }
        }
        print("Creating userData.json...")
        # Load data from data.json
        save_userData(userData)
    else:
        # Load data from data.json
        with open("userData.json", "r", encoding = "utf-8") as file:
            userData = json.load(file)
    return userData

def print_grade(userData:object):
    lis = []
    for code, info in userData["data"].items():
        if userData["semPreference"] not in ["", info[0]]:
            continue
        else: # grade changed
            lis.append(f"Subject: {code}: {info[1]}")
    return "\n".join(lis)