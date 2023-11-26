import logging
from typing import List

import requests

from bs4 import BeautifulSoup

from .models import URLConfig


class URLCollector:
    """
    This class is used to collect all the URLs from a given website.
    - url_info: The URL to collect the extension-specific URLs from.
    """

    def __init__(self, url_info: URLConfig):
        self.url = url_info.url
        self.max_depth = url_info.max_depth
        self.file_extensions = url_info.file_extensions
        self.process_static_pages = url_info.process_static_pages

    def _collect_urls_from_static_pages(self) -> List[str]:
        """
        Collect all the URLs for provided file extensions from a given URL.
        This method will only collect URLs from the static pages of the website.
        """
        try:
            response = requests.get(self.url, timeout=5)
            soup = BeautifulSoup(response.content, "html.parser")

            links = soup.find_all("a", href=True)

            file_extension_links = []

            for link in links:
                for file_extension in self.file_extensions:
                    if link.has_attr("href") and isinstance(link["href"], str):
                        href = link["href"]
                        assert isinstance(href, str)
                        if href.endswith(file_extension):
                            file_extension_links.append(href)
            return file_extension_links
        except requests.exceptions.RequestException as e:
            logging.debug("Error: %s", e)
            return []

    def collect_urls(self):
        """Collect all the URLs for provided file extensions from a given URL."""
        if self.process_static_pages:
            return self._collect_urls_from_static_pages()

        return []
