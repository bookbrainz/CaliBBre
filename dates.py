import re
from datetime import date, datetime

# BookBrainz represents dates as "extended dates": a signed year of four to six
# digits, optionally followed by -MM and -DD.
# Examples: "+002017", "+002017-01", "+002017-01-04", "-000120-03", "2017-01-04"
EXTENDED_DATE_REGEX = re.compile(
    r"^([+-]?\d{4,6})(?:-(\d{2}))?(?:-(\d{2}))?$"
)


def parse_extended_date(date_str):
    """Parse an extended date string.

    Returns a (year, month, day) tuple where month and day are None when the
    string omits them, or None when the string is not a valid extended date.
    """
    if not date_str:
        return None
    match = EXTENDED_DATE_REGEX.match(date_str.strip())
    if not match:
        return None
    year, month, day = match.groups()
    return (
        int(year),
        int(month) if month else None,
        int(day) if day else None,
    )


def format_extended_date(date_str, fmt="%x", default="Unknown"):
    """Render an extended date as a locale-aware date-only string.

    Falls back to the raw extended string when the year is outside Python's
    supported range, and to "default" when the date can't be parsed.
    """
    parsed = parse_extended_date(date_str)
    if parsed is None:
        return default
    year, month, day = parsed
    if not 1 <= year <= 9999:
        return date_str.strip()
    if month and day:
        try:
            return date(year, month, day).strftime(fmt)
        except ValueError:
            return date_str.strip()
    if month:
        return date(year, month, 1).strftime("%B %Y")
    return str(year)


def extended_date_to_datetime(date_str):
    """Convert an extended date to a datetime (missing month/day default to 1).

    Returns None when the date can't be parsed or its year is outside Python's
    supported range.
    """
    parsed = parse_extended_date(date_str)
    if parsed is None:
        return None
    year, month, day = parsed
    if not 1 <= year <= 9999:
        return None
    try:
        return datetime(year, month or 1, day or 1)
    except ValueError:
        return None
