DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M:%S"


def current_formatted_date(format: str = DEFAULT_DATE_FORMAT) -> str:
    """Returns big-endian string of the current date"""
    import datetime

    return datetime.datetime.now().strftime(format)
