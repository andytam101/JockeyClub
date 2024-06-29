from utilities import *
from sqlalchemy.exc import IntegrityError


def set_high_quality(raceId: int, high_quality=True):
    session = get_session()
    try:
        race_obj = session.query(Race).filter_by(id=raceId).one()
        race_obj.highQuality = high_quality
        session.commit()
        return True
    except IntegrityError as e:
        session.rollback()
        print(e)
        return False
    except Exception as e:
        session.rollback()
        print(e)
        return False


def set_fair(raceId: int, fair_type):
    if fair_type not in {"fair", "catch", "quick"}:
        return False

    session = get_session()
    try:
        race_obj = session.query(Race).filter_by(id=raceId).one()
        race_obj.fair = fair_type
        session.commit()
        return True
    except IntegrityError as e:
        session.rollback()
        print(e)
        return False
    except Exception as e:
        session.rollback()
        print(e)
        return False
