from .base_transformer import BaseTransformer
from .models import TransformerConfig


class PDFTransformer(BaseTransformer):
    def __init__(self, configuration: TransformerConfig):
        super().__init__(configuration=configuration)

    def parse(self):
        """Parse the PDF file."""
        return "This is a PDF file"
