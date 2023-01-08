import pandas as pd
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '1Os1HEFrAv91SYUqafeYoV1P3lt4s0QtNvtp2RabydnY'



PATH = "C:\Program Files\chromedriver.exe"

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="sheet1!A2:A243").execute()
values = result.get('values', )

final_list = []
for value in values:
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.google.com/")

    input = driver.find_element(By.CLASS_NAME, "gLFyf")
    input.send_keys(f"{value[0]} t20 stats cricketer espncricinfo")
    input.send_keys(Keys.ENTER)

    first_link = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a/h3[contains(text(), "profile and biography")]')
    first_link[0].click()


    t20_stats = driver.find_elements(By.XPATH, "//tbody/tr/td/span[text()='T20']/parent::node()/following-sibling::node()/span")

    batting_stats = []
    bowling_stats = []
    title = driver.find_elements(By.XPATH, '//span[contains(text(), "Career Averages")]/parent::node()/parent::node()/following-sibling::node()/div/h5')

    if title[0].text == "Batting & Fielding":
        for i in t20_stats[:15]:
            batting_stats.append(i.get_attribute('textContent'))
        for i in t20_stats[15:]:
            bowling_stats.append(i.get_attribute('textContent'))

    else:
        for i in t20_stats[:13]:
            bowling_stats.append(i.get_attribute('textContent'))
        for i in t20_stats[13:]:
            batting_stats.append(i.get_attribute('textContent'))

    final_list = [batting_stats + bowling_stats]
    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="sheet2!A1:AA1", 
                                valueInputOption="USER_ENTERED",
                                insertDataOption="INSERT_ROWS",
                                body={"values":final_list}).execute()


    driver.quit()

# request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
#                                 range="sheet1!E2", 
#                                 valueInputOption="USER_ENTERED", 
#                                 body={"values":final_list}).execute()

