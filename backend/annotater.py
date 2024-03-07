from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import cv2
import base64
import supervision as sv
from ultralytics import YOLO 
import numpy as np

model = YOLO("yolov8n.pt")  # Load your YOLOv8 model
model.to(device='cuda')
app = FastAPI()

@app.post('/annotate')
async def annotate_image(file: UploadFile = File(...)):
    image_bytes = await file.read()

    # Convert bytes to OpenCV image format
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  

    # Perform YOLO inference
    results = model(image)[0]
    detections = sv.Detections.from_ultralytics(results)

    # Create annotators
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    # Get labels
    labels = [
        model.model.names[class_id]
        for class_id
        in detections.class_id
    ]

    # Annotate the image
    annotated_image = bounding_box_annotator.annotate(
        scene=image, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections, labels=labels)

    # Convert annotated image back to bytes for sending
    # Or '.png' if needed

    ret, buffer = cv2.imencode('.jpg', annotated_image)  
    image_bytes = buffer.tobytes()

    # Encode as base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')  

    return {"image": image_base64} 