import streamlit as st
import tensorflow as tf
import pandas as pd
import cv2
from PIL import Image, ImageOps
import numpy as np
import subprocess
import os 
from werkzeug.utils import secure_filename, send_from_directory
import zipfile

def create_zip_file(folder_path):
    # Create a zip file object in write mode
    zip_file = zipfile.ZipFile("my_folder.zip", "w")

    # Iterate over all the files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Add each file to the zip file
            zip_file.write(os.path.join(root, file))

    # Close the zip file
    zip_file.close()

# Define the folder path to download
folder_path = "static"
files =  os.listdir(folder_path)
# Loop through the files and delete each one
for file in files:
    file_path = os.path.join(folder_path, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

#Allow cache in the application for prediction 
st.cache(allow_output_mutation=True)

#Frontend texts
st.markdown("<h1 style='text-align: center;'> PCB defect detection</h1>", unsafe_allow_html=True)


instructions = """
                Please upload your PCB images here.
                The image you select or upload will be fed through the 
                Deep Neural Network in real-time and the output will be displayed to the screen.
                """
st.write(instructions)

#File uploader with multiple upload option
file = st.file_uploader("Upload the image to be classified \U0001F447", type=["jpg", "png","jpeg"], accept_multiple_files=True)

st.set_option('deprecation.showfileUploaderEncoding', False)

if file is None:
    st.text("Please upload an image file")
else:
    #Loop through the List, "files", to classify every image uploaded
    for img_upload in (file):
        with open(os.path.join("uploads",img_upload.name),"wb") as f: 
            f.write(img_upload.getbuffer()) 
        subprocess.run("dir", shell=True)
        subprocess.run(['python', 'detect.py','--source', os.path.join('uploads', secure_filename(img_upload.name))], shell=True)

        filename = secure_filename(img_upload.name)
        st.image('static'+'/' +filename, use_column_width=True, caption=img_upload.name)
        print("img============",img_upload)
# Create a download button
# if st.button("Download Folder"):
    create_zip_file(folder_path)

    # Download the zip file
    if len(file)>0:
        st.success("image detected successfully!")

        with open("my_folder.zip", "rb") as f:
            bytes_data = f.read()
            st.text("you can download the predited images by clicking on download button")
            st.download_button(label="Download Folder", data=bytes_data, file_name="my_folder.zip", mime="application/zip")
