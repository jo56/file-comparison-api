from fastapi import UploadFile
from model.compare_service import CompareService
import difflib

class py_compare_service(compare_service):

    x
    
    @staticmethod
    def compare(self, file1: UploadFile, file2: UploadFile):
        """Compare 2 files."""
        

        # Generate a unified diff
        diff = difflib.unified_diff(
            file1_lines, 
            file2_lines, 
            fromfile='File1', 
            tofile='File2', 
            lineterm=''
        )

        print("Differences:")
        for line in diff:
            print(line)
        
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            file1_lines = f1.readlines()
            file2_lines = f2.readlines()

        
