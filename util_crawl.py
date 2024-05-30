import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Crawler:
    defaultURL = f"https://sisprod.psft.ust.hk/psc/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_MY_ACAD.GBL?Page=SSS_MY_ACAD&Action=U"
    buttonId = "DERIVED_SSSACA2_SSS_ACAD_HISTORY"
    tableId = "CRSE_HIST$scroll$0"
    
    def __init__(self):
        
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(Crawler.defaultURL)

    def move_page(self):
        btn_academics = self.driver.find_element(By.ID, Crawler.buttonId)
        btn_academics.click()

    def extract_data(self)->object:
        soup = bs(self.driver.page_source, "html.parser")
        table = soup.find("table", {"id":Crawler.tableId})
        rows = table.select("tr")[1:]
        keyRow = lambda row: row.select_one("td:nth-child(1)").text.replace("\n","") 
        semRow = lambda row: row.select_one("td:nth-child(3)").text.replace("\n","")
        gradeRow = lambda row: row.select_one("td:nth-child(4)").text.replace("\n","")
        data = {
            keyRow(row): [
            semRow(row),
            gradeRow(row)
            ]
            
            for row in rows
        }
        return data

    def crawl_data(self):
        self.driver.refresh()
        if self.driver.find_elements(By.ID, Crawler.tableId) == []:
            self.driver.get(Crawler.defaultURL)
            time.sleep(3)
            self.move_page()
        
        while self.driver.find_elements(By.ID, Crawler.tableId) == []:
            time.sleep(0.3)
        return self.extract_data()