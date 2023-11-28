import abc
from typing import Optional

from .models import TransformerConfig


class BaseTransformer(abc.ABC):
    path: Optional[str]
    url: Optional[str]
    text: Optional[str]

    def __init__(self, configuration: TransformerConfig):
        self.transformer_config = TransformerConfig.model_validate(configuration)

    @abc.abstractmethod
    def parse(self) -> list:
        """Parse the file."""
