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

def getMetadataAndMakeMiniatureVips(path, pathForMiniature):
    miniature_size = 256
    isMiniatured = True
    pathJPG = get_miniature_suffix(pathForMiniature)
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
            try:
                value = value.decode()
            except (UnicodeDecodeError, AttributeError):
                pass
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
    
def get_miniature_suffix(data):
    fileEXT = "." + data.split('.')[-1]
    if fileEXT in ['.jpg', '.jpeg']:
        miniatureURL = data.replace(fileEXT, 'Miniature$$#%^&.jpg')
    else:
        miniatureURL = data.replace(fileEXT, '.jpg')
    return miniatureURL