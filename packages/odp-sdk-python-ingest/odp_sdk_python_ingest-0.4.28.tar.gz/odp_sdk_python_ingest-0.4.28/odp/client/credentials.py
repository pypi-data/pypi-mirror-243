from abc import ABC, abstractmethod
from contextlib import contextmanager

import requests


class AzureClientCredentialsABC(ABC):
    """
    Abstract class for Azure credentials. Two methods must be implemented:
    - get_token to return a token
    - session: a context manager to use for sending requests.
    """

    @abstractmethod
    def get_token(self) -> str:
        pass

    @abstractmethod
    @contextmanager
    def session(self) -> requests.Session:
        pass


class ODCAzureClientCredentials(AzureClientCredentialsABC):
    """
    Credentials class for using the ODPClient within the ODC.
    """

    def get_token(self) -> str:
        res = requests.post("http://localhost:8000/access_token")
        res.raise_for_status()
        return res.json()["token"]

    def _auth_callback(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        request.headers.update({"Authorization": f"Bearer {self.get_token()}"})
        return request

    @contextmanager
    def session(self) -> requests.Session:
        session = requests.Session()
        session.auth = self._auth_callback

        yield session
        session.close()
