import datetime
import pendulum
import math


def date_with_timezone(timezone: str) -> pendulum.DateTime:
    timezone = timezone.replace(' ', '')
    timezone_split = timezone.split('+')
    if len(timezone_split) == 1:
        timezone_split = timezone.split('-')
    if len(timezone_split) != 2:
        return pendulum.now()
    current_date = pendulum.now(tz=timezone_split[0])
    current_date = current_date.add(
        hours=int(timezone_split[1])) if '+' in timezone else current_date.subtract(
        hours=int(timezone_split[1]))
    return current_date


def time_with_timezone(timezone: str):
    date = date_with_timezone(timezone=timezone)
    current_time = date.time()
    return current_time


def date_from_timestamp(timestamp: pendulum.Union[int, float], timezone: str) -> pendulum.DateTime:
    timestamp = math.trunc(timestamp)
    if len(str(timestamp)) == 13:
        timestamp = timestamp/1000
    timezone_split = timezone.split('+')
    if len(timezone_split) == 1:
        timezone_split = timezone.split('-')
    if len(timezone_split) != 2:
        return pendulum.now()
    current_date = pendulum.from_timestamp(timestamp=timestamp, tz=timezone_split[0])
    current_date = current_date.add(
        hours=int(timezone_split[1])) if '+' in timezone else current_date.subtract(
        hours=int(timezone_split[1]))
    return current_date


def pendulum_time_from_time(time: datetime.time) -> pendulum.Time:
    return pendulum.time(hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)


def time_from_timestamp_with_timezone(timestamp: pendulum.Union[int, float], timezone: str):
    date = date_from_timestamp(timestamp=timestamp, timezone=timezone)
    current_time = date.time()
    return current_time


def today_date_from_time(time: datetime.time, timezone: str = None):
    now = date_with_timezone(timezone=timezone) if timezone else pendulum.now()
    date = pendulum.datetime(year=now.year, month=now.month, day=now.day, hour=int(time.hour),
                             minute=int(time.minute), second=int(time.second), microsecond=int(time.microsecond),
                             tz=now.timezone)
    return date
