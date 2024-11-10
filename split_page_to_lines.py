import cv2
import pytesseract
import numpy as np

# Step 1: Load the image
image_path = r'/home/bibrahim/PycharmProjects/Machine Learning/pdf_images/page_4.png'
image = cv2.imread(image_path)

# Check if the image is None
if image is None:
    raise ValueError("Invalid image file or path.")

# Step 2: Preprocess the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Select a kernel with more width to connect lines
kernel_size = (15, 1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

# Step 3: Perform the closing operation: Dilate and then close
bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

# Find contours for each text line
contours, _ = cv2.findContours(bw_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours to select those whose width is at least 3 times its height
filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 3.0]

# Sort contours based on y-coordinate
sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])

# Get the full width of the image
image_width = image.shape[1]
padding = 3

cropping = []

for contour in sorted_contours:
    # Use the full width of the image for each bounding box
    _, y, _, h = cv2.boundingRect(contour)
    x, y, w, h = (0, y - padding, image_width, h + 2 * padding)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Crop the line using the full width and recognize text
    if (y,y + h, x,x + w) not in cropping:
        cropping.append((y,y + h, x,x + w))
        line_image = image[y:y + h, x:x + w]
        cv2.imshow('Text Lines', line_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        line_text = pytesseract.image_to_string(line_image)
        print(line_text)
    else:
        print("Line already detected")

# Display and save the image with bounding boxes
cv2.imshow('Text Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('opencv_detect_text_lines.jpg', image)
