import cv2
import os
from ultralytics import YOLOv10

# Load the YOLO model
model = YOLOv10('./runs-186/detect/train/weights/last.pt')

# Path to the input and output folders
input_folder = 'test'  # Folder containing input images
output_folder = 'output_images'  # Folder to save output images

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all image files in the input folder
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]


# Process each image
for image_file in image_files:
    # Load the image
    image_path = os.path.join(input_folder, image_file)
    frame = cv2.imread(image_path)

    # Check if image is loaded correctly
    if frame is None:
        print(f"Error loading image {image_file}")
        continue

    # Apply YOLO object detection using the predict method
    results = model.predict(source=frame) # Correct method for YOLO v8+ versions

    # Iterate through the detections and draw bounding boxes
    for result in results:  # YOLOv8 results are typically iterable
        boxes = result.boxes  # Bounding boxes
        for box in boxes:
            conf = box.conf.cpu().numpy()  # Confidence score

            if conf[0] > 0.5:  # Only proceed if confidence is greater than 0.5
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Bounding box coordinates
                cls = box.cls.cpu().numpy()  # Class ID

                label = f'{model.names[int(cls)]} {conf[0]:.2f}'

                # Draw bounding box and label on the image
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)  # Bounding box
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Save the processed image to the output folder
    output_image_path = os.path.join(output_folder, image_file)
    cv2.imwrite(output_image_path, frame)

#     print(f'Processed {image_file}')
#
# print(f'All images processed and saved to {output_folder}')
