from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/create_task")
async def create_task(files: list[UploadFile] = File(...)):
    file_names = []

    for file in files:
        contents = await file.read() 
        file_names.append(file.filename)

    print(file_names)
    return {"message": "Файлы успешно загружены", "file_names": file_names}

