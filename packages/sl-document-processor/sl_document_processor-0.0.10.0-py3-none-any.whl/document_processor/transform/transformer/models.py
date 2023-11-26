from typing import List, Optional

from pydantic import BaseModel, Field


class ScrapeSettings(BaseModel):
    """Scrape settings for the Transformer model."""

    request_wait_time: int = Field(
        description="Time to wait between requests.", default=1
    )


class ElementSettings(BaseModel):
    name: str = Field(..., description="Name of the element.")
    description: Optional[str] = Field(
        description="Description of the element.", default=""
    )
    selector: str = Field(..., description="Selector of the element.")
    selector_type: str = Field(..., description="Selector type of the element.")
    elements: Optional[List["ElementSettings"]] = Field(
        description="Nested elements of the element.", default=None
    )


class SourceSettings(BaseModel):
    """Source settings for the Transformer model."""

    url: str = Field(..., description="URL of the source.")
    elements: List[ElementSettings] = Field(..., description="Elements of the source.")


class TransformerConfig(BaseModel):
    """Configuration for the Transformer model."""

    name: str = Field(..., description="Name of the bot.")
    description: Optional[str] = Field(description="Description of the bot.")
    version: str = Field(..., description="Version of the model.")
    author: Optional[str] = Field(description="Author of the model.")
    author_email: Optional[str] = Field(description="Author email of the model.")
    bot_license: Optional[str] = Field(
        description="License of the model.", default="MIT"
    )
    scrape_settings: ScrapeSettings = Field(
        ..., description="Scrape settings of the model."
    )
    source_settings: SourceSettings = Field(
        ..., description="Source settings of the model."
    )
