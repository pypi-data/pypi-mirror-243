import datetime


def get_date():
    """Returns the current date in the format of dd/mm/yyyy

    :return: str
    """
    return datetime.datetime.now().strftime("%d/%m/%Y")


def get_time():
    """Returns the current time in the format of hh:mm:ss

    :return: str
    """
    return datetime.datetime.now().strftime("%H:%M:%S:%f")
