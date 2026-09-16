from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID
import time
import os
import uuid
import tempfile

from utils import decode_base64_image, encode_image_to_base64
from pose_detection import predict

app = FastAPI()

class ImageRequest(BaseModel):
    id: UUID
    image: str  # base64 encoded string

@app.post("/api/pose_estimation")
async def pose_json_api(request: ImageRequest):
    try:
        # 1. Decode the base64 image into a PIL Image
        img = decode_base64_image(request.image)

        # 2. Generate temporary file paths
        temp_dir = tempfile.gettempdir()
        img_id = str(uuid.uuid4())
        input_path = os.path.join(temp_dir, f"{img_id}_input.jpg")
        output_path = os.path.join(temp_dir, f"{img_id}_output.jpg")

        # 3. Save the image to the temporary location
        img.save(input_path)

        # 4. Call the model for inference
        start_pre = time.time()
        model_path = 'movenet-full-256.tflite'  # Ensure the model is in the same directory
        start_infer = time.time()
        keypoints = predict(model_path, input_path, output_path)
        end_infer = time.time()
        end_post = time.time()

        # 5. Organize keypoints and box information
        people_count = 1  # MoveNet detects only one person
        boxes = []

        if len(keypoints) > 0:
            # Calculate the bounding box (minimum enclosing all keypoints)
            x_coords = [kp[1] for kp in keypoints[0]]
            y_coords = [kp[0] for kp in keypoints[0]]
            confidences = [kp[2] for kp in keypoints[0]]

            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            prob = sum(confidences) / len(confidences)

            box = {
                "x": float(round(x_min, 4)),
                "y": float(round(y_min, 4)),
                "width": float(round(x_max - x_min, 4)),
                "height": float(round(y_max - y_min, 4)),
                "probability": float(round(prob, 4))
            }
            boxes.append(box)

        # 6. Create the response data
        response = {
            "id": str(request.id),
            "count": people_count,
            "boxes": boxes,
            "keypoints": [kp.tolist() for kp in keypoints],  # (1, 17, 3) → list
            "speed_preprocess": round(start_infer - start_pre, 4),
            "speed_inference": round(end_infer - start_infer, 4),
            "speed_postprocess": round(end_post - end_infer, 4)
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/pose_estimation_annotation")
async def pose_image_api(request: ImageRequest):
    try:
        # Decode image from base64
        img = decode_base64_image(request.image)

        # Save image to temp file
        temp_dir = tempfile.gettempdir()
        img_id = str(uuid.uuid4())
        input_path = os.path.join(temp_dir, f"{img_id}_input.jpg")
        output_path = os.path.join(temp_dir, f"{img_id}_output.jpg")
        img.save(input_path)

        # Run pose estimation (predict will save annotated image)
        model_path = "movenet-full-256.tflite"
        predict(model_path, input_path, output_path)

        # Read and encode annotated image to base64
        annotated_base64 = encode_image_to_base64(output_path)

        return {
            "id": str(request.id),
            "image": annotated_base64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


