from utilities import *
from scrape import scrape
from selenium.webdriver.common.by import By


def scrape_compete(url: str):
    driver = scrape(url)
    table = driver.find_elements(By.CSS_SELECTOR, 'table')[4]
    names = table.find_elements(By.CSS_SELECTOR, 'td:nth-child(4)')[1:]

    horses = list(map(lambda x: x.text, names))
    result = {
        "table": build_table(horses),
    }
    result.update(get_every_two_data(horses))
    return result


def build_table(horses):
    # horses as a list of names (not ids)
    n = len(horses)
    result = [["#"] + [h for h in horses]]
    for i in range(n):
        result.append([horses[i]])
        for j in range(n):
            if i != j:
                i_code = get_code_of_horse(horses[i])
                j_code = get_code_of_horse(horses[j])
                if i_code is not None and j_code is not None:
                    result[-1].append(str(count_two_versus(i_code, j_code)))
                else:
                    result[-1].append("0")
            else:
                result[-1].append("")

    return result


def get_intersection(h1, h2):
    return set(get_races_by_horse(h1)) & set(get_races_by_horse(h2))


def count_two_versus(h1, h2):
    return len(get_intersection(h1, h2))


def get_two_versus_data(h1, h2) -> list[dict]:
    intersection = get_intersection(h1, h2)
    results = []
    for i in intersection:
        displayId, high_quality = format_race(i)
        results.append({"id": displayId, "h1": get_ranking(i, h1),
                        "h2": get_ranking(i, h2), "highQuality": high_quality, "url": get_race_obj(i).url})
    return results


def get_every_two_data(horses):
    n = len(horses)
    result = {}
    for i in range(n):
        for j in range(i + 1, n):
            i_code = get_code_of_horse(horses[i])
            j_code = get_code_of_horse(horses[j])
            result.update({f"{horses[i]}, {horses[j]}": get_two_versus_data(i_code, j_code)})
            result.update({f"{horses[j]}, {horses[i]}": get_two_versus_data(j_code, i_code)})
    return result


if __name__ == "__main__":
    print(scrape_compete("https://racing.hkjc.com/racing/information/Chinese/racing/RaceCard.aspx"))
