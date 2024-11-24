from src.model.comparison_file import ComparisonFile
import io
import difflib
#from abc import ABC, abstractmethod
#class compare_service(ABC):
class CompareService():
    @staticmethod
    #@abstractmethod
    def compare(compfile1: ComparisonFile, compfile2: ComparisonFile):
        """Compare 2 files."""
        
        
        # Compare the files using difflib
        diff = difflib.unified_diff(compfile1.text.splitlines(), compfile2.text.splitlines(), 
                                    fromfile=compfile1.filename, tofile=compfile2.filename, lineterm='')
        
        # Join the diff result and return it
        diff_result = '\n'.join(diff)

        return diff_result