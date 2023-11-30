import requests

from typing import Optional, Callable


class BytebinException(BaseException):
    ...


class ByteResponse:
    """
    ByteResponse Class

    Attributes
    ----------
    url: str
        The URL of the paste
    key: str
        The key of the paste
    content: str
        The content of the paste
    """

    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        content: Optional[str] = None,
    ) -> None:
        """
        Parameters
        ----------
        url: str
            The URL of the paste
        key: str
            The key of the paste
        content: str
            The content of the paste

        Returns
        -------
        None
        """
        self._url: str = url
        self._key: str = key
        self._content: str = content

    @property
    def url(self) -> str:
        """The URL of the paste"""
        return self._url

    @property
    def key(self) -> str:
        """The key of the paste"""
        return self._key

    @property
    def content(self) -> str:
        """The content of the paste"""
        return self._content

    @classmethod
    def build(
        cls, url: str = None, key: str = None, content: str = None
    ) -> "ByteResponse":
        """
        Builds a ByteResponse object

        Parameters
        ----------
        url: str
            The URL of the paste
        key: str
            The key of the paste
        content: str
            The content of the paste

        Returns
        -------
        ByteResponse
            The ByteResponse object
        """
        return cls(url=url, key=key, content=content if content else None)


class Bytebin:
    """
    Bytebin Class

    Attributes
    ----------
    session: requests.Session
        The session used for the requests
    base_url: str
        The base URL of the API
    raw_base_url: str
        The base URL of the raw API

    Methods
    -------
    create(text: str) -> Callable[[ByteResponse], BytebinException]
        Creates a paste

    lookup(key: str) -> Callable[[ByteResponse], BytebinException]
        Looks up a paste

    """

    def __init__(
        self,
        proxy: Optional[str] = None,
        timeout: Optional[int] = 30,
        use_retry: Optional[bool] = True,
    ) -> None:
        self.session: requests.Session = requests.Session()
        self.session.headers.update({"User-Agent": "Bytebin.py"})
        self.session.proxies: dict = {"http": proxy, "https": proxy} if proxy else None
        self.base_url: str = "https://bytebin.dev/"
        self.raw_base_url: str = "https://bytebin.dev/raw/"
        self.timeout: int = timeout

    def create(self, text: str) -> Callable[[ByteResponse], BytebinException]:
        """
        Creates a paste

        Parameters
        ----------
        text: str
            The text to create the paste with

        Returns
        -------
        Callable[[ByteResponse], BytebinException]
            The ByteResponse object

        Raises
        ------
        BytebinException
            If the status code is not 200
        """
        if text == "":
            return "Enter Content Please"

        self.session.headers.update({"Content-Type": "text/plain"})
        self.session.headers.update({"Content-Length": f"{len(text)}"})
        response = self.session.post(f"{self.base_url}documents", data=text)

        if response.status_code != 200:
            raise BytebinException(f"Status code: {response.status_code}")

        url = response.json()["url"]

        return ByteResponse.build(url=url, key=url.split("/")[-1])

    def lookup(self, key: str) -> Callable[[ByteResponse], BytebinException]:
        """
        Looks up a paste

        Parameters
        ----------
        key: str
            The key of the paste

        Returns
        -------
        Callable[[ByteResponse], BytebinException]
            The ByteResponse object

        Raises
        ------
        BytebinException
            If the status code is not 200
        """
        if key == "":
            return "Enter Content Please"

        self.session.headers.update({"Content-Type": "text/plain; charset=UTF-8"})
        response = self.session.get(self.raw_base_url + key).text

        if response == 404:
            raise BytebinException(f"Status code: {response.status_code}")

        return ByteResponse.build(
            url=self.raw_base_url + key, key=key, content=response
        )
