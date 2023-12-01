from http import HTTPStatus

from fiddler3.exceptions import NotFound
from fiddler3.schemas.response import ErrorData


def raise_not_found(message: str) -> None:
    """Raise NotFound if the resource is not found while fetching with names"""
    raise NotFound(
        error=ErrorData(
            code=HTTPStatus.NOT_FOUND,
            message=message,
            errors=[
                {
                    'reason': 'ObjectNotFound',
                    'message': message,
                    'help': '',
                }
            ],
        ),
    )
