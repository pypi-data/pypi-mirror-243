from datetime import datetime
import io

from .utils.aws_s3 import S3
from .utils.pdf import PDF
from .utils.image import Image
from .exceptions import S3PDFException


class S3Pdf:
    """
    S3Pdf Python utility for combining objects from Amazon S3 into a single PDF file.
    Ideal for users who need to aggregate content stored in S3 buckets and generate consolidated PDF documents
    for reports, archives, or data presentation.
    """

    def __init__(self, bucket_name, region=None):
        self.bucket_name = bucket_name
        self.s3_client = S3(bucket_name=bucket_name, region=region)

    @classmethod
    def __get_output_name(cls):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"output-{str(timestamp)}.pdf"

    def convert_image_to_pdf(self, object_key, output_bucket_name=None):
        """Convert image to PDF

        :param object_key: key of object to convert
        :param output_bucket_name: bucket to upload combined pdf, default to origin bucket name
        :return: pre-signed url to access file on bucket
        """
        output_name = self.__get_output_name()

        if output_bucket_name is None:
            output_bucket_name = self.bucket_name

        try:
            object_res = self.s3_client.download_s3_object(object_key)
            Image.supported_file_type([object_res])

            # combine the files
            converted_pdf_bytes = Image.convert_image_to_pdf(object_res["ReadBodyStream"])

            # upload combined files to destination s3 bucket
            self.s3_client.put_object(output_bucket_name, converted_pdf_bytes, output_name)

            # return download url for combined files
            return self.s3_client.generate_download_url(output_bucket_name, output_name)
        except Exception:
            raise S3PDFException()

    def apply_watermark_object(self, object_key, watermark_key=None, text=None):
        """Apply watermark on object

        :param object_key: key of object to apply watermark on
        :param watermark_key: s3 object key to download watermark, if not text arg must be provided
        :param text: Text watermark to apply, if not watermark_key must be provided
        """

        try:
            watermark_data = None

            if watermark_key:
                watermark_res = self.s3_client.download_s3_object(watermark_key)
                PDF.supported_file_type([watermark_res])
                watermark_data = watermark_res["ReadBodyStream"]
            if text:
                watermark_data = Image.create_watermark(text)

            if not watermark_data:
                raise ValueError("watermark_key or text is required")

            # download file
            object_res = self.s3_client.download_s3_object(object_key)
            PDF.supported_file_type([object_res])

            # watermark file
            watermarked_file_pdf_bytes = PDF.apply_watermark(watermark_data, object_res["ReadBodyStream"])

            # upload watermarked file to s3
            self.s3_client.put_object(self.bucket_name, watermarked_file_pdf_bytes, object_key)
        except Exception:
            raise S3PDFException()

    def combine_objects(self, objects_to_combine, output_bucket_name=None):
        """ Merges the files into one pdf and upload to output s3_bucket

        :param objects_to_combine: object name or keys of file to combine within
        :param output_bucket_name: bucket to upload combined pdf, default to origin bucket name
        :return: pre-signed url to access file on bucket
        """
        output_name = self.__get_output_name()

        if output_bucket_name is None:
            output_bucket_name = self.bucket_name

        objects = []

        # get s3 objects using object keys
        for object_key in objects_to_combine:
            object_res = self.s3_client.download_s3_object(object_key)
            objects.append(object_res)

        try:
            # validate file type is supported
            PDF.supported_file_type(objects)

            # combine the files
            combined_pdf_bytes = PDF.combine_files([data["ReadBodyStream"] for data in objects])

            # upload combined files to destination s3 bucket
            self.s3_client.put_object(output_bucket_name, combined_pdf_bytes, output_name)

            # return download url for combined files
            return self.s3_client.generate_download_url(output_bucket_name, output_name)
        except Exception:
            raise S3PDFException()
