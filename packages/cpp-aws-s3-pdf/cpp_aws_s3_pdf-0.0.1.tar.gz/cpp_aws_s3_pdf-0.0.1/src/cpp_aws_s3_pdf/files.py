from datetime import datetime

from .utils.aws_s3 import S3
from .utils.pdf import PDF
from .exceptions import S3PDFCombineException


class S3ToPDFCombine:
    """
    S3ToPDFCombine Python utility for combining objects from Amazon S3 into a single PDF file.
    Ideal for users who need to aggregate content stored in S3 buckets and generate consolidated PDF documents
    for reports, archives, or data presentation.
    """

    def __init__(self, bucket_name, region=None):
        self.bucket_name = bucket_name
        self.s3_client = S3(bucket_name=bucket_name, region=region)

    def combine_objects(self, objects_to_combine, output_bucket_name=None):
        """ Merges the files into one pdf and upload to output s3_bucket

        :param objects_to_combine: object name or keys of file to combine within
        :param output_bucket_name: bucket to upload combined pdf, default to origin bucket name
        :return: pre-signed url to access file on bucket
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_name = f"output-{str(timestamp)}.pdf"

        if output_bucket_name is None:
            output_bucket_name = self.bucket_name

        objects = []

        # get s3 objects using object keys
        for object_key in objects_to_combine:
            object_res = self.s3_client.download_s3_object(object_key)
            objects.append(object_res)

        try:
            # combine the files
            combined_pdf_bytes = PDF.combine_files(objects)

            # upload combined files to destination s3 bucket
            self.s3_client.put_object(output_bucket_name, combined_pdf_bytes, output_name)

            # return download url for combined files
            return self.s3_client.generate_download_url(output_bucket_name, output_name)
        except Exception:
            raise S3PDFCombineException()
