import logging
import requests
import sys
from flask import Request
from typing import Any, Final
from werkzeug.exceptions import BadRequest

from .env_pomes import APP_PREFIX, env_get_int
from .exception_pomes import exc_format
from .http_statuses import _HTTP_STATUSES

HTTP_DELETE_TIMEOUT: Final[int] = env_get_int(f"{APP_PREFIX}_HTTP_DELETE_TIMEOUT", 300)
HTTP_GET_TIMEOUT: Final[int] = env_get_int(f"{APP_PREFIX}_HTTP_GET_TIMEOUT", 300)
HTTP_POST_TIMEOUT: Final[int] = env_get_int(f"{APP_PREFIX}_HTTP_POST_TIMEOUT", 300)
HTTP_PUT_TIMEOUT: Final[int] = env_get_int(f"{APP_PREFIX}_HTTP_PUT_TIMEOUT", 300)

MIMETYPE_BINARY: Final[str] = "application/octet-stream"
MIMETYPE_CSS: Final[str] = "text/css"
MIMETYPE_CSV: Final[str] = "text/csv"
MIMETYPE_HTML: Final[str] = "text/html"
MIMETYPE_JAVASCRIPT: Final[str] = "text/javascript"
MIMETYPE_JSON: Final[str] = "application/json"
MIMETYPE_MULTIPART: Final[str] = "multipart/form-data"
MIMETYPE_PDF: Final[str] = "application/pdf"
MIMETYPE_PKCS7: Final[str] = "application/pkcs7-signature"
MIMETYPE_SOAP: Final[str] = "application/soap+xml"
MIMETYPE_TEXT: Final[str] = "text/plain"
MIMETYPE_URLENCODED: Final[str] = "application/x-www-form-urlencoded"
MIMETYPE_XML: Final[str] = "application/xml"
MIMETYPE_ZIP: Final[str] = "application/zip"


def http_status_code(status_name: str) -> int:
    """
    Return the corresponding code of the HTTP status *status_name*.

    :param status_name: the name of HTTP the status
    :return: the corresponding HTTP status code
    """
    # initialize the return variable
    result: int | None = None

    for key, value in _HTTP_STATUSES:
        if status_name == value["name"]:
            result = key

    return result


def http_status_name(status_code: int) -> str:
    """
    Return the corresponding name of the HTTP status *status_code*.

    :param status_code: the code of the HTTP status
    :return: the corresponding HTTP status name
    """
    item: dict = _HTTP_STATUSES.get(status_code)
    return (item or {"name": "Unknown status code"}).get("name")


def http_status_description(status_code: int, lang: str = "en") -> str:
    """
    Return the description of the HTTP status *status_code*.

    :param status_code: the code of the HTTP status
    :param lang: optional language ('en' or 'pt' - defaults to 'en')
    :return: the corresponding HTTP status description, in the given language
    """
    item: dict = _HTTP_STATUSES.get(status_code)
    return (item or {"en": "Unknown status code", "pt": "Status desconhecido"}).get(lang)


def http_json_from_form(request: Request) -> dict:
    """
    Build and return a *dict* containing the *key-value* pairs of the form parameters found in *request*.

    :param request: the HTTP request
    :return: dict containing the form parameters found
    """
    # initialize the return variable
    result: dict = {}

    # traverse the form parameters
    for key, value in request.form.items():
        result[key] = value

    return result


def http_json_from_request(request: Request) -> dict:
    """
    Obtain the *JSON* holding the *request*'s input parameters.

    :param request: the Request object
    :return: dict containing the input parameters (empty, if no input data exist)
    """
    # initialize the return variable
    result: dict = {}

    # retrieve the input JSON
    try:
        result: dict = request.get_json()
    except BadRequest:
        resp: str = request.get_data(as_text=True)
        # does the request contain input data ?
        if len(resp) > 0:
            # yes, possibly mal-formed JSON
            raise

    return result


