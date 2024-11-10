import os
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader  # Use PdfFileReader for newer PyPDF2 versions

# Function to convert PDF to images in chunks of pages
def pdf_to_images(pdf_path, output_folder, chunk_size=10):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the total number of pages in the PDF
    with open(pdf_path, 'rb') as file:
        reader = PdfFileReader(file)
        total_pages = reader.getNumPages()

    image_paths = []

    # Process in chunks of chunk_size pages
    for chunk_start in range(1, total_pages + 1, chunk_size):
        chunk_end = min(chunk_start + chunk_size - 1, total_pages)

        # Convert the chunk of pages to images
        images = convert_from_path(pdf_path, first_page=chunk_start, last_page=chunk_end)

        # Save each image in the output folder
        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f'page_{chunk_start + i}.png')
            image.save(image_path, 'PNG')
            image_paths.append(image_path)

        print(f"Processed pages {chunk_start} to {chunk_end}")

    return image_paths

# Example usage
pdf_path = '/home/bibrahim/PycharmProjects/Machine Learning/10680 Proforma.pdf'  # Provide your PDF file path
output_folder = '/home/bibrahim/PycharmProjects/Machine Learning/pdf_images'  # Folder to store images

image_paths = pdf_to_images(pdf_path, output_folder)
print(f"Images saved in folder: {output_folder}")
