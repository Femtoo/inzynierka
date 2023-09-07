from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile, Form
from dicom_service import getAttributesAndMakeMiniature
from db_functions import GetImageById, addImage, addGroup, GetAllImages, deleteImage, deleteGroup, GetUrlsByIds
from starlette.responses import FileResponse
from typing import List
from zipfile import ZipFile
import shutil
import sqlite3
import uuid
import os

STORAGE_PATH = r'C:\Users\KT\inzynierka\storage'

app = FastAPI()

origins = [
    "https://localhost:44398"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World", }

@app.post("/uploadimages/")
async def create_upload_files(files: List[UploadFile] = File(...), groupName: str = Form(...), description: str = Form(...)):
    uid = uuid.uuid4()
    groupID = str(uid)
    path = os.path.join(STORAGE_PATH,groupID)
    os.mkdir(path)
    errors = ""

    #copying files
    for file in files:
        fileName = file.filename
        fileExt = fileName.split('.')[-1]
        if fileExt in ['dcm']:
            url = os.path.join(path,fileName)
            try:
                with open(url, 'wb') as f:
                    shutil.copyfileobj(file.file, f)
            except Exception:
                if len(os.listdir(path)) == 0:
                    os.rmdir(path)
                errors += "There was an error uploading the file {}".format(fileName)
            finally:
                file.file.close()
                #adding to db
                (metadata,isMiniatured) = getAttributesAndMakeMiniature(url)
                await addImage(fileName, fileExt, description, url, metadata, groupID, groupName)
                await addGroup(groupID, groupName)
    return {"filenames": [file.filename for file in files], "errors": errors}

@app.get("/getimages/")
async def get_images():
    images = await GetAllImages()
    return images

@app.delete("/deleteimages/")
async def delete_images(ids):
    for id in ids:
        deleteImage(id)
    return True

@app.delete("/deletegroup/")
async def delete_group(id):
    deleteGroup(id)
    return True

@app.post("/downloadimages/")
async def download_images(ids: List[int]):
    zipUrl = os.path.join(STORAGE_PATH,"images.zip")
    with ZipFile(zipUrl, 'w') as zip_object:
        urls = await GetUrlsByIds(ids)
        for url in urls:
            zip_object.write(url['URL'])

    return "images.zip"

@app.get("/downloadzip/")
async def download_zip(filename: str):
    zipUrl = os.path.join(STORAGE_PATH,filename)
    return FileResponse(zipUrl, media_type='multipart/form-data', filename='images.zip')

@app.get("/showimage/")
async def show_image(id: int):
    img = await GetImageById(id)
    filename = img['TITLE'].replace('.dcm','.jpg')
    url = img['URL'].replace('.dcm','.jpg')
    return FileResponse(url, media_type='multipart/form-data', filename=filename)

@app.post("/downloadgroup")
async def download_group():

    return FileResponse()