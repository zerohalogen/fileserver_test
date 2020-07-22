import os

import aiofiles
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from hashlib import sha256
from starlette.responses import FileResponse

app = FastAPI(title="Простой сервер для хранения файлов")

FILES_DIR = os.getcwd() + '/store/'


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    """Загрузка файла"""
    file_bytes = file.file.read()
    file_hash = sha256(file_bytes).hexdigest()

    try:
        os.mkdir(FILES_DIR)
    except FileExistsError as e:
        print(e)

    file_dir = FILES_DIR + file_hash[:2] + '/'
    file_path = file_dir + file_hash

    try:
        os.mkdir(file_dir)
    except FileExistsError as e:
        print(e)

    async with aiofiles.open(file_path, 'wb+') as new_file:
        await new_file.write(file_bytes)

    return {"hash": file_hash}


@app.delete("/delete/")
async def delete(filename: str):
    """Удаление файла"""
    result = {}
    file_dir = FILES_DIR + filename[:2] + '/'
    file_path = file_dir + filename

    if os.path.exists(file_path):
        os.remove(file_path)
        result['File was deleted: '] = filename
        if not os.listdir(file_dir):
            os.rmdir(file_dir)
    else:
        result['File was not found: '] = filename

    return result


@app.get("/download/")
async def download(filename: str):
    """Скачивание файла"""
    file_dir = FILES_DIR + filename[:2] + '/'
    file_path = file_dir + filename

    if os.path.exists(file_path):
        result = FileResponse(
            path=file_path,
            media_type='application/octet-stream',
            filename=filename,
        )
    else:
        result = {'File was not found: ': filename}

    return result
