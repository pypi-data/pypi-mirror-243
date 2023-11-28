import logging
from getpass import getpass
from os import environ
from time import time
from typing import Union
from urllib.parse import quote_plus

import requests

logger = logging.getLogger(__name__)
_token_cache = {}


def ensure_list(value: Union[list[str], str]) -> list[str]:
    """
    Helper function that always returns a string as a list[str].

    """

    return [value] if isinstance(value, str) else value


def get_token() -> str:
    """
    Returns an access token for the client in Azure AD.
    Uses the same token from _token_cache in repeated API-calls.

    Documentation:
    https://learn.microsoft.com/en-us/graph/auth/auth-concepts

    """

    BASE_URL = "https://login.microsoftonline.com/{}/oauth2/v2.0/token"
    CLOCK_SKEW_SECONDS = 5 * 60

    global _token_cache
    if _token_cache:
        if _token_cache["exp"] >= time() + CLOCK_SKEW_SECONDS:
            logger.info("Using cached access token")
            return _token_cache["jwt"]
        else:
            logger.info("Cached access token has expired")

    (tenant_id, client_id, client_secret) = _get_config()

    url = BASE_URL.format(quote_plus(tenant_id))
    payload = {
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    logger.info("Getting access token ..")

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        error_message = "Request failed ({} {}) - {}".format(
            response.status_code,
            response.reason,
            response.json().get("error_description"),
        )
        logger.error(error_message)
        raise ConnectionError(error_message)

    data = response.json()
    _token_cache["jwt"] = data["access_token"]
    _token_cache["exp"] = time() + data["expires_in"]

    seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
    logger.info(f"Access token retrieved and saved to cache ({seconds_str})")

    return data["access_token"]


def _get_config() -> tuple[str]:
    """
    Returns a tuple with variables for connecting to the Azure AD client.

    Attempts to read AAD_TENANT_ID, AAD_CLIENT_ID and AAD_CLIENT_SECRET
    from settings.py when running from Django, or alternatively from os.environ
    if Django is not installed or settings are not initialized.

    Prompts the user for input if any of the required variables are empty.

    """

    try:
        from django.conf import settings

        # If settings.py is initialized
        if settings.configured:
            logger.info("Importing client credentials from django.conf.settings")
            tenant_id = settings.AAD_TENANT_ID
            client_id = settings.AAD_CLIENT_ID
            client_secret = settings.AAD_CLIENT_SECRET
        else:
            raise ImportError("Django not running")

    # Django is not installed or not running
    except ImportError:
        logger.info("Importing client credentials from os.environ")
        tenant_id = environ.get("AAD_TENANT_ID")
        client_id = environ.get("AAD_CLIENT_ID")
        client_secret = environ.get("AAD_CLIENT_SECRET")

    if not tenant_id:
        logger.info("AAD_TENANT_ID missing or empty")
        tenant_id = input("AAD_TENANT_ID: ")
    if not client_id:
        logger.info("AAD_CLIENT_ID missing or empty")
        client_id = input("AAD_CLIENT_ID: ")
    if not client_secret:
        logger.info("AAD_CLIENT_SECRET missing or empty")
        client_secret = getpass("AAD_CLIENT_SECRET: ")

    return (tenant_id, client_id, client_secret)
