from cpp_aws_s3_pdf.s3_pdf import S3Pdf

bucket_name = "cpp-aws-s3-pdf"

s3_pdf = S3Pdf(bucket_name)


def combine_file(object_keys):
    download_url = s3_pdf.combine_objects(object_keys)
    print(download_url)


def watermark_file(object_key, text):
    s3_pdf.apply_watermark_object(object_key, text=text)


def convert_image_to_pdf(object_key):
    s3_pdf.convert_image_to_pdf(object_key)


if __name__ == "__main__":
    objects_to_combine = ["object_1.pdf", "object_2.pdf", "object_3.pdf"]

    combine_file(objects_to_combine)
    watermark_file(objects_to_combine[2], "This is a sample watermark.")
    convert_image_to_pdf("object_image.jpg")
