from src.model.comparison_file import ComparisonFile
import io
import difflib
import re
from src.model.file_change_models import FileChange, FileChangeComparison, ComparisonServiceOutput
import json
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

        
        combined_diff = ""
        for specific_diff in diff:
             combined_diff += specific_diff + "\n"

        if combined_diff == "":
            filename_format = f"--- {compfile1.filename}\n+++ {compfile2.filename}\n"
            return ComparisonServiceOutput(filename_format, [] , 0, 0)

        diff_result = combined_diff
        print("diff_result")
        print(diff_result)
        diffsplit = diff_result.split("@@")
        trimmed_diffsplit = []
        for item in diffsplit:
            if item != '':
                trimmed_diffsplit.append(item)
        
        print("diffsplit 1")
        diffsplit = trimmed_diffsplit
        for diff in diffsplit:
            print(diff)
        filenames = diffsplit.pop(0)
        total_differences = []
        pattern = r"-(\d+),(\d+) \+(\d+),(\d+)"



        print("diffsplit 2")
        print(diffsplit)
        total_file1_lines_affected = 0
        total_file2_lines_affected = 0
        for i in range (0, len(diffsplit), 2):
            File1Changes = FileChange()
            File2Changes = FileChange()
            
            change_line_readings = diffsplit[i]
            change_line_readings = change_line_readings.strip()
            print(i)
            print("line changes")
            print(change_line_readings)
            change_line_readings.replace("-", '')
            change_line_split = change_line_readings.split('+')
            #match = re.match(pattern, change_line_readings)

            start_old, count_old = get_line_change(change_line_split[0])
            start_new, count_new = get_line_change(change_line_split[1])

            File1Changes.starting_line = start_old
            File1Changes.total_lines = count_old

            File2Changes.starting_line = start_new
            File2Changes.total_lines = count_new

            line_changes = diffsplit[i+1]
            full_text = line_changes
            line_changes_split = line_changes.split("\n")
            #for line in line_changes
            file1_exclusive_lines =[]
            file2_exclusive_lines = []
            for line in line_changes_split:
                if line.startswith('-'):
                    file1_exclusive_lines.append(line[1:])
                    total_file1_lines_affected = total_file1_lines_affected + 1
                elif line.startswith('+'):
                    file2_exclusive_lines.append(line[1:])
                    total_file2_lines_affected = total_file2_lines_affected + 1
            
            File1Changes.exclusive_lines = file1_exclusive_lines
            File2Changes.exclusive_lines = file2_exclusive_lines

            CombinedFileDifferences = FileChangeComparison(File1Changes, File2Changes, full_text)
            total_differences.append(CombinedFileDifferences)

        output_result = ComparisonServiceOutput(filenames, total_differences , total_file1_lines_affected, total_file2_lines_affected)
        return output_result
    
    
def  get_line_change(input_string: str):
        if ',' not in input_string:
            return input_string, 1
        else:
            comma_split = input_string.split(',')
            split_second = comma_split[1].strip()
            return comma_split[0], split_second