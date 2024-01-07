import logging
import os
from PIL import Image
import re

VIPS_PATH = r'C:\Users\KT\inzynierka\vips\vips-dev-8.14\bin'

os.environ['PATH'] = VIPS_PATH + ";" + os.environ['PATH']

if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(VIPS_PATH):
        import pyvips
else:
    import pyvips

logger = logging.getLogger("main_logger")

def getMetadataAndMakeMiniatureVips(path, pathForMiniature):
    miniature_size = 256
    isMiniatured = True
    imageFormat = ''
    pathJPG = get_miniature_suffix(pathForMiniature)
    metadata = ""

    filename = path.split('\\')[-1]
    logger.info(f"Reading file {filename}")

    # header = pyvips.Image.header(path)
    # print(header)
    try:
        image = pyvips.Image.new_from_file(path, access='sequential')
        # image.dzsave('overview.jpg', suffix=".jpg", tile_size=256, overlap=0, centre=True, skip_blanks=1)
        # print(str(image.get_fields()))
        fields = image.get_fields()
        photometric_interpretation = ''
        for field in fields:
            value = image.get(field)
            try:
                value = value.decode()
            except (UnicodeDecodeError, AttributeError):
                pass
            metadata += f"{field}: {value}\n"
            if field == 'interpretation':
                photometric_interpretation = value
        imageFormat = get_image_type(metadata, path)
        out = image
        try:
            if photometric_interpretation != '' and photometric_interpretation != 'rgb':
                out = image.colourspace('rgb',source_space=photometric_interpretation)
        except Exception as e:
            pass
        # print(imageFormat)
        # print(metadata)
    except Exception as e:
        print(e)
        logger.error(f"Error reading file {filename}")
        return ("There was an error reading file", False)
    finally:
        try:
            logger.info(f"Making miniature for file {filename}")
            out = out.thumbnail_image(miniature_size, height=miniature_size)
            # out = pyvips.Image.thumbnail(path, miniature_size)
            out.write_to_file(pathJPG)
        except Exception as e:
            print(e)
            logger.error(f"Error making miniature for file {filename}")
            isMiniatured = False
        return (metadata, isMiniatured, imageFormat)
    
def get_miniature_suffix(data):
    fileEXT = "." + data.split('.')[-1]
    if fileEXT in ['.jpg', '.jpeg']:
        miniatureURL = data.replace(fileEXT, 'Miniature$$#%^&.jpg')
    else:
        miniatureURL = data.replace(fileEXT, '.jpg')
    return miniatureURL

def get_image_type(metadata, path):
    fileEXT = path.split('.')[-1].lower()
    if fileEXT == 'mrxs':
        return 'MIRAX'
    elif fileEXT == 'svs':
        return 'Aperio'
    elif fileEXT == 'scn':
        return 'Leica'
    elif fileEXT in ['ndpi', 'vmu', 'vms']:
        return 'Hamamatsu'
    elif fileEXT == 'svslide':
        return 'Sakura'
    elif fileEXT == 'bif':
        return 'Ventana'
    elif fileEXT == 'tif' or fileEXT == 'tiff':
        value = re.search(r"ImageDescription:(.*)", metadata)
        if value != None:
            tag = value.group(1).strip().lower()
            if re.search(r"\Aaperio", tag):
                return 'Aperio'
        value = re.search(r"Software:(.*)", metadata)
        if value != None:
            tag = value.group(1).strip().lower()
            if re.search(r"\Amedscan", tag) != None:
                return 'Trestle'
            elif re.search(r"\Aphilips", tag) != None:
                return 'Philips'
        value = re.search(r"XMP:(.*)", metadata)
        if value != None:
            tag = value.group(1).strip().lower()
            if re.search(r".*iscan.*", tag) != None and re.search(r".*ventana.*", tag) != None:
                return 'Ventana'
        return 'Tiff'
    else:
        return 'unknown'
    
# print(get_image_type("re re re fidhwihfd \nXMP: p<iscan> gbpfkv <ventana.image> jrjvrv gaaperioNDPI \n lolololol", r"CMU-1.tif"))

# getMetadataAndMakeMiniatureVips(r"C:\Users\KT\inzynierka\testdata\tif\CMU-1.tif", r"C:\Users\KT\inzynierka\testdata\tif\CMU-1.tif")