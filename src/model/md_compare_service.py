from fastapi import UploadFile
from src.model.compare_service import CompareService

class md_compare_service(compare_service):
    
    @staticmethod
    def compare(self, file1: UploadFile, file2: UploadFile):
        """Compare 2 files."""
        pass