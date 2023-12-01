# models.py
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ParsedWebhook:
    """
    Represents a parsed Shopify webhook request.

    Attributes:
        payload (Dict[str, Any]): The main content of the webhook, typically parsed from JSON.
        attributes (Dict[str, str]): The headers from the webhook request.
        source_url (str): The source URL of the webhook, extracted from the headers.
        onlinestore_name (str): The name of the online store, derived from the source URL.
        topic (str): The topic of the webhook, extracted from the headers.

    The `source_url`, `onlinestore_name`, and `topic` attributes are set in the `__post_init__` method
    based on the provided `attributes`.
    """

    payload: dict[str, Any]
    attributes: dict[str, str]
    source_url: str = field(init=False)
    onlinestore_name: str = field(init=False)
    topic: str = field(init=False)

    def __post_init__(self):
        """
        Post-initialization processing to set derived attributes.
        Extracts the source URL, online store name, and topic from the provided attributes.
        """
        self.source_url = self.attributes.get("X-Shopify-Shop-Domain", "")
        self.onlinestore_name = self.source_url.split(".")[0] if self.source_url else ""
        self.topic = self.attributes.get("X-Shopify-Topic", "")
