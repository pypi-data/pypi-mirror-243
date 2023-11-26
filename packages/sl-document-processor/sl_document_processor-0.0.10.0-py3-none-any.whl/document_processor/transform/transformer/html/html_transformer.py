from document_processor.transform.transformer.base_transformer import BaseTransformer

from document_processor.transform.transformer.models import TransformerConfig

from .parser import BeautifulSoupParser


class HTMLTransformer(BaseTransformer):
    """
    This class transforms a given HTML file OR URL into a common format utilsiing the configuration provided.
    """

    def __init__(self, configuration: TransformerConfig):
        super().__init__(configuration=configuration)

    def parse(self):
        """Parse the HTML file."""
        parser = BeautifulSoupParser(configuration=self.transformer_config)
        return parser.parse()
