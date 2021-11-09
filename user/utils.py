from io import BytesIO
from pathlib import Path

from PIL import Image
from django.core.files import File
from django.utils.translation import ugettext as _


def resize_image(image, width, height):
    # Open the image using Pillow
    img = Image.open(image)
    img_format = img.format
    # if it is not a square
    if img.width > width or img.height > height or abs(img.height - img.width) >= 2:
        # Get dimensions
        width_org, height_org = img.size
        # Determine max edge size
        limit = width_org if width_org <= height_org else height_org
        # Calculate cropping values to get square image
        left = (width_org - limit) / 2
        top = (height_org - limit) / 2
        right = (width_org + limit) / 2
        bottom = (height_org + limit) / 2
        # crop unwanted edges
        img = img.crop((left, top, right, bottom))

        output_size = (width, height)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
    # Find the file name of the image
    img_filename = Path(image.file.name).name
    # Save the resized image into the buffer, noting the correct file type
    buffer = BytesIO()
    img.save(buffer, format=img_format, quality=85, progressive=True)
    # Wrap the buffer in File object
    resized_image = File(buffer, name=img_filename)
    # Save the new resized file as usual, which will save to S3 using django-storages
    return resized_image