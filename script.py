# The path can also be read from a config file, etc.
OPENSLIDE_PATH = r'C:\Users\AT\inzynierka\openslide\openslide-win64-20230414\bin'

import os

#dll hell
os.environ['PATH'] = OPENSLIDE_PATH + ";" + os.environ['PATH']

if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
        print("loaded")
else:
    import openslide

slide = openslide.OpenSlide(r'Mirax2-Fluorescence-1.mrxs')
# slide = openslide.OpenSlide(r'DCM_0.dcm')
print(dir(slide))
slide.close()