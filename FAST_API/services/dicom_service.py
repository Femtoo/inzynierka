import logging
import pydicom as dicom
from pydicom.pixel_data_handlers import convert_color_space
from PIL import Image
import numpy as np
import math
import re

logger = logging.getLogger("main_logger")

def getAttributesAndMakeMiniatureDCM(path, pathForMiniature):
    isMiniatured = True
    miniature_size = 256, 256
    pathJPG = pathForMiniature.replace('.dcm','.jpg')
    filename = path.split('\\')[-1]
    logger.info(f"Reading file {filename}")

    try:
        ds = dicom.dcmread(path)
        # print(str(ds))
    except Exception:
        logger.error(f"Error reading file {filename}")
        return ("There was an error reading file", False)
    finally:
        try:
            logger.info(f"Making miniature for file {filename}")
            shape = ds.pixel_array.shape
            pixel_array = ds.pixel_array
            photometric_interpretation = ds.PhotometricInterpretation
            if re.search(".*YBR_FULL_422.*", photometric_interpretation):
                print("in")
                pixel_array = convert_color_space(pixel_array, "YBR_FULL_422", "RGB", True)
            elif re.search(".*YBR_FULL.*", photometric_interpretation):
                pixel_array = convert_color_space(pixel_array, "YBR_FULL", "RGB", True)
            if(len(shape) == 4):
                num_columns = int(math.sqrt(shape[0]))
                frames = pixel_array
                num_frames = frames.shape[0]

                # Calculate the number of rows needed for the grid
                num_rows = (num_frames + num_columns - 1) // num_columns

                # Create an empty list to store individual frame images
                frame_images = []

                for frame_idx in range(num_frames):
                    frame = frames[frame_idx]
                    frame_image = Image.fromarray(frame)
                    frame_images.append(frame_image)

                # Calculate the size of each grid cell
                cell_width = frame_images[0].width
                cell_height = frame_images[0].height

                # Create a blank grid image
                grid_width = num_columns * cell_width
                grid_height = num_rows * cell_height
                grid_image = Image.new("RGB", (grid_width, grid_height))

                # Paste each frame image into the grid
                for frame_idx, frame_image in enumerate(frame_images):
                    row = frame_idx // num_columns
                    col = frame_idx % num_columns
                    x_offset = col * cell_width
                    y_offset = row * cell_height
                    grid_image.paste(frame_image, (x_offset, y_offset))

                # grid_image.show()  # Display the grid image
                grid_image.thumbnail(miniature_size, Image.Resampling.LANCZOS)
                grid_image.save(pathJPG,"JPEG")
            else:
                image = pixel_array
                im = Image.fromarray(image)
                im.thumbnail(miniature_size, Image.Resampling.LANCZOS)
                im.save(pathJPG,"JPEG")
        except Exception as e:
            print(e)
            logger.error(f"Error making miniature for file {filename}")
            isMiniatured=False
        return (str(ds),isMiniatured)

# getAttributesAndMakeMiniatureDCM(r'C:\Users\KT\inzynierka\testdata\DCM_1.dcm')
# metadata, ismin = getAttributesAndMakeMiniature('DCM_1.dcm')
# print(ismin)
# print(metadata)
    