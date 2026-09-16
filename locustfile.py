from locust import HttpUser, task, between
import os
import base64
import uuid
import random
import json

class PoseUser(HttpUser):
    wait_time = between(1, 2)  # Each user waits 1 to 2 seconds between 
requests

    # Preload all images at the start
    def on_start(self):
        self.images = []
        image_dir = os.path.expanduser("~/inputfolder")
        for filename in os.listdir(image_dir):
            if filename.endswith(".jpg"):
                with open(os.path.join(image_dir, filename), "rb") as 
image_file:
                    encoded = 
base64.b64encode(image_file.read()).decode("utf-8")
                    img_id = str(uuid.uuid5(uuid.NAMESPACE_OID, filename))
                    self.images.append({
                        "id": img_id,
                        "image": encoded
                    })

    @task(1)
    def send_pose_request_json(self):
        # Send a request to /api/pose_estimation to receive keypoints in JSON
        if self.images:
            data = random.choice(self.images)
            self.client.post("/api/pose_estimation", json=data, timeout=10)

    @task(1)
    def send_pose_request_annotated(self):
        # Send a request to /api/pose_estimation_annotation to receive annotated image
        if self.images:
            data = random.choice(self.images)
            self.client.post("/api/pose_estimation_annotation", json=data,timeout=10)
