import requests
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TGSession:
    """
    A class to manage a Telegram session using the requests library.

    Attributes:
        session (requests.Session): The HTTP session object.
    """

    def __init__(self):
        self.session = requests.Session()

    def get(self, url: str, params: Optional[dict] = None) -> requests.Response:
        """
        Send an HTTP GET request.

        Args:
            url (str): The URL to send the request to.
            params (dict, optional): Parameters to send with the request. Defaults to None.

        Returns:
            requests.Response: The response from the server.
        """
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending GET request: {e}")
            return None

    def post(self, url: str, data: Optional[dict] = None) -> requests.Response:
        """
        Send an HTTP POST request.

        Args:
            url (str): The URL to send the request to.
            data (dict, optional): Data to send in the request body. Defaults to None.

        Returns:
            requests.Response: The response from the server.
        """
        try:
            response = self.session.post(url, data=data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending POST request: {e}")
            return None

# Create a TGSession object
tg_session = TGSession()

# Example usage:
# response = tg_session.get('https://api.example.com/data', params={'key': 'value'})
# print(response.json())
