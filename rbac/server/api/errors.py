# Copyright 2019 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
"""Define exceptions for HTTP error codes."""
from sanic.response import json
from sanic import Blueprint
from sanic.exceptions import SanicException
from sanic.exceptions import NotFound
from rethinkdb import ReqlDriverError

from rbac.common.logs import get_default_logger

ERRORS_BP = Blueprint("errors")
LOGGER = get_default_logger(__name__)
DEFAULT_MSGS = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    409: "Target Conflict",
    501: "Not Implemented",
    503: "Internal Error",
}


def add_status_code(code):
    """
    Decorator used for adding exceptions to _sanic_exceptions.
    """

    def class_decorator(cls):
        cls.status_code = code
        return cls

    return class_decorator


class ApiException(SanicException):
    """API exception with HTTP status code."""

    def __init__(self, message=None, status_code=None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code
        if message is None:
            self.message = DEFAULT_MSGS[self.status_code]
        else:
            self.message = message


@add_status_code(400)
class ApiBadRequest(ApiException):
    """Define ApiBadRequest exception."""

    pass


@add_status_code(401)
class ApiUnauthorized(ApiException):
    """Define ApiUnauthorized exception."""

    pass


@add_status_code(403)
class ApiForbidden(ApiException):
    """Define ApiForbidden exception."""

    pass


@add_status_code(404)
class ApiNotFound(ApiException):
    """Define ApiNotFound exception."""

    pass


@add_status_code(405)
class ApiDisabled(ApiException):
    """API is disabled due to incorrect mode."""

    pass


@add_status_code(409)
class ApiTargetConflict(ApiException):
    """ Define ApiTargetConflict exception."""

    pass


@add_status_code(501)
class ApiNotImplemented(ApiException):
    """Define ApiNotImplemented exception."""

    pass


@add_status_code(503)
class ApiInternalError(ApiException):
    """Define ApiInternalError exception."""

    pass


@ERRORS_BP.exception(NotFound)
async def handle_not_found(request, exception):
    """Return NotFound exception as json."""
    if not request:
        LOGGER.debug(request)
    return json(
        {"code": exception.status_code, "message": exception.message},
        status=exception.status_code,
    )


@ERRORS_BP.exception(ApiException)
def api_json_error(request, exception):
    """Return ApiException as json."""
    if not request:
        LOGGER.debug(request)
    return json(
        {"code": exception.status_code, "message": exception.message},
        status=exception.status_code,
    )


@ERRORS_BP.exception(SanicException)
async def handle_errors(request, exception):
    """Return SanicException as json."""
    if not request:
        LOGGER.debug(request)
    return json(
        {"code": exception.status_code, "message": exception.message},
        status=exception.status_code,
    )


@ERRORS_BP.exception(ReqlDriverError)
async def handle_reql_error(request, exception):
    """Re-establish connection on driver error """
    LOGGER.exception(exception)
    request.app.config.DB_CONN.reconnect(noreply_wait=False)


@ERRORS_BP.exception(Exception)
def json_error(request, exception):
    """Return request exception as json."""
    if not request:
        LOGGER.debug(request)
    try:
        code = exception.status_code
    except AttributeError:
        code = 503
    LOGGER.exception(exception)
    return json({"code": code, "message": exception.args[0]}, status=code)
