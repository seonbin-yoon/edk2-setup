import datetime


def get_spend_time(start_time: datetime.datetime, end_time: datetime.datetime) -> str:
    spend_second = int((end_time - start_time).total_seconds())

    if spend_second < 60:
        return f"{spend_second}초"

    if spend_second < 3600:
        return f"{spend_second // 60}분"

    return f"{spend_second // 3600}시간"
