import io
import os
from PIL import Image as PILImage, ImageDraw, ImageFont

from ..exceptions import UnsupportedFileTypeException


class Image:
    supported_extensions = [".png", ".jpeg", ".jpg"]

    @classmethod
    def is_image(cls, object_key):
        """
        Validate current object is a pdf
        """
        _, file_extension = os.path.splitext(object_key.lower())

        return file_extension in cls.supported_extensions

    @staticmethod
    def supported_file_type(data_list):
        """
        Check if object in data list is supported
        """
        for data in data_list:
            if not Image.is_image(data["ObjectKey"]):
                raise UnsupportedFileTypeException(
                    f"Image File type not supported only: {str(Image.supported_extensions)} is allowed")

    @classmethod
    def convert_image_to_pdf(cls, image_data):
        image = PILImage.open(io.BytesIO(image_data))
        rgb_image_converter = image.convert('RGB')

        # create bytes buffer to save converted image
        pdf_bytes = io.BytesIO()
        rgb_image_converter.save(pdf_bytes, 'PDF', resolution=100.0)
        # go to the beginning of the bytes
        pdf_bytes.seek(0)

        return pdf_bytes

    @classmethod
    def create_watermark(cls, text, size=(210, 297), font_size=16, opacity=128):
        image_width, image_height = size
        watermark_image = PILImage.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_image)

        # set the font size
        font = ImageFont.truetype("cpp_aws_s3_pdf/fonts/Lato-Regular.ttf", size=font_size)
        left, top, right, bottom = font.getbbox(text)
        text_width, text_height = right - left, bottom - top
        position = ((image_width - text_width) / 2, (image_height - text_height) / 2)
        draw.text(position, text, fill=(205, 209, 228, opacity), font=font)

        pdf_bytes = io.BytesIO()

        # Save the image
        watermark_image.save(pdf_bytes, "PDF")
        pdf_bytes.seek(0)

        return pdf_bytes
