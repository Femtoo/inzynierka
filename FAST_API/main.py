import zipfile
from fastapi import BackgroundTasks, FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from services.mirax_service import getMetadataAndMakeMiniatureMRX
from services.dicom_service import getAttributesAndMakeMiniatureDCM
from services.tiff_service import getMetadataAndMakeMiniatureTIFF
from services.jpg_service import getMetadataAndMakeMiniatureJPG
from db_functions import GetImageById, addImage, addGroup, GetAllImages, deleteImages, deleteGroup, GetUrlsByIds
from starlette.responses import FileResponse
from typing import List
from zipfile import ZipFile
import shutil
import sqlite3
import uuid
import os
from os.path import basename

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
    errors = ""
    # isAllowed = False

    # for file in files:
    #     fileName = file.filename
    #     # print(fileName)
    #     fileExt = fileName.split('.')[-1]
    #     if fileExt in ['dcm', 'zip', 'tif', 'tiff', 'jpg', 'jpeg']:
    #         isAllowed = True

    # if isAllowed == False:
    #     return {"message": "Not allowed format", }
    
    path = os.path.join(STORAGE_PATH,groupID)
    os.mkdir(path)

    #copying files
    for file in files:
        fileName = file.filename
        fileExt = fileName.split('.')[-1].lower()
        fileName = fileName.replace(fileName.split('.')[-1], fileExt)
        url = os.path.join(path,fileName)
        isCopied = True

        if fileExt in ['dcm', 'zip', 'tif', 'tiff', 'jpg', 'jpeg']:
            try:
                with open(url, 'wb') as f:
                    shutil.copyfileobj(file.file, f)
            except Exception:
                # if len(os.listdir(path)) == 0:
                #     os.rmdir(path)
                errors += "There was an error uploading the file {}".format(fileName)
                isCopied = False
            finally:
                file.file.close()

        if isCopied:
            if fileExt == 'dcm':
                (metadata,isMiniatured) = getAttributesAndMakeMiniatureDCM(url)
                await addImage(fileName, fileExt, description, url, metadata, groupID, groupName)
                await addGroup(groupID, groupName)
            elif fileExt == 'zip':
                with zipfile.ZipFile(url, 'r') as zip_ref:
                    zip_ref.extractall(path)
                (metadata,isMiniatured) = getMetadataAndMakeMiniatureMRX(url.replace('.zip', '.mrxs'))
                await addImage(fileName, 'mrxs', description, url, metadata, groupID, groupName)
                await addGroup(groupID, groupName)
            elif fileExt == 'tiff' or fileExt == 'tif':
                (metadata,isMiniatured) = getMetadataAndMakeMiniatureTIFF(url)
                await addImage(fileName, fileExt, description, url, metadata, groupID, groupName)
                await addGroup(groupID, groupName)
            elif fileExt == 'jpg' or fileExt == 'jpeg':
                (metadata,isMiniatured) = getMetadataAndMakeMiniatureJPG(url)
                await addImage(fileName, fileExt, description, url, metadata, groupID, groupName)
                await addGroup(groupID, groupName)
            else:
                errors += "There was an error uploading the file {} - wrong format".format(fileName)

    return {"filenames": [file.filename for file in files], "errors": errors}

@app.get("/getimages/")
async def get_images():
    images = await GetAllImages()
    return images

@app.get("/getgroups/")
async def get_groups():
    images = await GetAllImages()
    return images

@app.post("/deleteimages/")
async def delete_images(ids: List[int]):
    try:
        urls = await GetUrlsByIds(ids)
        for url in urls:
            os.remove(get_miniature_suffix(url['URL']))
            os.remove(url['URL'])
        await deleteImages(ids)
    except Exception:
        return False
    return True

@app.delete("/deletegroup/")
async def delete_group(id):
    await deleteGroup(id)
    return True

@app.post("/downloadimages/")
async def download_images(ids: List[int]):
    uid = uuid.uuid4()
    zipName = str(uid)
    zipUrl = os.path.join(STORAGE_PATH,zipName)
    with ZipFile(zipUrl, 'w') as zip_object:
        urls = await GetUrlsByIds(ids)
        for url in urls:
            zip_object.write(url['URL'], basename(url['URL']))

    return zipName

@app.get("/downloadzip/")
async def download_zip(filename: str, background_tasks: BackgroundTasks):
    zipUrl = os.path.join(STORAGE_PATH,filename)
    background_tasks.add_task(delete_zip_package, zipUrl)
    return FileResponse(zipUrl, media_type='multipart/form-data', filename='images.zip')

@app.get("/showimage/")
async def show_image(id: int):
    img = await GetImageById(id)
    filename = get_miniature_suffix(img['TITLE'])
    url = get_miniature_suffix(img['URL'])
    # print(str(url) + " " + str(filename))
    return FileResponse(url, media_type='multipart/form-data', filename=filename)

@app.post("/downloadgroup/")
async def download_group():

    return FileResponse()

def get_miniature_suffix(data):
    fileEXT = "." + data.split('.')[-1]
    if fileEXT in ['.jpg', '.jpeg']:
        miniatureURL = data.replace(fileEXT, 'Miniature$$#%^&.jpg')
    else:
        miniatureURL = data.replace(fileEXT, '.jpg')
    return miniatureURL

def delete_zip_package(zipPackageUrl :str):
    os.remove(zipPackageUrl)