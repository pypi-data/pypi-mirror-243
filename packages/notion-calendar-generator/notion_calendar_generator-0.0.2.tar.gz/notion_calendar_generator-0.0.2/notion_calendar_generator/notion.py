from typing import Union

import requests
import json
from urllib.error import HTTPError
import logging


# The API class is used to interact with the Notion API.
class API:
    def __init__(self, url: str, headers: dict, logger: logging.Logger) -> None:
        """
        Initialize the API class.

        Args:
            url (str): The URL for the Notion API.
            headers (dict): The headers to use when making requests to the Notion API.
            logger (logging.Logger): A logger instance.
        """
        self.year_id = None
        self.quarter_id = None
        self.month_id = None
        self.week_id = None
        self.day_id = None
        self.headers = headers
        self.url = url
        self.logger = logger

    # Private method to call the Notion API.
    @staticmethod
    def __call_api(url: str, headers: dict = None, data: dict = None, method: str = 'post') -> requests.Response:
        """
        Call the Notion API.

        Args:
            url (str): The URL for the Notion API.
            headers (dict): The headers to use when making requests to the Notion API.
            data (dict): The data to send with the request.
            method (str): The HTTP method to use for the request. Defaults to 'post'.

        Returns:
            requests.Response: The response from the Notion API.
        """
        method_map = {
            'get': requests.get,
            'post': requests.post
        }
        http = method_map[method]
        # data = json.dumps(data).encode('utf-8')
        if method == "get":
            response = http(url, headers=headers, params=data)
            return response
        response = http(url, headers=headers, json=data)
        response.raise_for_status()
        return response

    # Private method to create the payload for a POST request.
    @staticmethod
    def __post_payload(destination: str, **data) -> dict:
        """
        Create the payload for a POST request.

        Args:
            destination (str): The destination for the request.
            **data: Additional data to include in the payload.

        Returns:
            dict: The payload for the request.
        """
        data_dict = dict(
            {
                "parent": {"database_id": destination},
                "properties": {
                    "title": {
                        "title": [
                            {
                                "text": {
                                    "content": data['title']
                                }
                            }]
                    },
                    "Date": {
                        "date": {
                            "start": data['start']
                        }}}})
        if 'relations' in data.keys():
            for relation_name, relation_ids in data['relations'].items():
                relation = {relation_name: {
                    "relation": [{"id": id} for id in relation_ids]
                }}
                data_dict['properties'].update(relation)
        if 'end' in data.keys():
            end_date = {"end": data['end']}
            data_dict['properties']['Date']['date'].update(end_date)
        return data_dict

    # Private method to post a single page to the Notion API.
    def __post_single_page(self, destination: str, data: dict) -> str:
        """
        Post a single page to the Notion API.

        Args:
            destination (str): The destination for the request.
            data (dict): The data to send with the request.

        Returns:
            str: The ID of the created page.
        """
        self.logger.info(f'posting data: {data["title"]}')
        data = self.__post_payload(destination, **data)
        response = self.__call_api(self.url, self.headers, data, 'post')
        return response.json()['id']

    # Private method to post multiple pages to the Notion API.
    def __post_multiple_pages(self, destination: str, data: Union[list, set]) -> list:
        """
        Post multiple pages to the Notion API.

        Args:
            destination (str): The destination for the request.
            data (Union[list, set]): The data to send with the request.

        Returns:
            list: The IDs of the created pages.
        """
        request_responses = []
        for d in data:
            request_responses.append(self.__post_single_page(destination, d))
        return request_responses

    # Method to post a page to the Notion API.
    def post_page(self, destination: str, data: Union[dict, list, set]) -> Union[list, str]:
        """
        Post a page to the Notion API.

        Args:
            destination (str): The destination for the request.
            data (Union[dict, list, set]): The data to send with the request.

        Returns:
            Union[str, list]: The ID(s) of the created page(s).
        """
        if isinstance(data, (list, tuple)):
            return self.__post_multiple_pages(destination, data)
        return self.__post_single_page(destination, data)

    # Method to add connection strings to the API instance.
    def add_connection_strs(self, day: str, week: str, month: str, quarter: str, year: str) -> None:
        """
        Add connection strings to the API instance.

        Args:
            day (str): The ID for the day.
            week (str): The ID for the week.
            month (str): The ID for the month.
            quarter (str): The ID for the quarter.
            year (str): The ID for the year.
        """
        self.day_id = day
        self.week_id = week
        self.month_id = month
        self.quarter_id = quarter
        self.year_id = year
