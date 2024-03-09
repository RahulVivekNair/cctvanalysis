import streamlit as st

def render_camera_component(camera_id):
    st.header(f"Camera {camera_id+1}")
    st.divider()
    camera_key = f"camera_{camera_id}"  # Unique key based on camera_id

    st.image("assets/placeholder.jpg")
    with st.expander("Camera Settings"):
        source_type = st.selectbox("Source", ["Image", "Video", "YouTube Video", "IP Camera", "Webcam"], key=f"{camera_key}_source_type")
        if source_type in ["Image", "Video"]:
            uploaded_file = st.file_uploader("Upload File", type=["jpg", "png", "mp4"], key=f"{camera_key}_file_uploader")
            if uploaded_file is not None:
                pass  # Do something with the uploaded file (e.g., pass to your backend)

        elif source_type in ["YouTube Video", "IP Camera"]:
            link = st.text_input("Enter Link", key=f"{camera_key}_link")
            if link:
                pass
                # Do something with the link (e.g., validate, pass to backend)
        confidence_level = st.slider("Confidence Level", 0.0, 1.0, 0.75, key=f"{camera_key}_confidence_level")
        filter_types = st.multiselect("Filters", ["Crowd Density", "Threat", "Anomaly"], key=f"{camera_key}_filter_types")
    st.button("Start Analysis", key=f"{camera_key}_start_analysis")