import unittest
import os

from data_ingestion.workbook import WorkBook

class WorkBookTest(unittest.TestCase):
    def test_it_descovers_sheets_from_excel(self):
        workBook = WorkBook.from_xlsx("src/test/test_data/Sample-Spreadsheets_data-ingestion_fixtures.xlsx")

        self.assertEquals(10, workBook.size())

    def test_it_exports_to_csv(self):
        filename = "Sample-Spreadsheets_data-ingestion_fixtures"

        target_dir = "src/test/test_data/output"
        
        workBook = WorkBook.from_xlsx(f"src/test/test_data/{filename}.xlsx")

        workBook.write_all(target_dir)

        self.assert_file_count_for_dir(target_dir,10)

    def test_it_blows_up_for_missing_dir_with_no_create_flag(self):
        filename = "Sample-Spreadsheets_data-ingestion_fixtures"

        target_dir = "test_data/I/do/not/EXIST"
        
        workBook = WorkBook.from_xlsx(f"src/test/test_data/{filename}.xlsx")

        def try_it():
            workBook.write_all(target_dir,should_create_dir=False)

        self.assertRaises(Exception,try_it)

    def assert_file_count_for_dir(self,dir_name,expected_number_of_files):
        actual_count = 0

        for path in os.listdir(dir_name):
            if os.path.isfile(os.path.join(dir_name, path)):
                actual_count += 1

        self.assertEquals(expected_number_of_files,actual_count)