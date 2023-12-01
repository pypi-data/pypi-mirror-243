from datetime import datetime, timedelta, timezone

GMT_STRING = "%a, %d %b %Y %H:%M:%S GMT"


def get_gmt_now() -> str:
    return datetime.now(tz=timezone.utc).strftime(GMT_STRING)


def parse_gmt(date_string: str) -> datetime:
    return datetime.strptime(date_string, GMT_STRING).replace(tzinfo=timezone.utc)


def check_max_offset_now(dt: datetime, minutes: int = 5) -> bool:
    now = datetime.now(tz=timezone.utc)

    if dt > now + timedelta(minutes=minutes):
        return False

    if dt < now - timedelta(minutes=minutes):
        return False

    return True
