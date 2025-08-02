#################################################
# Facial Image Collector
# This script collects facial images for a user 
# and saves them in a specified directory.
# Author: Shrayanendra Nath Mandal
# Date: 2023-10-01
# Version: 1.0
##################################################
import cv2
import uuid
import logging
from pathlib import Path
from datetime import datetime

class FaceCollector:
    def __init__(self, user_name: str, num_images: int = 100, output_dir: str = "Datasets", log_dir: str = "logs"):
        self.user_name = user_name
        self.num_images = num_images
        self.output_dir = Path(output_dir)
        self.user_id = str(uuid.uuid4())
        self.user_folder = self.output_dir / f"{self.user_name}_{self.user_id}"
        self.user_folder.mkdir(parents=True, exist_ok=True)

        # Set up logs
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = Path(log_dir) / f"{self.user_name}_{timestamp}.log"
        logging.basicConfig(
            filename=log_filename,
            filemode='w',
            level=logging.INFO,
            format='%(asctime)s — %(levelname)s — %(message)s'
        )
        self.logger = logging.getLogger()

        # Face detection setup
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.cap = cv2.VideoCapture(0)

    def _detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return gray, faces

    def _save_face(self, face_img, count):
        img_path = self.user_folder / f"{self.user_name}_{count:03d}.jpg"
        cv2.imwrite(str(img_path), face_img)
        self.logger.info(f"Saved image: {img_path}")

    def collect(self):
        self.logger.info(f"Starting collection for {self.user_name} (UUID: {self.user_id})")
        count = 0

        while count < self.num_images:
            ret, frame = self.cap.read()
            if not ret:
                self.logger.error("Failed to read frame.")
                break

            gray_frame, faces = self._detect_faces(frame)
            for (x, y, w, h) in faces:
                face_img = gray_frame[y:y+h, x:x+w]  # Grayscale face crop
                self._save_face(face_img, count)
                count += 1
                if count >= self.num_images:
                    break

            cv2.imshow("Face Capture (Grayscale Preview)", gray_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.logger.info("Collection interrupted by user.")
                break

        self.cap.release()
        cv2.destroyAllWindows()
        self.logger.info(f"Collection complete. {count} grayscale face images saved in {self.user_folder}")
        self.logger.info(f"User ID: {self.user_id}, Folder: {self.user_folder}")
        print(f"Collection complete. {count} grayscale face images saved in {self.user_folder}")
        return self.user_id, self.user_folder
