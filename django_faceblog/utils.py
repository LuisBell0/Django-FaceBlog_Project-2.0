from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


def compress_image(image_field, max_size=(800, 800), quality=70):
    """Compresses and resizes an image before saving it."""
    if not image_field:
        return image_field

    img = Image.open(image_field)
    img_format = img.format

    # Convert PNG to JPEG to reduce size
    if img_format == "PNG":
        img = img.convert("RGB")
        img_format = "JPEG"

    # Resize image while maintaining aspect ratio
    img.thumbnail(max_size, Image.LANCZOS)

    # Save the compressed image to a BytesIO buffer
    buffer = BytesIO()
    img.save(buffer, format=img_format, quality=quality, optimize=True)

    # Return the new image file
    return ContentFile(buffer.getvalue(), name=os.path.basename(image_field.name))
