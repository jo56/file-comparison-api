import importlib
from unittest import TestCase
from fastapi import UploadFile, HTTPException
from io import BytesIO
from src.main import compare_files, generate_comparison_file, convert_output_to_json
from src.model.compare_service import CompareService
import os
import asyncio
import unittest
import json


class AppTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    async def test_txt_compare(self):

        current_dir = os.path.dirname(__file__)
        file1_path =  os.path.join(current_dir, "test_files",  "text", "text_file1.md")
        file2_path =  os.path.join(current_dir, "test_files", "text", "text_file2.md")

        upload_file1 = create_upload_file_from_local(file1_path)
        upload_file2 = create_upload_file_from_local(file2_path)
        output = await compare_files(upload_file1, upload_file2)
        
        expected_response_path = os.path.join(current_dir, "expected_results", "text_comparison_result.json")

        with open(expected_response_path, "r") as expected_response_json:
            expected_response = json.load(expected_response_json)
            self.assertDictEqual(output, expected_response)

    async def test_pdf_compare(self):

        current_dir = os.path.dirname(__file__)
        file1_path =  os.path.join(current_dir, "test_files",  "pdf", "pdf_file1.pdf")
        file2_path =  os.path.join(current_dir, "test_files", "pdf", "pdf_file2.pdf")

        upload_file1 = create_upload_file_from_local(file1_path)
        upload_file2 = create_upload_file_from_local(file2_path)
        output = await compare_files(upload_file1, upload_file2)

        expected_response_path = os.path.join(current_dir, "expected_results", "pdf_comparison_result.json")
        
        with open(expected_response_path, "r") as expected_response_json:
            expected_response = json.load(expected_response_json)
            self.assertDictEqual(output, expected_response)

    async def test_python_compare(self):

        current_dir = os.path.dirname(__file__)
        file1_path =  os.path.join(current_dir, "test_files",  "python", "python_file1.py")
        file2_path =  os.path.join(current_dir, "test_files", "python", "python_file2.py")
        
        upload_file1 = create_upload_file_from_local(file1_path)
        upload_file2 = create_upload_file_from_local(file2_path)
        output = await compare_files(upload_file1, upload_file2)

        expected_response_path = os.path.join(current_dir, "expected_results", "python_comparison_result.json")
        
        with open(expected_response_path, "r") as expected_response_json:
            expected_response = json.load(expected_response_json)
            self.assertDictEqual(output, expected_response)

    async def test_typescript_compare(self):

        current_dir = os.path.dirname(__file__)
        file1_path =  os.path.join(current_dir, "test_files",  "typescript", "ts_file1.ts")
        file2_path =  os.path.join(current_dir, "test_files", "typescript", "ts_file2.ts")
        
        upload_file1 = create_upload_file_from_local(file1_path)
        upload_file2 = create_upload_file_from_local(file2_path)
        output = await compare_files(upload_file1, upload_file2)

        expected_response_path = os.path.join(current_dir, "expected_results", "typescript_comparison_result.json")
        
        with open(expected_response_path, "r") as expected_response_json:
            expected_response = json.load(expected_response_json)
            #expected_file_index = [f"--- {os.path.basename(file1_path)}", f"+++ {os.path.basename(file1_path)}"]
            #expected_response["file_index"] = expected_file_index
            self.assertDictEqual(output, expected_response)

    async def test_cross_type_compare(self):

        current_dir = os.path.dirname(__file__)
        file1_path =  os.path.join(current_dir, "test_files",  "pdf", "pdf_file2.pdf")
        file2_path =  os.path.join(current_dir, "test_files", "typescript", "ts_file2.ts")
        
        upload_file1 = create_upload_file_from_local(file1_path)
        upload_file2 = create_upload_file_from_local(file2_path)
        output = await compare_files(upload_file1, upload_file2)

        expected_response_path = os.path.join(current_dir, "expected_results", "cross_type_comparison_result.json")

        with open(expected_response_path, "r") as expected_response_json:
            expected_response = json.load(expected_response_json)
            self.assertDictEqual(output, expected_response)

    async def test_same_file_compare(self):

        current_dir = os.path.dirname(__file__)
        file1_path =  os.path.join(current_dir, "test_files", "typescript", "ts_file2.ts")
        
        upload_file1 = create_upload_file_from_local(file1_path)
        upload_file2 = create_upload_file_from_local(file1_path)
        output = await compare_files(upload_file1, upload_file2)

        expected_response = {
            "num_changed_sections": 0,
            "total_lines_affected": {
                "file1": 0,
                "file2": 0
            },
            "file_index": [
                "--- ts_file2.ts",
                "+++ ts_file2.ts"
            ],
            "changed_sections": []
        }

        self.assertDictEqual(output, expected_response)

    async def test_invalid_format(self):

        current_dir = os.path.dirname(__file__)
        file1_path =  os.path.join(current_dir, "test_files",  "pdf", "pdf_file2.pdf")
        file2_path =  os.path.join(current_dir, "test_files", "invalid_format", "test_file1.doc")
        upload_file1 = create_upload_file_from_local(file1_path)
        upload_file2 = create_upload_file_from_local(file2_path)

        with self.assertRaises(HTTPException):
            await compare_files(upload_file1, upload_file2)

   
def create_upload_file_from_local(file_path: str) -> UploadFile:
        with open(file_path, "rb") as f:
            file_content = BytesIO(f.read())

        return UploadFile(filename=file_path.split("\\")[-1], file=file_content)
    