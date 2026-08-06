from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_weather_message(county_id: str = "C66") -> str:
    url = "https://www.cwa.gov.tw/V8/C/"

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    driver.find_element(By.ID, "C66").click()


    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    patch= soup.select_one(".weather-loc")
    site=patch.select_one(".county-name").get_text()
    time=patch.select_one(".datetime").get_text()
    low=patch.select_one(".low").get_text()
    height=patch.select_one(".height").get_text()
    cc="-".join([low,height])
    rain=patch.select_one(".rain").get_text()
    message = "\n".join([
        site,
        time,
        cc,
        rain
    ])
    driver.close()
    return message
