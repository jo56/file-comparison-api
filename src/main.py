from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from src.model.compare_service import CompareService
from src.model.comparison_file import ComparisonFile
import json

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
    
    file1_content = await file1.read()
    file2_content = await file2.read()

    file1_text = file1_content.decode("utf-8")
    file2_text = file2_content.decode("utf-8")


    file1_obj = ComparisonFile(file1.filename, file1_text)
    file2_obj = ComparisonFile(file2.filename, file2_text)
    

    output = CompareService.compare(file1_obj, file2_obj)

    print(output)
    comparison_list = output.changes
    file_index = output.filename_index

    changes_list = []

    for change in comparison_list:
        {
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
        changes_list.append(change)

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


    """
    # Save the files or process them
    file1_path = f"./uploads/{file1.filename}"
    file2_path = f"./uploads/{file2.filename}"

    # Save files to disk
    with open(file1_path, "wb") as f:
        f.write(await file1.read())

    with open(file2_path, "wb") as f:
        f.write(await file2.read())
    

    return {
        "message": "Files uploaded successfully",
        "file1": file1.filename,
        "file2": file2.filename,
    }"""
