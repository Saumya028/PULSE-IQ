from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def is_recent(date_string, days=30):

    if not date_string:
        return False

    try:

        try:
            dt = datetime.fromisoformat(
                date_string.replace("Z", "+00:00")
            )

        except Exception:
            dt = parsedate_to_datetime(date_string)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return (datetime.now(timezone.utc) - dt).days <= days

    except Exception:

        print("DATE ERROR:", date_string)

        return False