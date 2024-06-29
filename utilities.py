from db import Ran, Horse, Race, get_session


CURRENT_SEASON = 2024


def get_url(raceId: int) -> str:
    session = get_session()
    ans = session.query(Race.url).filter(Race.id == raceId).scalar()
    session.close()
    return ans


def get_name_of_horse(code: str) -> str:
    session = get_session()
    ans = session.query(Horse.name).filter(Horse.id == code).scalar()
    session.close()
    return ans


def get_code_of_horse(name: str) -> str:
    session = get_session()
    ans = session.query(Horse.id).filter(Horse.name == name).scalar()
    session.close()
    return ans


def get_ranking(raceId: int, horse: str) -> int:
    session = get_session()
    ans: int = (
        session.query(Ran.ranking)
        .filter(Ran.raceId == raceId)
        .filter(Ran.horseId == horse)
        .scalar()
    )
    session.close()
    return ans


def get_races_by_horse(code) -> [int]:
    session = get_session()
    ans = session.query(Ran.raceId).filter(Ran.horseId == code).all()
    session.close()
    return list(map(lambda x: x[0], ans))


def format_race(raceId) -> (str, bool):
    race_obj = get_race_obj(raceId)
    displayId = str(raceId)
    if race_obj.fair == "catch":
        # 後上
        displayId += "*"
    elif race_obj.fair == "quick":
        # 快放
        displayId += "^"

    return displayId, race_obj.highQuality


def get_race_obj(raceId):
    session = get_session()
    race_obj = session.query(Race).filter(Race.id == raceId).one()
    session.close()
    return race_obj


def get_horse_obj(horseId):
    session = get_session()
    horse_obj = session.query(Horse).filter(Horse.id == horseId).one()
    session.close()
    return horse_obj


def race_exist(raceId):
    session = get_session()
    result = session.query(Race).filter(Race.id == raceId).first()
    session.close()
    return result is not None


def horse_exist(horseId):
    session = get_session()
    result = session.query(Horse).filter(Horse.id == horseId).first()
    session.close()
    print(result.name)
    return result is not None


if __name__ == "__main__":
    print(get_name_of_horse("E194"))
    print(get_code_of_horse("符號"))
    print(get_races_by_horse("E194"))
    print(format_race(627))
    print(get_url(627))
