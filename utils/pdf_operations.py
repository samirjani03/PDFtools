import os
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
import img2pdf

def pdf_to_jpg(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    jpg_paths = []
    for i, image in enumerate(images):
        jpg_path = os.path.join(output_folder, f'page_{i+1}.jpg')
        image.save(jpg_path, 'JPEG')
        jpg_paths.append(jpg_path)
    return jpg_paths

def jpg_to_pdf(jpg_paths, output_path):
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(jpg_paths))

def encrypt_pdf(pdf_path, output_path, password):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open(output_path, "wb") as f:
        writer.write(f)

def decrypt_pdf(pdf_path, output_path, password):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    if reader.is_encrypted:
        try:
            reader.decrypt(password)
        except:
            raise ValueError("Incorrect password")

    for page in reader.pages:
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)
def merge_pdfs(pdf_paths, output_path):
    writer = PdfWriter()

    for pdf_path in pdf_paths:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

def split_pdf(pdf_path, output_folder):
    reader = PdfReader(pdf_path)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        output_path = os.path.join(output_folder, f"page_{i+1}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

# Add more PDF operations as needed