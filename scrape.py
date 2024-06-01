from selenium import webdriver


def scrape(url: str) -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)

    driver.get(url)
    return driver

