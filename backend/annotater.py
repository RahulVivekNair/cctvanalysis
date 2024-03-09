import os
from fastapi import FastAPI, File, UploadFile
import cv2
import supervision as sv
from ultralytics import YOLO
import numpy as np
app = FastAPI()

@app.post("/upload_video/{camera_id}")
async def upload_video(camera_id: int, video: UploadFile = File(...)):
    # Generate a unique filename for the uploaded video
    _, ext = os.path.splitext(video.filename)
    filename = f"camera_{camera_id}_video{ext}"
    
    # Save the uploaded video to a temporary folder
    file_path = os.path.join("temp/", filename)
    
    with open(file_path, "wb") as file:
        content = await video.read()
        file.write(content)
    
    return {"message": "Video uploaded successfully"}

@app.post("/analyze_crowd/{camera_id}")
async def analyze_crowd(camera_id: int, data: dict):
    # Load the video from the temporary folder
    file_path = f"temp/camera_{camera_id}_video.mp4"
    video = cv2.VideoCapture(file_path)
    
    # Load the YOLOv5 model
    model = YOLO("models/yolov8n.pt")

    heat_map_annotator = sv.HeatMapAnnotator(
        position=sv.Position.BOTTOM_CENTER,
        opacity=0.5,
        radius=25,
        kernel_size=25,
        top_hue=0,
        low_hue=125,
    )
    label_annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER)
    corner_annotator = sv.BoxCornerAnnotator()
    trace_annotator = sv.TraceAnnotator()
    cap = cv2.VideoCapture(file_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()

    byte_tracker = sv.ByteTrack(
        track_thresh=0.35,
        track_buffer=5 * fps,
        match_thresh=0.99,
        frame_rate=fps,
    )
    video_info = sv.VideoInfo.from_video_path(video_path=file_path )
    frames_generator = sv.get_video_frames_generator(
        source_path=file_path , stride=1
    )
    with sv.VideoSink(target_path=f"result/camera_{camera_id}_video.mp4", video_info=video_info,codec="H264") as sink:
        for frame in frames_generator:
            result = model(
                source=frame,
                classes=[0],  # only person class
                conf=data["confidence_level"],
                iou=0.5,
                # show_conf = True,
                # save_txt = True,
                # save_conf = True,
                # save = True,
                device=0,  # use None = CPU, 0 = single GPU, or [0,1] = dual GPU
            )[0]

            detections = sv.Detections.from_ultralytics(result)  # get detections

            detections = byte_tracker.update_with_detections(
                detections
            )  # update tracker

            annotated_frame = frame.copy()  # Start with a fresh copy in every iteration

            if data["heatmap"]:
                annotated_frame = heat_map_annotator.annotate(
                    scene=annotated_frame, detections=detections
                )

            if data["trace"]:
                annotated_frame = trace_annotator.annotate(
                    scene=annotated_frame, detections=detections
                )

            if data["bounding_boxes"]:
                annotated_frame = corner_annotator.annotate(
                    scene=annotated_frame, detections=detections
                )
            if data["label"]:
            ### draw other attributes from `detections` object
                labels = [
                    f"#{tracker_id}"
                    for class_id, tracker_id in zip(
                        detections.class_id, detections.tracker_id
                    )
                ]
                
                label_annotator.annotate(
                    scene=annotated_frame, detections=detections, labels=labels
                )

            sink.write_frame(frame=annotated_frame)
    # Perform crowd analysis
    print(data)
    
    # Return the results
    return {"message": "Crowd analysis complete"}
