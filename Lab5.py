import datetime

def current_datetime_formatted(format="%Y-%m-%d %H:%M:%S"):
    """
    Возвращает текущую дату и время в заданном формате.

    :param format: Формат вывода даты и времени. По умолчанию: "%Y-%m-%d %H:%M:%S".
    :return: Строка с текущей датой и временем в указанном формате.
    """
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

def calculate_date_difference(date1, date2):
    """
    Вычисляет разницу между двумя датами.

    :param date1: Первая дата в формате datetime.
    :param date2: Вторая дата в формате datetime.
    :return: Объект timedelta, представляющий разницу между датами.
    """
    if date1 > date2:
        date1, date2 = date2, date1
    date_difference = date2 - date1
    return date_difference
