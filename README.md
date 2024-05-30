# Introduction
A very basic tool to check your HKUST grade automatically & periodically. Data is crawled directly from SIS webpage.

Made of:
- `main_cli.py`: crawls grading data regularly and prints any output.
- `main.py`: one that extends above facility as a Telegram chatbot.
  - One is able to:
    -  check / modify semester to check
    -  check / change crawling duration
    -  check current grading / recrawl the data 
  - requires modification of `utils.py` (i.e. bot & user info) to be executed

## Limitations
As of current stage, the program requires the user's login & authorization whenever you start the program. It may be solved if it is integrated into an application with an actual API from the University. 
