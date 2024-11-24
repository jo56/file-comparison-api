from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

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
    }
