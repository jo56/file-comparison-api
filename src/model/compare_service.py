from fastapi import UploadFile
from abc import ABC, abstractmethod
class compare_service(ABC):
    
    @staticmethod
    @abstractmethod
    def compare(self, file1: UploadFile, file2: UploadFile):
        """Compare 2 files."""
        pass