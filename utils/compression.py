from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io

def compress_pdf(input_path, output_path, quality=90):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

def compress_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img.save(output_path, optimize=True, quality=quality)

# Add more compression operations as needed