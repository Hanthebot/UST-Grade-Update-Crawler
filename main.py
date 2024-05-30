import time
import telepot
from telepot.loop import MessageLoop

from util import load_userData, load_manifest, save_userData, print_grade
from util_crawl import Crawler
import time

commands = {
    "help": "Show available commands: help",
    "refresh_grade": "Refresh grade: refresh_grade",
    "my_grade": "Show my grade: my_grade",
    "share_bot": "Share bot: share_bot",
    "change_sem": "Change semester preference: change_sem 2023-24 Spring",
    "check_sem": "Check semester preference: check_sem",
    "change_duration": "Change duration (in seconds): change_duration 3600",
    "check_duration": "Check duration: check_duration",
    "terminate": "Terminate the program: terminate"
    }

def handle_msg(chat_id, command, msg):
    if command == "help":
        bot.sendMessage(chat_id, "Available commands:\n" + ", ".join(commands.keys()))
    elif command == "refresh_grade":
        userData["data"] = crawler.crawl_data()
        bot.sendMessage(chat_id, print_grade(userData))
    elif command == "my_grade":
        bot.sendMessage(chat_id, print_grade(userData))
    elif command == "share_bot":
        bot.sendMessage(chat_id, "https://t.me/" + manifest["bot_id"])
    elif command == "change_sem":
        userData["semPreference"] = " ".join(msg.split(" ")[1:]) if len(msg.split(" ")) > 1 else "2023-24 Spring"
        save_userData(userData)
        bot.sendMessage(chat_id, "Semester preference changed to " + msg.split(" ")[1])
    elif command == "check_sem":
        bot.sendMessage(chat_id, "Semester preference is " + userData["semPreference"])
    elif command == "check_duration":
        bot.sendMessage(chat_id, "Duration is " + str(userData["duration"]))
    elif command == "change_duration":
        if len(msg.split(" ")) < 2:
            bot.sendMessage(chat_id, "Please specify the duration in seconds")
            return
        userData["duration"] = int(msg.split(" ")[1])
        save_userData(userData)
        bot.sendMessage(chat_id, f"Duration is f{userData['duration']}")
    elif command == "terminate":
        bot.sendMessage(chat_id, "Bye")
        exit()

def handle(msg):
    content_type, _, chat_id = telepot.glance(msg)
    if content_type != "text" or chat_id != manifest["owner"]:
        return
    command = msg["text"].split(" ")[0].lower()
    if command in commands:
        handle_msg(chat_id, command, msg["text"])
    else:
        bot.sendMessage(chat_id, "No such command, try 'help'")

if __name__ == "__main__":
    manifest = load_manifest()
    userData = load_userData()
    
    if userData["firstTime"]:
        sec = input("Please enter the duration of the program (in seconds): ")
        userData["duration"] = int(sec) if sec != "" else 1800
        inp = input("Please enter your semester preference (e.g. 2023-24 Spring): ")
        userData["semPreference"] = inp if inp != "" else "2023-24 Spring"
        userData["firstTime"] = False
    
    save_userData(userData)
    
    crawler = Crawler()

    input("please login and press enter to continue...")

    prev = userData["data"].copy()

    firstTime = True
    bot = telepot.Bot(token=manifest["bot_token"])
    MessageLoop(bot, handle).run_as_thread()
    print("Running...")

    while True:
        if time.time() % userData["duration"] >= userData["duration"]*0.1 and not firstTime:
            time.sleep(userData["duration"]*0.08)
            continue

        userData["data"] = crawler.crawl_data()
        # save if there is any change
        if (prev != userData["data"]):
            save_userData(userData)
        # if there is a difference, send a message
        for code, info in userData["data"].items():
            if userData["semPreference"] not in ["", info[0]] or \
                info[1] == prev.get(code, "  ")[1]:
                continue
            else: # grade changed
                msg = "[{}] \nSubject: {} \n{} -> {}".format(\
                        time.strftime('%Y-%m-%d %H:%M:%S'), code, prev.get(code, "  "), info[1]
                        )
                bot.sendMessage(manifest["owner"], msg)
                print(msg)
        prev = userData["data"].copy()
        if firstTime:
            firstTime = False
        time.sleep(userData["duration"]*0.1)