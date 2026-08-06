from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def create_driver() -> webdriver.Chrome:
    """建立適用於本機與 GitHub Actions 的 Chrome 瀏覽器。"""

    options = Options()

    # GitHub Actions 沒有圖形桌面，必須使用無頭模式
    options.add_argument("--headless=new")

    # Linux 與容器環境常用設定
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 設定無頭瀏覽器畫面大小
    options.add_argument("--window-size=1920,1080")

    options.add_argument(
        "--user-agent=Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )

    return webdriver.Chrome(options=options)


def get_weather_message(county_id: str = "C66") -> str:
    """
    取得中央氣象署指定縣市的天氣資訊。

    county_id 範例：
    C66：臺中市
    """

    url = "https://www.cwa.gov.tw/V8/C/"
    driver = create_driver()

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 20)

        # 等待指定縣市按鈕可以點擊
        county_button = wait.until(
            EC.element_to_be_clickable((By.ID, county_id))
        )

        county_button.click()

        # 等待天氣區塊出現在網頁中
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".weather-loc")
            )
        )

        # 等待點擊後的資料載入
        wait.until(
            lambda current_driver: current_driver.find_element(
                By.CSS_SELECTOR,
                ".weather-loc .county-name",
            ).text.strip() != ""
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        weather_block = soup.select_one(".weather-loc")

        if weather_block is None:
            raise ValueError("找不到 .weather-loc 天氣資料區塊")

        site_element = weather_block.select_one(".county-name")
        time_element = weather_block.select_one(".time")
        low_element = weather_block.select_one(".low")
        high_element = weather_block.select_one(".height")
        rain_element = weather_block.select_one(".rain")

        elements = {
            "縣市": site_element,
            "時間": time_element,
            "最低溫": low_element,
            "最高溫": high_element,
            "降雨機率": rain_element,
        }

        missing_elements = [
            name
            for name, element in elements.items()
            if element is None
        ]

        if missing_elements:
            raise ValueError(
                "找不到以下天氣欄位："
                + "、".join(missing_elements)
            )

        site = site_element.get_text(strip=True)
        weather_time = time_element.get_text(strip=True)
        low = low_element.get_text(strip=True)
        high = high_element.get_text(strip=True)
        rain = rain_element.get_text(strip=True)

        temperature = f"{low}-{high}"

        message = "\n".join(
            [
                site,
                weather_time,
                temperature,
                rain,
            ]
        )

        return message

    finally:
        # 即使發生錯誤，也完整關閉 Chrome
        driver.quit()
