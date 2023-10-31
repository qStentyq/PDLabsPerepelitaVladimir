import unittest
from Lab5 import current_datetime_formatted, calculate_date_difference
import datetime

class TestDateUtils(unittest.TestCase):
    def test_current_datetime_formatted(self):
        # Тест форматирования текущей даты и времени
        formatted_time = current_datetime_formatted("%Y-%m-%d %H:%M:%S")
        current_time = datetime.datetime.now()
        expected_formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(formatted_time, expected_formatted_time)

    def test_calculate_date_difference(self):
        # Тест вычисления разницы между датами
        date1 = datetime.datetime(2023, 1, 1)
        date2 = datetime.datetime(2023, 1, 5)
        date_difference = calculate_date_difference(date1, date2)
        expected_difference = datetime.timedelta(days=4)
        self.assertEqual(date_difference, expected_difference)

if __name__ == '__main__':
    unittest.main()
