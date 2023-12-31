import os
from PIL import Image

VIPS_PATH = r'C:\Users\KT\inzynierka\vips\vips-dev-8.14\bin'

os.environ['PATH'] = VIPS_PATH + ";" + os.environ['PATH']

if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(VIPS_PATH):
        import pyvips
else:
    import pyvips

def getMetadataAndMakeMiniatureMRX(path):
    miniature_size = 256
    isMiniatured = True
    pathJPG = path.replace('.mrxs','.jpg')
    metadata = ""
    # header = pyvips.Image.header(path)
    # print(header)
    try:
        image = pyvips.Image.new_from_file(path, access='sequential')
        # image.dzsave('overview.jpg', suffix=".jpg", tile_size=256, overlap=0, centre=True, skip_blanks=1)
        # print(str(image.get_fields()))
        fields = image.get_fields()
        for field in fields:
            value = image.get(field)
            metadata += f"{field}: {value}\n"
        # print(metadata)
    except Exception as e:
        print(e)
        return ("There was an error reading file", False)
    finally:
        try:
            out = pyvips.Image.thumbnail(path, miniature_size)
            out.write_to_file(pathJPG)
        except Exception as e:
            print(e)
            isMiniatured = False
        return (metadata, isMiniatured)


# filein=r'C:\Users\KT\inzynierka\testdata\mirax\Mirax2-Fluorescence-1.mrxs'
# getMetadataAndMakeMiniatureMRX(filein)
# fileout='Mirax.jpg'
# scale=1 

# resize(filein=filein, fileout=fileout, scale=scale)