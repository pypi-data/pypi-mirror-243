class S3PDFException(Exception):
    """Base class for exceptions"""

    def __init__(self, message="Something went wrong, please try again", *args):
        self.message = message
        super().__init__(message, *args)


class UnsupportedFileTypeException(S3PDFException):
    def __init__(self, message="File type not supported", *args):
        self.message = message
        super().__init__(message, *args)


class ConvertImageToPDFException(S3PDFException):
    def __init__(self, message="Error converting image to PDF", *args):
        self.message = message
        super().__init__(message, *args)


class CombinePDFException(S3PDFException):
    def __init__(self, message="Error Combining PDF", *args):
        self.message = message
        super().__init__(message, *args)


class FetchFileException(S3PDFException):
    def __init__(self, message="Unable to fetch requested file", *args):
        self.message = message
        super().__init__(message, *args)
