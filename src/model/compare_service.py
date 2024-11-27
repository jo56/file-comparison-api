from src.model.comparison_file import ComparisonFile
import difflib
from src.model.file_change_models import FileChange, FileChangeComparison, ComparisonServiceOutput
class CompareService():


    @staticmethod
    def compare(compfile1: ComparisonFile, compfile2: ComparisonFile) -> ComparisonServiceOutput:

        diff = difflib.unified_diff(compfile1.text.splitlines(), compfile2.text.splitlines(), 
                                    fromfile=compfile1.filename, tofile=compfile2.filename, lineterm='')
        
        combined_diff = ""
        filename_format = f"--- {compfile1.filename}\n+++ {compfile2.filename}\n"

        for specific_diff in diff:
             combined_diff += specific_diff + "\n"

        if combined_diff == "":
            return ComparisonServiceOutput(filename_format, [] , 0, 0)

        raw_changed_sections_list = combined_diff.split("@@")
        changed_sections_list = filter_array(raw_changed_sections_list)
        changed_sections_list.pop(0)

        total_differences = []
        for i in range (0, len(changed_sections_list), 2):
            new_comparison = generate_comparison_for_section(changed_sections_list, i)
            total_differences.append(new_comparison)

        total_file1_lines_affected = 0
        total_file2_lines_affected = 0
        for comp in total_differences:
            total_file1_lines_affected = total_file1_lines_affected + len(comp.file1.exclusive_lines)
            total_file2_lines_affected = total_file2_lines_affected + len(comp.file2.exclusive_lines)

        output_result = ComparisonServiceOutput(filename_format, total_differences, 
                                                total_file1_lines_affected, total_file2_lines_affected)
        return output_result
    
    

        
def  generate_comparison_for_section(changed_section: str, i: int) -> FileChangeComparison:
        File1Changes = FileChange()
        File2Changes = FileChange()
        
        change_line_readings = changed_section[i]
        change_line_readings = change_line_readings.strip()
        change_line_readings = change_line_readings.replace("-", '')
        change_line_split = change_line_readings.split('+')
        print(change_line_readings)

        start_old, count_old = get_line_change(change_line_split[0])
        start_new, count_new = get_line_change(change_line_split[1])

        File1Changes.starting_line = start_old
        File1Changes.total_lines = count_old

        File2Changes.starting_line = start_new
        File2Changes.total_lines = count_new

        line_changes = changed_section[i+1]
        full_text = line_changes
        line_changes_split = line_changes.split("\n")

        file1_exclusive_lines =[]
        file2_exclusive_lines = []
        for line in line_changes_split:
            if line.startswith('-'):
                file1_exclusive_lines.append(line[1:])
            elif line.startswith('+'):
                file2_exclusive_lines.append(line[1:])
            
        File1Changes.exclusive_lines = file1_exclusive_lines
        File2Changes.exclusive_lines = file2_exclusive_lines
        
        return FileChangeComparison(File1Changes, File2Changes, full_text)
        
def filter_array(input_array: list) -> list:
    filtered_array = []
    for item in input_array:
        if item != '':
            filtered_array.append(item)
    return filtered_array

def  get_line_change(input_string: str) -> tuple[int, int]:
        if ',' not in input_string:
            return int(input_string.strip()), 1
        else:
            comma_split = input_string.split(',')
            split_second = comma_split[1].strip()
            return int(comma_split[0].strip()), int(split_second)