import os
from PIL import Image

VIPS_PATH = r'C:\Users\KT\inzynierka\vips\vips-dev-8.14\bin'

os.environ['PATH'] = VIPS_PATH + ";" + os.environ['PATH']

if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(VIPS_PATH):
        import pyvips
        print("loaded")
else:
    import pyvips

def getMetadataAndMakeMiniatureMRX(path):
    miniature_size = 256
    isMiniatured = True
    pathJPG = path.replace('.mrxs','.jpg')
    try:
        image = pyvips.Image.new_from_file(path, access='sequential')
        metadata = ""
        fields = image.get_fields()
        for field in fields:
            value = image.get(field)
            metadata += f"{field}: {value}\n"
    except Exception:
        return ("There was an error reading file", False)
    finally:
        try:
            out = pyvips.Image.thumbnail(path, miniature_size)
            out.write_to_file(pathJPG)
        except Exception:
            isMiniatured = False
        return (metadata, isMiniatured)


# filein='Mirax2-Fluorescence-1/Mirax2-Fluorescence-1.mrxs'
# fileout='Mirax.jpg'
# scale=1 

# resize(filein=filein, fileout=fileout, scale=scale)