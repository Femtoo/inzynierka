import pydicom as dicom
from PIL import Image
import numpy as np
import math
STORAGE_PATH = r'C:\Users\KT\inzynierka\storage'

def getAttributesAndMakeMiniature(path):
    isMiniatured = True
    miniature_size = 256, 256
    pathJPG = path.replace('.dcm','.jpg')
    try:
        ds = dicom.dcmread(path)
    except Exception:
        return ("", False)
    finally:
        try:
            shape = ds.pixel_array.shape
            if(len(shape) == 4):
                num_columns = int(math.sqrt(shape[0]))
                frames = ds.pixel_array
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
                image = ds.pixel_array
                im = Image.fromarray(image)
                im.thumbnail(miniature_size, Image.Resampling.LANCZOS)
                im.save(pathJPG,"JPEG")
        except Exception:
            isMiniatured=False
        return (str(ds),isMiniatured)

# print(getAttributesAndMakeMiniature('DCM_0.dcm'))
# metadata, ismin = getAttributesAndMakeMiniature('DCM_1.dcm')
# print(ismin)
# print(metadata)
    