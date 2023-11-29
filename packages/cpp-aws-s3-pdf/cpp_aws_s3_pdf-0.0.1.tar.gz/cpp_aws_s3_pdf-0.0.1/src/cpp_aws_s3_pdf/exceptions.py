class S3PDFCombineException(Exception):
    """Base class for exceptions"""

    def __init__(self, message="Something went wrong, please try again", *args):
        self.message = message
        super().__init__(message, *args)


class UnsupportedFileTypeException(S3PDFCombineException):
    def __init__(self, message="File type not supported", *args):
        self.message = message
        super().__init__(message, *args)


class FetchFileException(S3PDFCombineException):
    def __init__(self, message="Unable to fetch requested file", *args):
        self.message = message
        super().__init__(message, *args)
