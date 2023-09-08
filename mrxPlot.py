import sys
import os

VIPS_PATH = r'C:\Users\KT\inzynierka\vips\vips-dev-8.14\bin'

os.environ['PATH'] = VIPS_PATH + ";" + os.environ['PATH']

if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(VIPS_PATH):
        import pyvips
        print("loaded")
else:
    import pyvips

def resize(filein, fileout, scale):
    image = pyvips.Image.new_from_file(filein, access='sequential')

    fields = image.get_fields()
    for field in fields:
        value = image.get(field)
        print(f"{field}: {value}")
    # out = pyvips.Image.resize(image, scale)
    # out.write_to_file(fileout)

filein='Mirax2-Fluorescence-1/Mirax2-Fluorescence-1.mrxs'
fileout='Mirax.jpg'
scale=1 # this will scale it down to 25% of original

resize(filein=filein, fileout=fileout, scale=scale)