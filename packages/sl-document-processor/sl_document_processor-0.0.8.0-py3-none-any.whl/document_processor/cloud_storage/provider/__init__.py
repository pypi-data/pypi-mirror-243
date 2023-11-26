"""
Module to handle cloud storage providers
"""

__all__ = ["CloudCredentials", "AWSCloudStorage"]

from ._base_storage import CloudCredentials
from .aws_storage import AWSCloudStorage
