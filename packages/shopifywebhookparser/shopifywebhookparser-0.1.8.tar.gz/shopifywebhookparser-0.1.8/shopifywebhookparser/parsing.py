import logging
import json
from typing import Any, Callable, Tuple

from azure.functions import HttpRequest

from .models import ParsedWebhook

logger = logging.getLogger(__name__)
ParseFn = Callable[[Any], Tuple[bytes, dict[str, Any]]]


def create_parsed_webhook(req: HttpRequest, strategy: ParseFn) -> ParsedWebhook:
    """
    Parses an incoming HTTP request and creates a ParsedWebhook instance using the provided strategy.

    Args:
        req (HttpRequest): The incoming HTTP request.
        strategy (ParseFn): A callable strategy for parsing the request.

    Returns:
        ParsedWebhook: A dataclass instance containing parsed webhook data.

    Raises:
        ValueError: If the request cannot be parsed as JSON.
        RuntimeError: If the strategy function fails.
    """
    try:
        data_bytes, headers = strategy(req)
        try:
            payload = json.loads(data_bytes)
        except json.JSONDecodeError:
            logger.error("Failed to parse request body as JSON", exc_info=True)
            raise ValueError("Invalid JSON in request body")
    except Exception as e:
        logger.error(f"Failed to parse request using strategy: {e}", exc_info=True)
        raise RuntimeError("Error parsing request") from e

    return ParsedWebhook(payload=payload, attributes=headers)


def parse_verification_params(req: Any, strategy: ParseFn) -> Tuple[bytes, str, str]:
    """
    Parses the incoming Shopify webhook request using the provided strategy to extract verification parameters.

    Args:
        req (Any): The request object to parse.
        strategy (ParseFn): A callable that implements the parsing logic.

    Returns:
        Tuple[bytes, str, str]: A tuple containing the request body in bytes, HMAC SHA256 string, and online store name.

    Raises:
        ValueError: If required headers are missing or if the request cannot be parsed.
    """
    try:
        data_bytes, headers = strategy(req)
        hmac_sha256 = headers.get("X-Shopify-Hmac-Sha256")
        onlinestore_name = headers.get("X-Shopify-Shop-Domain").split(".")[0].lower()

        if not hmac_sha256 or not onlinestore_name or not data_bytes:
            logger.error("Missing required Shopify headers", exc_info=True)
            raise ValueError("Missing required Shopify headers")

        logger.info("Extracted verification parameters")
        return data_bytes, hmac_sha256, onlinestore_name
    except Exception as e:
        logger.error(f"Error parsing Shopify webhook request: {e}", exc_info=True)
        raise ValueError("Failed to parse Shopify webhook request") from e


def azure_strategy(req: HttpRequest) -> Tuple[bytes, dict[str, Any]]:
    """
    Parses the incoming Shopify webhook request for Azure Function.

    Args:
        req (HttpRequest): The Azure Function HTTP request object.

    Returns:
        Tuple[bytes, dict[str, Any]]: A tuple containing the request body in bytes and headers.

    Raises:
        ValueError: If required headers are missing or request parsing fails.
    """
    try:
        body = req.get_body()
        headers = req.headers
        logger.info("Parsed Azure Function request body and headers")
        return body, headers
    except Exception as e:
        logger.error(
            f"Error in Azure Function request parse strategy: {e}", exc_info=True
        )
        raise ValueError(
            "Failed to parse Azure Function Shopify webhook request"
        ) from e
