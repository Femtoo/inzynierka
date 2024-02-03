import zipfile
from fastapi import BackgroundTasks, FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.mirax_service import getMetadataAndMakeMiniatureMRX
from services.dicom_service import getAttributesAndMakeMiniatureDCM
from services.tiff_service import getMetadataAndMakeMiniatureTIFF
from services.jpg_service import getMetadataAndMakeMiniatureJPG
from services.vips_service import getMetadataAndMakeMiniatureVips
from db_functions import GetImageById, addImage, addGroup, GetAllImages, deleteImages, deleteGroup, GetUrlsByIds, GetAllGroups, GetImagesByGroupId, GetImages, UpdateImagesGroup, UpdateImagesURL, GetGroupById, UpdateImagesDesc
from starlette.responses import FileResponse
from typing import List
from zipfile import ZipFile
from logging.config import dictConfig
import logging
from logconf import LogConfig
import shutil
import sqlite3
import uuid
import os
from os.path import basename

STORAGE_PATH = r'C:\Users\KT\inzynierka\storage'
WORK_DIR_PATH = r'C:\Users\KT\inzynierka\processImagesDir'

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("main_logger")

class ChangeGroupDTO(BaseModel):
    ids: List[int]
    groupID: str

class ChangeDescDTO(BaseModel):
    id: int
    description: str

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

@app.post("/uploadimages/")
async def upload_files(files: List[UploadFile] = File(...), groupName: str = Form(...), description: str = Form(...)):
    uid = uuid.uuid4()
    groupID = str(uid)
    errors = ""
    file_formats = ['dcm', 'zip', 'tif', 'tiff', 'jpg', 'jpeg', 'svs', 'vms', 'vmu', 'ndpi', 'scn', 'svslide', 'bif', 'mrxs']
    logger.info("Upload images: {}".format([file.filename for file in files]))
    path = os.path.join(STORAGE_PATH,groupID)
    os.mkdir(path)

    await addGroup(groupID, groupName)
    logger.info("Group {} created".format(groupName))
    #copying files
    for file in files:
        fileName = file.filename
        fileExt = fileName.split('.')[-1].lower()
        fileName = fileName.replace(fileName.split('.')[-1], fileExt)
        url = os.path.join(path,fileName)
        isCopied = True

        if fileExt in file_formats:
            try:
                with open(url, 'wb') as f:
                    shutil.copyfileobj(file.file, f)
            except Exception:
                # if len(os.listdir(path)) == 0:
                #     os.rmdir(path)
                errors += "There was an error uploading the file {}".format(fileName)
                logger.error("There was an error uploading the file {}".format(fileName))
                isCopied = False
            finally:
                file.file.close()
        else:
            errors += "There was an error uploading the file {} - wrong format".format(fileName)
            logger.error("There was an error uploading the file {} - wrong format".format(fileName))
            isCopied = False

        if isCopied:
            if fileExt == 'dcm':
                imageType = 'DICOM'
                (metadata,isMiniatured) = getAttributesAndMakeMiniatureDCM(url, url)
                await addImage(fileName, imageType, description, url, metadata, groupID, groupName)
            elif fileExt == 'zip':
                imageName = ''
                newuid = uuid.uuid4()
                workDirID = str(newuid)
                workDirPath = os.path.join(WORK_DIR_PATH,workDirID)
                os.mkdir(workDirPath)
                with zipfile.ZipFile(url, 'r') as zip_ref:
                    isFound, imageName = check_and_get_file_name(url)
                    if isFound:
                        zip_ref.extractall(workDirPath)
                    else:
                        errors += "There was an error uploading the file {} - wrong zip structure".format(fileName)
                        logger.error("There was an error uploading the file {} - wrong zip structure".format(fileName))
                        zip_ref.close()
                        os.remove(url)
                        shutil.rmtree(workDirPath)
                        continue
                if imageName.split('.')[-1].lower() == 'dcm':
                    imageFormat = 'DICOM'
                    (metadata,isMiniatured) = getAttributesAndMakeMiniatureDCM(os.path.join(workDirPath, imageName), url)
                    await addImage(fileName, imageFormat, description, url, metadata, groupID, groupName)
                else:
                    (metadata,isMiniatured, imageFormat) = getMetadataAndMakeMiniatureVips(os.path.join(workDirPath, imageName), url)
                    await addImage(fileName, imageFormat, description, url, metadata, groupID, groupName)
                shutil.rmtree(workDirPath)
                
            # elif fileExt == 'zip':
            #     imageType = 'MIRAX'
            #     fileValidation = fileName.split('.')[0]
            #     fileValidationName = fileValidation + '.mrxs'
            #     fileValidationDirectory = fileValidation +'/'
            #     with zipfile.ZipFile(url, 'r') as zip_ref:
            #         if all(item in zip_ref.namelist() for item in [fileValidationName, fileValidationDirectory]):
            #             zip_ref.extractall(path)
            #         else:
            #             errors += "There was an error uploading the file {} - wrong zip structure".format(fileName)
            #             zip_ref.close()
            #             os.remove(url)
            #             continue
            #     (metadata,isMiniatured) = getMetadataAndMakeMiniatureMRX(url.replace('.zip', '.mrxs'))
            #     await addImage(fileName, imageType, description, url, metadata, groupID, groupName)
            #     os.remove(os.path.join(path,fileValidationName))
            #     shutil.rmtree(os.path.join(path,fileValidationDirectory))
            # elif fileExt == 'tiff' or fileExt == 'tif':
            #     (metadata,isMiniatured) = getMetadataAndMakeMiniatureTIFF(url)
            #     await addImage(fileName, fileExt, description, url, metadata, groupID, groupName)
            elif fileExt == 'jpg' or fileExt == 'jpeg':
                imageFormat = 'jpg'
                (metadata,isMiniatured) = getMetadataAndMakeMiniatureJPG(url)
                await addImage(fileName, imageFormat, description, url, metadata, groupID, groupName)
            else:
                (metadata,isMiniatured, imageFormat) = getMetadataAndMakeMiniatureVips(url, url)
                await addImage(fileName, imageFormat, description, url, metadata, groupID, groupName)

    return {"filenames": [file.filename for file in files], "errors": errors}

