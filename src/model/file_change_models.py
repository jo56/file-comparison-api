
class FileChange:
    
    starting_line: int
    total_lines: int
    exclusive_lines: list[str]

class FileChangeComparison:

    file1: FileChange
    file2: FileChange
    full_text_difference: str 

    def __init__(self, file1, file2, text):
        self.file1 = file1
        self.file2 = file2
        self.full_text_difference = text

class ComparisonServiceOutput:
    filename_index: str
    changes: list[FileChangeComparison]
    file1_lines_affected: int
    file2_lines_affected: int

    def __init__(self, filename_index, changes, file1_lines_affected, file2_lines_affected):
        self.filename_index = filename_index
        self.changes = changes
        self.file1_lines_affected = file1_lines_affected
        self.file2_lines_affected = file2_lines_affected
