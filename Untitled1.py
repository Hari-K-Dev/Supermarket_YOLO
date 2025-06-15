from ultralytics import YOLO
from ultralytics.solutions import object_counter
import cv2

# Initialize YOLO model
model = YOLO("best.pt")


# Set up your video source
cap = cv2.VideoCapture(0)
classes_to_count = [0, 2,18] 
# Initialize Object Counter for your line
line_pedestrian_1 =  [(100, 100), (600, 100), (600, 360), (100, 360)]  # Define as per your need
counter = object_counter.ObjectCounter()
counter.set_args(view_img=True, reg_pts=line_pedestrian_1, classes_names=model.names)

while cap.isOpened():
    ret, im0 = cap.read()
    if not ret:
        break

    # Track objects
    results = model.track(im0,persist=True, show=False, classes=classes_to_count)

    # Start counting based on tracks and your line
    im0 = counter.start_counting(im0, results)

    # Display
    cv2.imshow("Count", im0)
    if cv2.waitKey(1) == ord('q'):  # press q to quit
        break

cap.release()
cv2.destroyAllWindows()
