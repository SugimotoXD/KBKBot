import unittest
from unittest.mock import patch
from tempfile import NamedTemporaryFile
import pandas as pd
from CheckSchedule import compare_excel_files


class TestCompareExcelFiles(unittest.TestCase):
    def test_compare_excel_files_no_changes(self):
        # Создаем временные файлы с одинаковым содержимым
        with NamedTemporaryFile(suffix=".xlsx") as file1, NamedTemporaryFile(suffix=".xlsx") as file2:
            df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
            df.to_excel(file1.name, index=False)
            df.to_excel(file2.name, index=False)

            # Вызываем функцию compare_excel_files
            result = compare_excel_files(file1.name, file2.name)

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, "Изменений нет")

    def test_compare_excel_files_with_changes(self):
        # Создаем временные файлы с разным содержимым
        with NamedTemporaryFile(suffix=".xlsx") as file1, NamedTemporaryFile(suffix=".xlsx") as file2:
            df1 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
            df2 = pd.DataFrame({"A": [1, 2, 3], "B": [7, 5, 6]})
            df1.to_excel(file1.name, index=False)
            df2.to_excel(file2.name, index=False)

            # Вызываем функцию compare_excel_files
            result = compare_excel_files(file1.name, file2.name)

        # Проверяем, что результат соответствует ожидаемому
        expected_result = "Расписание изменилось. Для групп: B"
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
