from functools import wraps

from botocore.exceptions import ClientError


class Error(Exception):
    @classmethod
    def from_client_error(cls, e):
        error = e.response["Error"]

        return cls(
            f"Error ({error['Code']}): {error['Message']}"
        )


def is_resource_not_found(e):
    return e.response["Error"]["Code"] == "ResourceNotFoundException"


def wrap_client_error(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ClientError as e:
            raise Error.from_client_error(e)

    return wrapper
