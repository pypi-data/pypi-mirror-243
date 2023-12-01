import boto3
from botocore.exceptions import ClientError

from ..exceptions import FetchFileException


class S3:

    def __init__(self, bucket_name, region=None):
        self.bucket_name = bucket_name
        self.bucket_region = region

    def get_s3_client(self):
        """Initializes client for s3

        :return: s3_client
        """
        service_name = 's3'
        region = self.bucket_region

        if not region:
            client = boto3.client(service_name)
        else:
            client = boto3.client(service_name, region_name=region)

        return client

    def download_s3_object(self, object_key):
        """
        Downloads s3 object from defined bucket
        :param object_key:
        :return:
        """

        try:
            s3_client = self.get_s3_client()
            response = s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
            read_body_stream = response["Body"].read()

            return {
                "ObjectKey": object_key,
                "ContentType": response["ContentType"],
                "ReadBodyStream": read_body_stream
            }
        except ClientError:
            raise FetchFileException()

    def put_object(self, bucket_name, data, object_key):
        """Adds an object to an S3 bucket.

            :param bucket_name:
            :param data: bytes or seekable file-like object
            :param object_key: S3 object key. If not specified then file_name is used
            :return: put response
        """

        s3_client = self.get_s3_client()
        response = s3_client.put_object(Body=data, Bucket=bucket_name, Key=object_key)
        return response

    def generate_download_url(self, bucket_name, object_key, expiration=3600):
        """
        Generate a pre-signed url for an S3 object with a specific version.

        :param bucket_name: Name of the S3 bucket.
        :param object_key: Key of the S3 object.
        :param expiration: Time in seconds for the pre-signed url to remain valid, defaults to 1hr.
        :return: pre-signed url as a string.
        """
        s3_client = self.get_s3_client()
        params = {'Bucket': bucket_name,
                  'Key': object_key}

        pre_signed_url = s3_client.generate_presigned_url('get_object',
                                                          Params=params,
                                                          ExpiresIn=expiration)
        return pre_signed_url
