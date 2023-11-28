from datetime import datetime


def parse_date_to_format(date: str, format='%d-%m-%Y'):
    return datetime.strptime(date, format).strftime(format)

def parse_date_object_to_format(date: datetime, format='%d-%m-%Y'):
    return date.strftime(format)