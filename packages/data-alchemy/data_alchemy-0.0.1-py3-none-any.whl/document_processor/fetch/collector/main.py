import logging
from typing import List

import requests
import yaml

from bs4 import BeautifulSoup

from document_processor.fetch.downloader.models import URLInformation
from document_processor.fetch.utils import fetch_unique_id, is_valid_url

from .models import CollectorConfiguration as Configuration, CollectorOptions


class Collector:
    """
    This class is used to collect all the URLs from a given website.
    - url_info: The URL to collect the extension-specific URLs from.
    """

    def __init__(self, configuration: Configuration):
        options = configuration.options
        options_file_path = configuration.options_file
        if not options and options_file_path:
            options = self._load_options_from_file(options_file_path)

        self.url = options.url
        self.max_depth = options.max_depth
        self.file_extensions = options.file_extensions
        self.process_static_pages = options.process_static_pages
        self.include_html = options.include_html

    def _load_options_from_file(self, options_file_path: str):
        with open(options_file_path, "rb") as stream:
            data = yaml.safe_load(stream)
        options = CollectorOptions.model_validate(data.get("source_settings", {}))
        return options

    def _collect_urls_from_static_pages(self) -> List[URLInformation]:
        """
        Collect all the URLs for provided file extensions from a given URL.
        This method will only collect URLs from the static pages of the website.
        """
        try:
            response = requests.get(self.url, timeout=5)
            soup = BeautifulSoup(response.content, "html.parser")

            links = soup.find_all("a", href=True)

            collected_urls = (
                []
                if not self.include_html
                else [
                    URLInformation(
                        url=self.url, name=fetch_unique_id(self.url), url_type="html"
                    )
                ]
            )

            for link in links:
                for file_extension in self.file_extensions:
                    if link.has_attr("href") and isinstance(link["href"], str):
                        href = link["href"]
                        assert isinstance(href, str)

                        if href.endswith(file_extension) and is_valid_url(href):
                            collected_urls.append(
                                URLInformation(
                                    url=href,
                                    name=fetch_unique_id(href),
                                    url_type=href.split("/")[-1].split(".")[1],
                                )
                            )

            return collected_urls
        except requests.exceptions.RequestException as e:
            logging.debug("Error: %s", e)
            return []

    def collect_urls(self):
        """Collect all the URLs for provided file extensions from a given URL."""
        if self.process_static_pages:
            return self._collect_urls_from_static_pages()

        return []