def http_json_from_get(errors: list[str] | None, url: str, headers: dict = None,
                       params: dict = None, timeout: int | None = HTTP_GET_TIMEOUT,
                       logger: logging.Logger = None) -> Any:
    """
    Retrieve the *JSON* content of a *GET* request to the given *url*.

    The *JSON* content is typically returned as a *dict*, or as a *list[dict]* .
    The request might contain *headers* and *parameters*.

    :param errors: incidental error messages
    :param url: the destination URL
    :param headers: optional headers
    :param params: optional parameters
    :param timeout: timeout, in seconds (defaults to HTTP_GET_TIMEOUT - use None to omit)
    :param logger: optional logger
    :return: the contents of the JSON string
    """
    # initialize the return variable
    result: Any = None

    if logger:
        logger.debug(f"GETing '{url}'")

    try:
        response: requests.Response = requests.get(url=url,
                                                   headers=headers,
                                                   params=params,
                                                   timeout=timeout)
        result = response.json()
        if logger:
            logger.debug(f"GETed '{url}', "
                         f"status {response.status_code} ({http_status_name(response.status_code)})")
    except Exception as e:
        err_msg: str = f"Error GETing '{url}': '{exc_format(e, sys.exc_info())}'"
        if logger:
            logger.error(err_msg)
        if errors is not None:
            errors.append(err_msg)

    return result


def http_json_from_post(errors: list[str] | None, url: str, headers: dict = None,
                        params: dict = None, data: dict = None, json: dict = None,
                        timeout: int | None = HTTP_POST_TIMEOUT, logger: logging.Logger = None) -> Any:
    """
    Retrieve the *JSON* content of a *POST* request to the given *url*.

    The *JSON* content is typically returned as a *dict*, or as a *list[dict]* .
    The request might contain *headers* and *parameters*.

    :param errors: incidental error messages
    :param url: the destination URL
    :param headers: optional headers
    :param params: optional parameters
    :param data: optionaL data to send in the body of the request
    :param json: optional JSON to send in the body of the request
    :param timeout: timeout, in seconds (defaults to HTTP_POST_TIMEOUT - use None to omit)
    :param logger: optional logger to log the operation with
    :return: the contents of the JSON string
    """
    # initialize the return variable
    result: Any = None

    if logger:
        logger.debug(f"POSTing '{url}'")

    try:
        response: requests.Response = requests.post(url=url,
                                                    headers=headers,
                                                    data=data,
                                                    json=json,
                                                    params=params,
                                                    timeout=timeout)
        result = response.json()
        if logger:
            logger.debug(f"POSTed '{url}', "
                         f"status {response.status_code} ({http_status_name(response.status_code)})")
    except Exception as e:
        err_msg: str = f"Error POSTing '{url}': '{exc_format(e, sys.exc_info())}'"
        if logger:
            logger.error(err_msg)
        if errors is not None:
            errors.append(err_msg)

    return result


def http_json_from_put(errors: list[str] | None, url: str, headers: dict = None,
                       params: dict = None, data: dict = None, json: dict = None,
                       timeout: int | None = HTTP_POST_TIMEOUT, logger: logging.Logger = None) -> Any:
    """
    Retrieve the *JSON* content of a *PUT* request to the given *url*.

    The *JSON* content is typically returned as a *dict*, or as a *list[dict]* .
    The request might contain *headers* and *parameters*.

    :param errors: incidental error messages
    :param url: the destination URL
    :param headers: optional headers
    :param params: optional parameters
    :param data: optionaL data to send in the body of the request
    :param json: optional JSON to send in the body of the request
    :param timeout: timeout, in seconds (defaults to HTTP_POST_TIMEOUT - use None to omit)
    :param logger: optional logger to log the operation with
    :return: the contents of the JSON string
    """
    # initialize the return variable
    result: Any = None

    if logger:
        logger.debug(f"PUTing '{url}'")

    try:
        response: requests.Response = requests.put(url=url,
                                                   headers=headers,
                                                   data=data,
                                                   json=json,
                                                   params=params,
                                                   timeout=timeout)
        result = response.json()
        if logger:
            logger.debug(f"PUTed '{url}', "
                         f"status {response.status_code} ({http_status_name(response.status_code)})")
    except Exception as e:
        err_msg: str = f"Error PUTing '{url}': '{exc_format(e, sys.exc_info())}'"
        if logger:
            logger.error(err_msg)
        if errors is not None:
            errors.append(err_msg)

    return result
