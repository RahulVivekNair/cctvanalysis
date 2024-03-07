import streamlit as st
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import base64
import json

st.header("cctv", divider='rainbow')
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    if st.button("Process Image"):
        with st.spinner("Processing image..."):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("http://localhost:8000/annotate", files=files)

            if response.status_code == 200:
              image_data = json.loads(response.content)  # Load JSON data 
              image_base64 = image_data["image"]         # Extract the base64 string
              image_bytes = base64.b64decode(image_base64) 
              processed_image = Image.open(BytesIO(image_bytes))
              st.image(processed_image, caption='Processed Image', use_column_width=True)
            else:
                st.error("Image processing failed.")