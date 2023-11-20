from PIL import Image
from PIL.ExifTags import TAGS

Image.MAX_IMAGE_PIXELS = None

def getMetadataAndMakeMiniatureJPG(path):
    miniature_size = 256, 256
    isMiniatured = True
    pathMIN = path.split('.')[0]
    pathMIN = pathMIN + "Miniature$$#%^&.jpg"
    metadata = ""
    try:
        img = Image.open(path)
        exifdata = img.getexif()
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode()
            if tag not in ['TileByteCounts', 'TileOffsets', 'JPEGTables']:
                metadata += f"{tag} = {data}\n"
    except Exception:
        return ("There was an error reading file", False)
    finally:
        try:
            img.thumbnail(miniature_size, Image.Resampling.LANCZOS)
            img.save(pathMIN,"JPEG")
        except Exception:
            isMiniatured = False
        # print(metadata + "" + str(isMiniatured))
        return(metadata, isMiniatured)

# print(getMetadataAndMakeMiniatureJPG('DSCN3142.jpg')[0])