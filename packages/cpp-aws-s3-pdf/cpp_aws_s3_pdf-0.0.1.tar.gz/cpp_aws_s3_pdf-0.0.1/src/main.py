from cpp_aws_s3_pdf.files import S3ToPDFCombine

if __name__ == "__main__":
    bucket_name = "cpp-aws-s3-pdf"

    objects_to_combine = ["object_1.pdf", "object_2.pdf", "object_3.pdf"]

    objects_combiner = S3ToPDFCombine(bucket_name)
    download_url = objects_combiner.combine_objects(objects_to_combine)

    print(download_url)
