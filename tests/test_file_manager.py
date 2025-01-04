# filepath: /mnt/Main/projects/01-LLM-RAG-Projects/smart-doc-loader/tests/test_file_manager.py
import unittest
import os
import shutil
from util.file_manager import FileManager

class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = "./TestData"
        self.file_manager = FileManager(root_dir=self.test_dir)
        self.artifacts_dir = os.path.join(self.test_dir, "artifacts")
        self.expected_artifacts_dir = os.path.join(self.test_dir, "expected_artifacts")

        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.artifacts_dir, exist_ok=True)
        os.makedirs(self.expected_artifacts_dir, exist_ok=True)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_01_reset_processed_directory(self):
        os.makedirs(self.file_manager.processed_dir, exist_ok=True)
        self.file_manager.reset_processed_directory()
        self.assertTrue(os.path.exists(self.file_manager.processed_dir))
        self.assertEqual(len(os.listdir(self.file_manager.processed_dir)), 0)

    def test_02_reset_raw_directory(self):
        os.makedirs(self.file_manager.raw_dir, exist_ok=True)
        self.file_manager.reset_raw_directory()
        self.assertTrue(os.path.exists(self.file_manager.raw_dir))
        self.assertEqual(len(os.listdir(self.file_manager.raw_dir)), 0)

    def test_03_reset_originals_directory(self):
        os.makedirs(self.file_manager.originals_dir, exist_ok=True)
        self.file_manager.reset_originals_directory()
        self.assertTrue(os.path.exists(self.file_manager.originals_dir))
        self.assertEqual(len(os.listdir(self.file_manager.originals_dir)), len(self.file_manager.subdir_dict))

    def test_04_reset_all_directories(self):
        os.makedirs(self.file_manager.processed_dir, exist_ok=True)
        os.makedirs(self.file_manager.raw_dir, exist_ok=True)
        os.makedirs(self.file_manager.originals_dir, exist_ok=True)
        self.file_manager.reset_all_directories()
        self.assertTrue(os.path.exists(self.file_manager.processed_dir))
        self.assertTrue(os.path.exists(self.file_manager.raw_dir))
        self.assertTrue(os.path.exists(self.file_manager.originals_dir))
        self.assertEqual(len(os.listdir(self.file_manager.processed_dir)), 0)
        self.assertEqual(len(os.listdir(self.file_manager.raw_dir)), 0)
        self.assertEqual(len(os.listdir(self.file_manager.originals_dir)), len(self.file_manager.subdir_dict))

    def test_05_append_raw_files(self):
        os.makedirs(self.file_manager.raw_dir, exist_ok=True)
        with open(os.path.join(self.file_manager.raw_dir, "test.txt"), 'w') as f:
            f.write("test")
        raw_files_dict = self.file_manager.append_raw_files(self.file_manager.raw_dir)
        self.assertIn("txt", raw_files_dict)
        self.assertEqual(len(raw_files_dict["txt"]), 1)

    def test_06_list_raw_files(self):
        os.makedirs(self.file_manager.raw_dir, exist_ok=True)
        with open(os.path.join(self.file_manager.raw_dir, "test.txt"), 'w') as f:
            f.write("test")
        raw_files = self.file_manager.list_raw_files()
        self.assertIn("txt", raw_files)
        self.assertEqual(len(raw_files["txt"]), 1)

    def test_07_process_raw_dir_process_zip_files(self):
        self.file_manager.reset_all_directories()
        # copy ./test01.zip to raw_dir
        shutil.copy("tests/test01.zip", self.file_manager.raw_dir)
        
        processed_files = self.file_manager.process_raw_dir()
        self.assertEqual(len(processed_files), 1)
        self.assertTrue(any("test01.zip" in file for file in processed_files))


    def test_08_process_raw_dir_process_zip_docx_files(self):
        self.file_manager.reset_all_directories()
        # copy ./test02.zip to raw_dir
        shutil.copy("tests/test02.zip", self.file_manager.raw_dir)

        # copy ./test02_expected_artifacts.zip to expected_artifacts_dir and unpack it
        shutil.unpack_archive("tests/test02_expected_artifact.zip", self.expected_artifacts_dir)
        expected_processed_files_list = os.listdir(self.expected_artifacts_dir)
        
        processed_files = self.file_manager.process_raw_dir()
        self.assertEqual(len(processed_files), 3)
        self.assertTrue(any("test02.zip" in file for file in processed_files))

        file_names = ["23", "Hello"]
        for file_name in file_names:
            self.assertTrue(any(f"{file_name}.docx" in file for file in processed_files), msg= f"{file_name}.docx not found in processed_files")

        processed_files_list = os.listdir(self.file_manager.processed_dir)
        self.assertEqual(len(processed_files_list), 4, msg= f"Expected 4 files in processed_dir, found {len(processed_files_list)}")

        # compare the processed files with the expected artifacts
        # for file_name in file_names:
        #     self.assertTrue(any(f"{file_name}.md" in file for file in processed_files_list), msg= f"{file_name}.md not found in processed_files")
        #     with open(os.path.join(self.expected_artifacts_dir, f"{file_name}.md"), 'r') as expected_file:
        #         with open(os.path.join(self.file_manager.processed_dir, f"{file_name}.md"), 'r') as actual_file:
        #             self.assertEqual(expected_file.read(), actual_file.read(), msg= f"Expected content of {file_name}.md does not match actual content")
        
        for idx in range(len(expected_processed_files_list)):
            self.assertEqual(processed_files_list[idx], expected_processed_files_list[idx], msg= f"Expected {expected_processed_files_list[idx]} does not match actual {processed_files_list[idx]}")
            if os.path.isfile(os.path.join(self.expected_artifacts_dir, expected_processed_files_list[idx])):
                with open(os.path.join(self.expected_artifacts_dir, expected_processed_files_list[idx]), 'r') as expected_file:
                    with open(os.path.join(self.file_manager.processed_dir, processed_files_list[idx]), 'r') as actual_file:
                        self.assertEqual(expected_file.read(), actual_file.read(), msg= f"Expected content of {expected_processed_files_list[idx]} does not match actual content")



if __name__ == "__main__":
    unittest.main()

# python -m unittest discover -s tests