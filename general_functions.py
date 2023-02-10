import pandas as pd
import numpy as np
import math
pip install asammdf==7.2.0
from asammdf import MDF, Signal

def uploading_files():
    from google.colab import files
    uploaded = files.upload()
    uploaded_files = list(uploaded.keys())
    output_filename = [] 
    for file_name in uploaded_files:
        output_filename.append(file_name.replace('.xlsx', ".mf4"))
    return (uploaded_files, output_filename)
