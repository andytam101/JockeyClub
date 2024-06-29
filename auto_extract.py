from scrape import scrape
from datetime import datetime
from selenium.webdriver.common.by import By
from store import scrape_all_on_date, add_all_data


URL = "https://racing.hkjc.com/racing/information/Chinese/racing/LocalResults.aspx"


def translate_location(location: str):
    if location == "沙田":
        return "ST"
    else:
        return "HV"


def parse_date_location(date_location: str):
    date_str, location_chin = date_location.split()[1:]
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    formatted_date_str = date_obj.strftime("%Y/%m/%d")
    return formatted_date_str, translate_location(location_chin)


def detect_info(url):
    driver = scrape(url)
    date, location = parse_date_location(
        driver.find_element(By.CLASS_NAME, "raceMeeting_select").find_element(By.CLASS_NAME, "f_fs13").text)

    race_count_row = driver.find_element(By.CLASS_NAME, "js_racecard").find_element(By.CSS_SELECTOR, "tr")
    race_count = len(race_count_row.find_elements(By.CSS_SELECTOR, "img")) - 1
    return date, location, race_count


if __name__ == "__main__":
    print("正在閱取資料...")
    try:
        g_date, g_location, g_race_count = detect_info(URL)
        print(f"日期: {g_date}")
        print(f"場地: {g_location}")
        print(f"場數: {g_race_count}")
        input("按鍵 Enter 繼續")
        print("=================================")
        result = scrape_all_on_date(g_date, g_location, g_race_count, lang=1)
        print("=================================")
        add_all_data(result, lang=1)
        print()
        input("成功！請按 Enter 完成")
    except Exception as e:
        print(e)
        input("下載失敗！請按 Enter 完成")
