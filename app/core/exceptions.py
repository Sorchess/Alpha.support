from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args):
        super().__init__(self.detail, *args)


class NabronirovalHTTPException(HTTPException):
    detail = "Unexpected error"
    status_code = 500

    def __init__(self, *args):
        super().__init__(self.status_code, self.detail, *args)


class ObjectNotFoundException(NabronirovalException):
    detail = "Object not found"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Object alredy exists"


class UserAlreadyExistsException(NabronirovalException):
    detail = "User alredy exists"


class UserAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "User alredy exists"


class MessageAlreadyExistsException(NabronirovalException):
    detail = "Message alredy exists"


class MessageAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Message alredy exists"


class TopicAlreadyExistsException(NabronirovalException):
    detail = "Topic alredy exists"


class TopicAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Topic alredy exists"


class UserNotFoundException(NabronirovalException):
    detail = "User not found"


class UserNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "User not found"


class FileNotFoundException(NabronirovalException):
    detail = "File not found"


class FileNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "File not found"


class TopicNotFoundException(NabronirovalException):
    detail = "Topic not found"


class TopicNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Topic not found"


class UserWrongPasswordException(NabronirovalException):
    detail = "Wrong password"


class UserWrongPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Wrong password"


class UserEmailNotVerificatedException(NabronirovalException):
    detail = "Email address not verified"


class UserEmailNotVerificatedHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Email address not verified"


class UnsupportedMediaTypeException(NabronirovalException):
    detail = "Unsupported media file type"


class UnsupportedMediaTypeHTTPException(NabronirovalHTTPException):
    status_code = 415
    detail = "Unsupported media file type"


class MissingSessionCookieException(NabronirovalException):
    detail = "Missing cookie"


class MissingSessionCookieHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Missing cookie"


class InvalidSessionCookieException(NabronirovalException):
    detail = "Invalid cookie"


class InvalidSessionCookieHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Invalid cookie"


class InvalidTokenException(NabronirovalException):
    detail = "Invalid token"


class InvalidTokenHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Invalid token"


class DeprecatedTokenException(NabronirovalException):
    detail = "Token is deprecated"


class DeprecatedTokenHTTPException(NabronirovalHTTPException):
    status_code = 400
    detail = "Token is deprecated"


class NotAuthorizedException(NabronirovalException):
    detail = "Not authorized"


class NotAuthorizedHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Not authorized"


class TooManyAttemptsException(NabronirovalException):
    detail = "Too many attempts"


class TooManyAttemptsHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Too many attempts"


class StreamingFileFailedException(NabronirovalException):
    detail = "Streaming file failed"


class StreamingFileFailedHTTPException(NabronirovalHTTPException):
    status_code = 502
    detail = "Streaming file failed"


class FileDeleteFailedException(NabronirovalException):
    detail = "File delete failed"


class FileDeleteFailedHTTPException(NabronirovalHTTPException):
    status_code = 502
    detail = "File delete failed"


class InvalidMetadataException(NabronirovalException):
    detail = "Invalid metadata"


class InvalidMetadataHTTPException(NabronirovalHTTPException):
    status_code = 400
    detail = "Invalid metadata"


class FileTooLargeException(NabronirovalException):
    detail = "File too large"


class FileTooLargeHTTPException(NabronirovalHTTPException):
    status_code = 413
    detail = "File too large"


class FileUploadFailedException(NabronirovalException):
    detail = "File upload failed"


class FileUploadFailedHTTPException(NabronirovalHTTPException):
    status_code = 502
    detail = "File upload failed"


class EmptyFileException(NabronirovalException):
    detail = "Empty file"


class EmptyFileExceptionHTTPException(NabronirovalHTTPException):
    status_code = 400
    detail = "Empty file"
