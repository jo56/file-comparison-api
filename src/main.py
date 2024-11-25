from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from src.model.compare_service import CompareService
from src.model.comparison_file import ComparisonFile

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
    
    print("TEST")
    file1_content = await file1.read()
    file2_content = await file2.read()

    print("TEST")

    # Decode bytes to strings (assuming UTF-8 encoded text files)
    file1_text = file1_content.decode("utf-8")
    file2_text = file2_content.decode("utf-8")

    print("TEST")

    file1_obj = ComparisonFile(file1.filename, file1_text)
    file2_obj = ComparisonFile(file2.filename, file2_text)
    
    print("TEST")

    output = CompareService.compare(file1_obj, file2_obj)
    return {
        "differences": output,
    }


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
