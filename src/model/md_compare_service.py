from fastapi import UploadFile
from model.compare_service import CompareService

class md_compare_service(CompareService):
    
    @staticmethod
    def compare(self, file1: UploadFile, file2: UploadFile):
        """Compare 2 files."""
        pass