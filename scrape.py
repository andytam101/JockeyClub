from selenium import webdriver


def scrape(url: str) -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)

    driver.get(url)
    return driver
