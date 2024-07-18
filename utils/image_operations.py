from PIL import Image
import os

def jpg_to_png(jpg_path, output_path):
    with Image.open(jpg_path) as img:
        img.save(output_path, 'PNG')

def png_to_jpg(png_path, output_path):
    with Image.open(png_path) as img:
        rgb_im = img.convert('RGB')
        rgb_im.save(output_path, 'JPEG')

def resize_image(image_path, output_path, size):
    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(output_path)

# Add more image operations as needed