import pydicom as dicom
import os
import PIL # optional
import pandas as pd
import csv
STORAGE_PATH = r'C:\Users\KT\inzynierka\storage'

def getAttributesAndMakeMiniature(path):
    try:
        ds = dicom.dcmread(path)
    except Exception:
        return ("", False)
    finally:
        # print(str(ds))
        return (str(ds),True)

# print(getAttributesAndMakeMiniature('DCM_0.dcm'))
# getAttributesAndMakeMiniature('DCM_0.dcm')
    