from abc import ABC
from pprint import pprint
from urllib.parse import urljoin

import pandas as pd
import requests

from .utils import uuid_regex

DEFAULT_HEADERS = {"Accept": "Application/ld+json"}


class Unsuccessful(Exception):
    """HTTP requests did not return status code 200"""

    pass


class Base(ABC):
    def __init__(
        self,
        base_url: str = "https://glossary.ecoinvent.org/",
        headers: dict = DEFAULT_HEADERS,
    ):
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.headers = headers

    def _make_request(
        self, endpoint: str | None = None, params: dict | None = None, json: bool = True
    ) -> requests.Response | dict:
        """Internal function to make a request and handle errors.

        Parameters
        ----------

        endpoint : str, optional
            URL path as str to concatenate with `self.base_url`.
            Uses `self.endpoint` as default
        params : dict, optional
            Additional parameters to pass to request constructor
        json : bool, optional
            Convert response from JSON-LD

        Returns
        -------

        `requests.Response` | dict
            See https://requests.readthedocs.io/en/latest/api/#requests.Response
            Return `dict` if `json` is truthy.

        Raises
        ------

        `Unsuccessful`
            Reponse status code was not 200

        """  # noqa: E501
        if endpoint is None and not hasattr(self, "endpoint"):
            raise NotImplementedError("Subclass is missing `endpoint` attribute")

        url = urljoin(self.base_url, endpoint or self.endpoint)
        response = requests.get(url, headers=self.headers, params=params or {})
        if response.status_code != 200:
            error = f"""HTTP request unsuccessful.
    URL: {url}
    Status code: {response.status_code}
    Time elapsed: {response.elapsed}
    Headers: {pprint(response.headers)}
    """
            raise Unsuccessful(error)
        if json:
            return response.json()
        else:
            return response

    def all(self, as_dataframe: bool = True) -> list[dict] | pd.DataFrame:
        """Get pandas DataFrame of all objects.

        Parameters
        ----------

        as_dataframe : bool
            Convert list of item elements to pandas DataFrame

        Returns
        -------

        list of item element dicts or pandas DataFrame

        Examples
        --------

        These examples assume the `units/` endpoint

        TBD; DataFrame formatting?

        """
        response_data = [item["item"] for item in self._make_request(json=True)["itemListElement"]]
        self._add_uuid(response_data)
        if as_dataframe:
            return pd.DataFrame(response_data)
        else:
            return response_data

    def _add_uuid(self, data: list[dict]) -> None:
        """Our data has `@id` elements with UUIDs. Break these out if possible.

        Modifies data in place.

        Only changes elements in `data` if `@id` is present, the UUID regex
        matches, and `uuid` is missing.

        Parameters
        ----------

        data : list[dict]
            List of data dictionaries to supplement

        """
        regex = uuid_regex(self.base_url)

        for obj in data:
            if "uuid" in obj or "@id" not in obj:
                continue
            match = regex.search(obj["@id"])
            if match is None or not match.group("uuid"):
                continue
            obj["uuid"] = match.group("uuid")

    def metadata(self) -> dict:
        response_data = self._make_request(json=True)
        return {key: value for key, value in response_data.items() if key != "itemListElement"}


class Units(Base):
    endpoint = "units/"
