from pypdf import PdfWriter, PdfReader
import io

from ..exceptions import UnsupportedFileTypeException


class PDF:
    allowed_content_type = ['application/pdf']

    @classmethod
    def is_pdf(cls, object_key, content_type):
        """
        Validate current object is a pdf
        """
        return object_key.lower().endswith('.pdf') or content_type in cls.allowed_content_type

    @staticmethod
    def supported_file_type(data_list):
        """
        Check if object in data list is supported
        """
        for data in data_list:
            if not PDF.is_pdf(data["ObjectKey"], data["ContentType"]):
                raise UnsupportedFileTypeException(
                    f"File type not supported only: {str(PDF.allowed_content_type)} is allowed")

    @staticmethod
    def apply_watermark(watermark_data, file_data):
        # Open the watermark image
        watermark_page = PdfReader(watermark_data).pages[0]
        pdf_writer = PdfWriter(clone_from=io.BytesIO(file_data))

        for page in pdf_writer.pages:
            page.merge_page(watermark_page, over=False)  # here set to False for watermarking

        watermarked_data = io.BytesIO()

        pdf_writer.write(watermarked_data)

        watermarked_data.seek(0)
        return watermarked_data

    @staticmethod
    def combine_files(objects_data):
        pdf_writer = PdfWriter()

        for data in objects_data:
            # read each file into a stream
            object_bytes = io.BytesIO(data)
            object_read_pdf = PdfReader(object_bytes)

            pdf_writer.append_pages_from_reader(object_read_pdf)

        merged_pdf = io.BytesIO()
        pdf_writer.write(merged_pdf)
        merged_pdf.seek(0)

        return merged_pdf
