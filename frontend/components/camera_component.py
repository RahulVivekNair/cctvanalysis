import streamlit as st
import requests
from io import BytesIO

def render_camera_component(camera_id):
    
    st.header(f"Camera {camera_id+1}")
    st.divider()
    camera_key = f"camera_{camera_id}"  # Unique key based on camera_id  # Display the video
    with st.expander("Camera Settings"):
        source_type = st.selectbox("Source", ["Video", "YouTube Video", "IP Camera", "Webcam"], key=f"{camera_key}_source_type")
        if source_type == "Video":
            uploaded_file = st.file_uploader("Upload File", type=['mp4', 'mov', 'avi'], key=f"{camera_key}_file_uploader")
            if st.button("Upload", key=f"{camera_key}_upload_button"):
                if uploaded_file is not None:
                    with st.spinner("Uploading video..."):
                        # Send the uploaded video to the backend
                        files = {'video': (uploaded_file.name, uploaded_file.getvalue())}
                        response = requests.post(f"http://localhost:8000/upload_video/{camera_id}", files=files)
                        if response.status_code == 200:
                            st.success("Video uploaded successfully!")
                        else:
                            st.error("Failed to upload video.")
        elif source_type in ["YouTube Video", "IP Camera"]:
            link = st.text_input("Enter Link", key=f"{camera_key}_link")
            if link:
                pass
                # Do something with the link (e.g., validate, pass to backend)
        confidence_level = st.slider("Confidence Level", 0.0, 1.0, 0.75, key=f"{camera_key}_confidence_level")
        filter_types = st.selectbox("Filters", ["Crowd Density", "Threat", "Anomaly"], key=f"{camera_key}_filter_types")
        if "Crowd Density" in filter_types:
            st.subheader("Crowd Management Options")
            st.checkbox("Bounding Boxes", key=f"{camera_key}_bounding_boxes")
            st.checkbox("Heatmap", key=f"{camera_key}_heatmap")
            st.checkbox("Trace", key=f"{camera_key}_trace")
            st.checkbox("Label", key=f"{camera_key}_label")
    if st.button("Start Analysis", key=f"{camera_key}_start_analysis"):
    # Collect the necessary settings from Streamlit session state
        data = {
            'confidence_level': confidence_level,
            'bounding_boxes': st.session_state.get(f"{camera_key}_bounding_boxes", False),  # Corrected  
            'heatmap': st.session_state.get(f"{camera_key}_heatmap", False),  
            'trace': st.session_state.get(f"{camera_key}_trace", False),  
            'label': st.session_state.get(f"{camera_key}_label", False) 
        }

        # Ensure that the video has been uploaded before starting the analysis
        if uploaded_file:
            with st.spinner("Analyzing video..."):
                response = requests.post(f"http://localhost:8000/analyze_crowd/{camera_id}", json=data)  # API call change
                if response.status_code == 200:
                    result = response.json()  # Retrieve results in JSON format
                    st.success("Crowd analysis complete!")
                    st.session_state[f"{camera_key}_result"] = result
  # Display received results
                else:
                    st.error("Failed to start crowd analysis.")
    if f"{camera_key}_result" in st.session_state:
        st.video(f"../backend/result/camera_{camera_id}_video.mp4")