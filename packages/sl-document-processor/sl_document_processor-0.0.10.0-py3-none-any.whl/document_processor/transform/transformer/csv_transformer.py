from .base_transformer import BaseTransformer

from .models import TransformerConfig


class CSVTransformer(BaseTransformer):
    def __init__(self, configuration: TransformerConfig):
        super().__init__(configuration=configuration)

    def parse(self):
        """Parse the PDF file."""
        return "This file type is not supported yet!"
