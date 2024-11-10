import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np
import os


# Make sure to update the tesseract_cmd path according to your Tesseract installation location.
# On Windows:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# On Linux, this might not be necessary.

# Function to convert PDF to images, save them, and return image paths
def pdf_to_images(pdf_path, output_folder):
    # Convert PDF to a list of images (one image per page)
    images = convert_from_path(pdf_path)
    image_paths = []

    for i, img in enumerate(images):
        # Convert image to a numpy array
        img_np = np.array(img)

        # Define path to save the image
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")

        # Save the numpy array as an image using OpenCV
        cv2.imwrite(image_path, img_np)

        # Store the image path
        image_paths.append(image_path)

    return image_paths


# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    # Read the image file using OpenCV
    img = cv2.imread(image_path)

    # Convert the image to string using Tesseract
    text = pytesseract.image_to_string(img)

    return text


# Main function to handle the workflow
def pdf_to_text(pdf_path, output_folder):
    # Step 1: Convert PDF to images and save them
    image_paths = pdf_to_images(pdf_path, output_folder)

    # Step 2: Extract text from each image and concatenate results
    full_text = ""
    for image_path in image_paths:
        text = extract_text_from_image(image_path)
        full_text += f"Text from {os.path.basename(image_path)}:\n{text}\n"

    return full_text


# Example usage
if __name__ == "__main__":
    # Path to the PDF file
    pdf_path = "/home/bibrahim/PycharmProjects/Machine Learning/0594_241009090035_001.pdf"

    # Folder to save the output images
    output_folder = "/home/bibrahim/PycharmProjects/Machine Learning/images-test"

    # Create the output folder if it doesn't exist
    # os.makedirs(output_folder, exist_ok=True)

    # Extract text from the PDF
    # extracted_text = pdf_to_text(pdf_path, output_folder)
    #
    # # Optionally save the extracted text to a file
    # with open(os.path.join(output_folder, "extracted_text.txt"), "w") as text_file:
    #     text_file.write(extracted_text)
    #
    # print("Text extraction complete. Check the output folder for results.")


    text = extract_text_from_image("/home/bibrahim/PycharmProjects/Machine Learning/images-test/page_2.png")
    print(text)