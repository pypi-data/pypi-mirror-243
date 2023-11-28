from typing import List

import requests
from bs4 import BeautifulSoup, element as BS4Element, ResultSet as Res
from lxml import etree

from document_processor.transform.transformer.models import (
    ElementSettings,
    TransformerConfig,
)

from .base_parser import BaseParser


class BeautifulSoupParser(BaseParser):
    def __init__(self, configuration: TransformerConfig):
        super().__init__(configuration)
        self.soup = self._get_soup()

    def _get_soup(self):
        response = requests.get(self.url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def parse(self):
        return self._parse(
            [self.soup.select("body")[0]], self.configuration.source_settings.elements
        )

    def _parse(
        self,
        parent_elements: List[BS4Element.Tag],
        child_elements: List[ElementSettings],
    ):
        """Parse the HTML file."""
        parsed_elements = []
        for selected_html_elment in parent_elements:
            for element in child_elements:
                temp_dict = {}
                if element.selector_type == "css":
                    tag, class_ = element.selector.split(".")
                    child_tags = self.parse_css_selector(
                        selected_html_elment, tag=tag, class_=class_
                    )
                    if element.elements is not None:
                        temp_dict[element.name] = self._parse(
                            child_tags, element.elements
                        )
                    else:
                        temp_dict[element.name] = [
                            child_tag.text for child_tag in child_tags
                        ]
                elif element.selector_type == "xpath":
                    child_tags = self.parse_xpath(
                        selected_html_elment, element.selector
                    )
                    if element.elements is not None:
                        temp_dict[element.name] = self._parse(
                            child_tags, element.elements
                        )
                    else:
                        temp_dict[element.name] = child_tags

                parsed_elements.append(temp_dict)

        return parsed_elements

    def parse_xpath(self, ele_tag: BS4Element.Tag, xpath_selector: str):
        """Parse the HTML file."""
        html_str = str(ele_tag)
        html_parser = etree.HTMLParser()
        tree: etree._Element = etree.fromstring(html_str, html_parser)
        parsed_elements = tree.xpath(xpath_selector)
        return parsed_elements

    def parse_css_selector(
        self, ele_tag: BS4Element.Tag, tag: str, class_: str
    ) -> Res[BS4Element.Tag]:
        """Parse the HTML file."""
        try:
            return ele_tag.find_all(tag, class_=class_)
        except Exception as e:
            print(f"Could not find tag: {tag} with class: {class_}")
            raise e
