import cv2
import numpy as np
from pathlib import Path


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = PROJECT_ROOT / "models"
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"

YUNET_MODEL = MODEL_DIR / "face_detection_yunet_2023mar.onnx"
SFACE_MODEL = MODEL_DIR / "face_recognition_sface_2021dec.onnx"


def main():
    # Find the first image inside input/
    image_files = []
    for extension in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        image_files.extend(INPUT_DIR.glob(extension))

    if not image_files:
        print("ERROR: Put a JPG/PNG image inside the input folder.")
        return

    image_path = image_files[0]
    print(f"Input image: {image_path}")

    # Load image
    image = cv2.imread(str(image_path))

    if image is None:
        print("ERROR: Could not read the image.")
        return

    height, width = image.shape[:2]

    # Create YuNet face detector
    detector = cv2.FaceDetectorYN.create(
        str(YUNET_MODEL),
        "",
        (width, height),
        0.9,
        0.3,
        5000
    )

    # Detect faces
    detector.setInputSize((width, height))
    _, faces = detector.detect(image)

    if faces is None:
        print("No face detected.")
        return

    print(f"Faces detected: {len(faces)}")

    # Create SFace recognizer
    recognizer = cv2.FaceRecognizerSF.create(
        str(SFACE_MODEL),
        ""
    )

    # Draw results
    output = image.copy()

    for index, face in enumerate(faces):
        x, y, w, h = face[:4].astype(int)

        # Draw bounding box
        cv2.rectangle(
            output,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Extract face feature
        aligned_face = recognizer.alignCrop(image, face)
        feature = recognizer.feature(aligned_face)

        # Save embedding
        embedding_path = OUTPUT_DIR / f"face_{index + 1}_embedding.npy"
        np.save(str(embedding_path), feature)

        # Label
        cv2.putText(
            output,
            f"Face {index + 1}",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        print(f"Face {index + 1} embedding shape: {feature.shape}")
        print(f"Saved: {embedding_path}")

    # Save annotated image
    output_path = OUTPUT_DIR / "detected_faces.jpg"
    cv2.imwrite(str(output_path), output)

    print()
    print("SUCCESS!")
    print(f"Annotated image: {output_path}")


if __name__ == "__main__":
    main()