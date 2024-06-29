from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW


def scrape(url: str) -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")

    service = ChromeService()
    service.creation_flags = CREATE_NO_WINDOW

    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(2)

    driver.get(url)
    return driver
