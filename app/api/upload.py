from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.rag import save_and_index_csv

router = APIRouter()

@router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_path = f"./data/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(content)

        save_and_index_csv(file_path)
        return {"message": "File uploaded and indexed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))