import importlib
from unittest import TestCase
from fastapi import UploadFile
from io import BytesIO
from src.main import upload_files, generate_comparison_file, convert_output_to_json
from src.model.compare_service import CompareService
import os
import asyncio
import unittest


class AppTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self):
        env_overrides = {}

    async def test_txt_compare(self):

        current_dir = os.path.dirname(__file__)
        
        file1_path =  os.path.join(current_dir, "test_files",  "text", "text_file1.txt")
        file2_path =  os.path.join(current_dir, "test_files", "text", "text_file2.txt")
        file1 = await create_comparison_file_from_local(file1_path)
        file2 = await create_comparison_file_from_local(file2_path)

        output = CompareService.compare(file1, file2)

        output_json = convert_output_to_json(output)

        expected_response = {
        "num_changed_sections": 1,
        "total_lines_affected": {
            "file1": 6,
            "file2": 0
        },
        "file_index": [
            "--- text_file1.txt",
            "+++ text_file2.txt"
        ],
        "changed_sections": [
            {
                "file1": {
                    "starting_line": "-1",
                    "line_total": "6",
                    "exclusive_lines": [
                        "gsagsfbsd",
                        "",
                        "43ghh",
                        "7",
                        "75",
                        "46yy45"
                    ]
                },
                "file2": {
                    "starting_line": "0",
                    "line_total": "0",
                    "exclusive_lines": []
                },
                "full_text_difference": "\n-gsagsfbsd\n-\n-43ghh\n-7\n-75\n-46yy45\n"
            }
        ]
    }
        print(expected_response)
        
        self.assertDictEqual(output_json, expected_response)

    def test_pdf_compare(self):
        pass

    def test_py_compare(self):
        pass

    def test_ts_compare(self):
        pass

   
def create_upload_file_from_local(file_path: str) -> UploadFile:
    # Open the local file in binary read mode
        with open(file_path, "rb") as f:
            # Read the file content
            file_content = BytesIO(f.read())

        # Create and return an UploadFile instance
        return UploadFile(filename=file_path.split("\\")[-1], file=file_content)
    

def create_comparison_file_from_local(file_path: str) -> UploadFile:
    # Open the local file in binary read mode
    upload_file = create_upload_file_from_local(file_path)
    comparison_file = generate_comparison_file(upload_file)
    return comparison_file