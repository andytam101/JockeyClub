"""Used to restore the contents of the database"""


from store import scrape_all_on_date, add_race


def scrape_all_dates(info):
    result = []
    for date, location, total_count in info:
        print(f"Fetching day {date}...")
        result += scrape_all_on_date(date, location, total_count)
        print("======================")
    return result


dates = [
    ("2024/05/29", "ST", 8),
    # ("2024/05/26", "ST", 10),
    # ("2024/05/22", "HV", 9),
    # ("2024/05/19", "ST", 10),
    # ("2024/05/15", "HV", 9),
    # ("2024/05/11", "ST", 10),
    # ("2024/05/08", "HV", 9),
    # ("2024/05/05", "ST", 11),
    # ("2024/05/01", "HV", 9)
]

if __name__ == "__main__":
    data = scrape_all_dates(dates)
    for d in data:
        add_race(d["raceId"], d["distance"], d["url"], d["results"])
