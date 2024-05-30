import time

from util import load_userData, save_userData
from util_crawl import Crawler
import time

if __name__ == "__main__":
    # Disable Selenium output

    userData = load_userData()
    
    crawler = Crawler()

    input("please login and press enter to continue...")

    prev = userData["data"].copy()

    print("Running...")

    firstTime = True
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
                        time.strftime('%Y-%m-%d %H:%M:%S'), code, prev.get(code, "  ")[1], info[1]
                        )
                print(msg)
        prev = userData["data"].copy()
        if firstTime:
            firstTime = False
        time.sleep(userData["duration"]*0.1)