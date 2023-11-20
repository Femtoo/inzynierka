from PIL import Image
from PIL.ExifTags import TAGS

Image.MAX_IMAGE_PIXELS = None

def getMetadataAndMakeMiniatureTIFF(path):
    miniature_size = 256, 256
    isMiniatured = True
    pathJPG = path.replace('.tiff','.jpg')
    pathJPG = pathJPG.replace('.tif','.jpg')
    metadata = ""
    try:
        img = Image.open(path)
        for key in img.tag:
            if TAGS[key] not in ['TileByteCounts', 'TileOffsets', 'JPEGTables']:
                metadata += f"{TAGS[key]} = {img.tag[key]}\n"
    except Exception:
        return ("There was an error reading file", False)
    finally:
        try:
            img.thumbnail(miniature_size, Image.Resampling.LANCZOS)
            img.save(pathJPG,"JPEG")
        except Exception:
            isMiniatured = False
        # print(metadata + "" + str(isMiniatured))
        return(metadata, isMiniatured)

# print(getMetadataAndMakeMiniatureTIFF('CMU-1.tiff'))