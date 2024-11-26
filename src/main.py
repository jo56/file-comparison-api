from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from src.model.compare_service import CompareService, ComparisonServiceOutput
from src.model.comparison_file import ComparisonFile
import json
from PyPDF2 import PdfReader

app = FastAPI()

@app.get("/")
def read_root():
    return {"Sucessful": "Connection"}

@app.get("/health")
def health_check():
    return {"Health": "Sucessful"}


@app.post("/upload")
async def upload_files(
    file1: UploadFile = File(...), 
    file2: UploadFile = File(...)
):
    # Ensure the files have valid filenames
    if not file1.filename or not file2.filename:
        return JSONResponse(
            {"error": "Both files must have valid filenames"}, status_code=400
        ) 
    

    file1_obj = await generate_comparison_file(file1)
    file2_obj = await generate_comparison_file(file2)

    output = CompareService.compare(file1_obj, file2_obj)

    output_json = convert_output_to_json(output)

    return output_json

def convert_output_to_json(output: ComparisonServiceOutput):
    comparison_list = output.changes
    file_index = output.filename_index

    changes_list = []

    for change in comparison_list:
        changes_json = {
            "file1" : {
                "starting_line": change.file1.starting_line,
                "line_total": change.file1.total_lines,
                "exclusive_lines": change.file1.exclusive_lines
            },
            "file2" : {
                "starting_line": change.file2.starting_line,
                "line_total": change.file2.total_lines,
                "exclusive_lines": change.file2.exclusive_lines
            },
            "full_text_difference": change.full_text_difference
        }
        changes_list.append(changes_json)

    file_index_split = file_index.split('\n')
    file_index_split.remove('')

    output_json = {
        "num_changed_sections": len(output.changes),
        "total_lines_affected":{
            "file1": output.file1_lines_affected,
            "file2": output.file2_lines_affected,
        },
        "file_index": file_index_split,
        "changed_sections": changes_list
    }

    return output_json


async def generate_comparison_file(file: UploadFile):
    if not file.filename.endswith((".pdf", ".txt", ".py", ".ts")):
        raise HTTPException(status_code=422, 
                            detail="Invalid format. Only accepts .pdf, .txt, .py, and .ts")
    
    if file.filename.endswith(".pdf"):
        pdf_reader = PdfReader(file.file)
        text = "".join(page.extract_text() for page in pdf_reader.pages)

    else:
        file_content = await file.read()
        text = file_content.decode("utf-8")


    file_obj = ComparisonFile(file.filename, text)

    return file_obj