@app.get("/getimages/")
async def get_images():
    images = await GetAllImages()
    return images

@app.get("/getgroups/")
async def get_groups():
    images = await GetAllGroups()
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

@app.delete("/deletegroup/{id}")
async def delete_group(id):
    try:
        images = await GetImagesByGroupId(id)
        ids = [img['ID'] for img in images]
        urls = await GetUrlsByIds(ids)
        await deleteImages(ids)
        await deleteGroup(id)
        shutil.rmtree(os.path.join(STORAGE_PATH, id))
    except Exception:
        return False
    return True

@app.put("/updategroup/")
async def update_group(dto: ChangeGroupDTO):
    ids = dto.ids
    groupID = dto.groupID
    groupPath = os.path.join(STORAGE_PATH, groupID)
    if groupID != '':
        try:
            group = await GetGroupById(groupID)
            imgs = await GetImages(ids)
            await UpdateImagesGroup(ids, groupID, group['GROUPNAME'])
            await UpdateImagesURL(imgs, groupPath)
            for img in imgs:
                shutil.move(img['URL'], os.path.join(groupPath, img['TITLE']))
                shutil.move(get_miniature_suffix(img['URL']), os.path.join(groupPath, get_miniature_suffix(img['TITLE'])))
        except Exception as e:
            print(e)
            return False
        return True

@app.post("/downloadimages/")
async def download_images(ids: List[int]):
    uid = uuid.uuid4()
    zipName = str(uid)
    zipUrl = os.path.join(STORAGE_PATH,zipName)
    urls = await GetUrlsByIds(ids)
    with ZipFile(zipUrl, 'w') as zip_object:
        for url in urls:
            zip_object.write(url['URL'], basename(url['URL']))

    return zipName

@app.get("/downloadzip/")
async def download_zip(filename: str, background_tasks: BackgroundTasks):
    zipUrl = os.path.join(STORAGE_PATH,filename)
    background_tasks.add_task(delete_zip_package, zipUrl)
    return FileResponse(zipUrl, media_type='multipart/form-data', filename=filename+'.zip')

@app.get("/showimage/")
async def show_image(id: int):
    img = await GetImageById(id)
    filename = get_miniature_suffix(img['TITLE'])
    url = get_miniature_suffix(img['URL'])
    # print(str(url) + " " + str(filename))
    return FileResponse(url, media_type='multipart/form-data', filename=filename)

@app.get("/downloadgroup/{id}")
async def download_group(id: str):
    uid = uuid.uuid4()
    zipName = str(uid)
    zipUrl = os.path.join(STORAGE_PATH,zipName)
    images = await GetImagesByGroupId(id)
    ids = [img['ID'] for img in images]
    urls = await GetUrlsByIds(ids)
    with ZipFile(zipUrl, 'w') as zip_object:
        for url in urls:
            zip_object.write(url['URL'], basename(url['URL']))
    return zipName

@app.put("/updatedesc/")
async def update_image_description(dto: ChangeDescDTO):
    await UpdateImagesDesc(dto.id, dto.description)
    return True

def get_miniature_suffix(data):
    fileEXT = "." + data.split('.')[-1]
    if fileEXT in ['.jpg', '.jpeg']:
        miniatureURL = data.replace(fileEXT, 'Miniature$$#%^&.jpg')
    else:
        miniatureURL = data.replace(fileEXT, '.jpg')
    return miniatureURL

def delete_zip_package(zipPackageUrl :str):
    os.remove(zipPackageUrl)

def check_and_get_file_name(zip_file_path):
    formats = ['dcm', 'zip', 'tif', 'tiff', 'svs', 'vms', 'vmu', 'ndpi', 'scn', 'svslide', 'bif', 'mrxs']
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        print(zip_ref.namelist())
        for item in formats:
            for file_name in zip_ref.namelist():
                if str('.' + item) in file_name.lower():
                    return True, file_name
    return False, None