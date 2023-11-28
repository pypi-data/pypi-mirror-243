import logging
from typing import Union
from urllib.parse import quote_plus, urljoin

import requests

from .core import ensure_list, get_token

logger = logging.getLogger(__name__)


def get_device(
    device_id: str = None,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
) -> Union[list[dict], dict]:
    """
    Returns one or more devices from the Microsoft Graph API.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 100 objects by default.
    This can be specified by setting top=[1..999], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "Device.Read.All" app permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/device
    https://learn.microsoft.com/en-us/graph/api/device-list

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/devices"
    MAX_PAGE_SIZE = 999

    if device_id and (filter or search):
        raise ValueError(
            "Parameters device_id and filter|search are mutually exclusive."
        )

    url = urljoin(f"{BASE_URL}/", quote_plus(device_id)) if device_id else BASE_URL
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "ConsistencyLevel": "eventual" if filter or search or orderby else None,
    }
    params = {
        "$select": ",".join(ensure_list(select)) if select else None,
        "$filter": filter,
        "$search": f'"{search}"' if search else None,
        "$orderby": ",".join(ensure_list(orderby)) if orderby else None,
        "$top": top if top is not None else (MAX_PAGE_SIZE if all else None),
        "$count": "true" if filter or search or orderby else None,
    }

    data = []
    total_seconds = 0.0
    logger.info("Getting devices ..")

    while True:
        response = requests.get(url, headers=headers, params=params)
        total_seconds += response.elapsed.total_seconds()

        if response.status_code != 200:
            error_message = "Request failed ({} {}) - {}".format(
                response.status_code,
                response.reason,
                response.json().get("error", {}).get("message"),
            )
            logger.error(error_message)
            raise ConnectionError(error_message)

        data.extend(response.json().get("value", [response.json()]))
        next_link = response.json().get("@odata.nextLink")

        if next_link and (all and top is None):
            if response.json().get("@odata.count"):
                count = response.json().get("@odata.count")

            seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
            logger.debug(
                f"Received {len(data)}/{count} objects in response ({seconds_str})"
            )

            params["$skiptoken"] = next_link.split("$skiptoken=")[1]
        else:
            break

    total_seconds_str = "{:.1f} s".format(total_seconds)
    logger.info(f"Received {len(data)} objects ({total_seconds_str})")

    return data[0] if device_id else data


def delete_device(device_id: str) -> bool:
    """
    Deletes a device based on its id property.

    Requires admin consent for "Device.ReadWrite.All" app permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/device-delete

    """

    BASE_URL = "https://graph.microsoft.com/v1.0/devices/{}"

    url = BASE_URL.format(quote_plus(device_id))
    headers = {"Authorization": f"Bearer {get_token()}"}

    logger.info(f"Deleting device {device_id} ..")

    response = requests.delete(url, headers=headers)

    if response.status_code != 204:
        error_message = "Request failed ({} {}) - {}".format(
            response.status_code,
            response.reason,
            response.json().get("error", {}).get("message"),
        )
        logger.error(error_message)
        raise ConnectionError(error_message)

    seconds_str = "{:.1f} s".format(response.elapsed.total_seconds())
    logger.info(f"Request completed successfully {seconds_str}")

    return True
