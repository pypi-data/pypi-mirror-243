from datetime import timedelta


def get_time_delta(time_unit, time_amount):
    if time_unit == 'SECOND':
        return timedelta(seconds=time_amount)
    if time_unit == 'MINUTE':
        return timedelta(minutes=time_amount)
    if time_unit == 'HOUR':
        return timedelta(hours=time_amount)
    if time_unit == 'DAY':
        return timedelta(days=time_amount)
    if time_unit == 'WEEK':
        return timedelta(weeks=time_amount)
    if time_unit == 'YEAR':
        return timedelta(days=time_amount * 365)
    return None
