from utilities import *
from scrape import scrape
from selenium.webdriver.common.by import By
from sqlalchemy.exc import IntegrityError


def separate_name_code(name_code: str) -> (str, str):
    name, code = name_code.split(" ")
    code = code[1:-1]
    return name, code


def details_of_race(details) -> dict:
    rows = details.find_elements(By.CSS_SELECTOR, 'tr')
    cell1 = rows[0].find_element(By.CSS_SELECTOR, 'td')
    cell2 = rows[2].find_element(By.CSS_SELECTOR, 'td')

    return {
        "raceId": get_race_id(cell1),
        "distance": get_distance(cell2)
    }


def get_race_id(cell) -> str:
    return cell.text.split(" ")[-1][1:-1]


def get_distance(cell) -> str:
    return cell.text.split(" - ")[1][:-1]


def parse_table(horses) -> [dict]:
    result = []
    names = horses.find_elements(By.CSS_SELECTOR, 'td:nth-child(3)')[1:]
    ranking = horses.find_elements(By.CSS_SELECTOR, 'td:nth-child(1)')[1:]
    n = len(names)
    for i in range(n):
        name, code = separate_name_code(names[i].text)
        result.append({
            "name": name,
            "code": code,
            "ranking": ranking[i].text
        })
    return result


def scrape_race(url: str) -> dict:
    for i in range(MAX_TRIES):
        try:
            driver = scrape(url)

            tables = driver.find_elements(By.CSS_SELECTOR, 'table')
            details = tables[1]
            horses = tables[2]

            result = parse_table(horses)
            details = details_of_race(details)

            driver.quit()

            details.update({"url": url})
            details.update({"results": result})
            return details
        except IndexError:
            print("Failed, trying again automatically")


def scrape_all(urls: [str], lang=0) -> [dict]:
    result = []
    for (idx, url) in enumerate(urls):
        if lang == 0:
            print(f"Fetching race {idx + 1}...")
        else:
            print(f"正在下載第 {idx + 1} 場資料...")
        result.append(scrape_race(url))

    return result


def generate_urls(date, location, total_count):
    urls = []
    base = f"https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx?RaceDate={date}&Racecourse={location}&RaceNo="
    for i in range(1, total_count + 1):
        urls.append(base + str(i))
    return urls


def scrape_all_on_date(date, location, total_count, lang=0):
    return scrape_all(generate_urls(date, location, total_count), lang)


def add_all_data(data, lang=0):
    for i, d in enumerate(data):
        if lang == 0:
            print(f"Storing race {i + 1}...")
        else:
            print(f"正在儲存第 {i+1} 場資料...")
        add_race(d["raceId"], d["distance"], d["url"], d["results"])


def add_race(raceId, distance, url, horses):
    session = get_session()
    try:
        if not race_exist(raceId):
            new_race = Race(id=raceId, season=CURRENT_SEASON, distance=distance, url=url)
            session.add(new_race)

        for h in horses:
            add_horse(h["code"], h["name"])
            new_ran = Ran(raceId=raceId, horseId=h["code"], ranking=h["ranking"])
            session.add(new_ran)

        session.commit()
    except IntegrityError as e:
        session.rollback()
        print("Already exists in database")
    except Exception as e:
        session.rollback()
        raise e


def add_horse(horseId, name):
    if not horse_exist(horseId):
        session = get_session()
        new_horse = Horse(id=horseId, name=name)
        session.add(new_horse)
        session.commit()
        return
