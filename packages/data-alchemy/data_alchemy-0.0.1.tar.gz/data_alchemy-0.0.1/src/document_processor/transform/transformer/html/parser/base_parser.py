import abc

from document_processor.transform.transformer.models import TransformerConfig


class BaseParser(abc.ABC):
    def __init__(self, configuration: TransformerConfig):
        self.configuration = configuration
        self.url = configuration.source_settings.url

    @abc.abstractmethod
    def parse(self):
        pass
