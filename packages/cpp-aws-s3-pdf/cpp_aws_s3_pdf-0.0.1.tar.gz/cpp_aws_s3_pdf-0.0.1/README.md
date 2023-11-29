# CPP_AWS_S3_PDF

## Overview

Cpp_aws_s3_pdf is a Python utility library designed to streamline the process of combining objects from Amazon S3 into a
single
PDF file.
This tool is ideal for users who need to aggregate content stored in S3 buckets and generate consolidated PDF documents
for reports, archives, or data presentation.

## Features

- S3 Integration: Seamlessly connect to Amazon S3 buckets and access objects.
- PDF Generation: Efficiently combine multiple objects into a single PDF file.
- Security: Ensures secure access to S3 resources with AWS credentials, with expiration on combined files.

## Installation

To install Your-Library-Name, simply use pip:

```bash
pip install cpp_aws_s3_pdf
```

## Usage

Here's a quick start on how to use `cpp_aws_s3_pdf`:

- Set up AWS Credentials: Ensure your AWS credentials are configured properly.
  This can be done by following the guidelines outline on
  the [Boto3 Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration)
  Page.

- Import and Initialize:

```python
from cpp_aws_s3_pdf.files import S3ToPDFCombine

objects_combiner = S3ToPDFCombine(bucket_name='your-bucket-name')
```

- Combine S3 Objects into PDF:

```python
objects_to_combine = ['object_key1', 'object_key2', ...]
download_url = objects_combiner.combine_objects(objects_to_combine, output_bucket_name='my_combine_bucket')
```

## Configuration

- AWS Region: Set the AWS region where your S3 bucket is located.

## Dependencies

- AWS
- boto3
- PyPDF

## For local development

- Clone repository

```bash
https://github.com/noble-cc/cpp_aws_s3_pdf.git
```

- Create `venv` environment and activate environment

- Build project

```bash
python -m build
```

### To install project locally:
```bash
pip install <file_path>*-any.whl
```

## License

This project is licensed under the MIT License.

