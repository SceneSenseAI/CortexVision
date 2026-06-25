import cv2
from time import time

from app.pipeline import CortexVisionPipeline
from core.frame import Frame


def main():

    pipeline = CortexVisionPipeline()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    frame_id = 0
    previous_time = time()

    print("===================================")
    print("      CortexVision Demo")
    print("===================================")
    print("Press 'q' to quit.")
    print()

    try:

        while True:

            ret, image = cap.read()

            if not ret:
                print("Failed to capture frame.")
                break

            frame_id += 1

            current_time = time()

            fps = 1.0 / (current_time - previous_time)

            previous_time = current_time

            frame = Frame(
                frame_id=frame_id,
                timestamp=current_time,
                image=image,
                fps=fps,
            )

            world_state, annotated = pipeline.run(
                frame,
                save_outputs=False,
                log_to_mlflow=False,
            )

            cv2.imshow("CortexVision Demo", annotated)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    finally:

        cap.release()
        cv2.destroyAllWindows()

        print("\nDemo finished.")


if __name__ == "__main__":
    main()