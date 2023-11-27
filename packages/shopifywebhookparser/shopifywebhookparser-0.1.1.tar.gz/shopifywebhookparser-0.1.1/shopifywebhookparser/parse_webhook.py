import logging
from typing import Any, Callable, Tuple
import azure.functions as func

# Set up logging
logger = logging.getLogger("ShopifyWebhookParser")
logger.setLevel(logging.INFO)

ParseFn = Callable[[Any], Tuple[str, bytes, dict[str, Any], str]]


def parse_shopify_webhook_request(
    req: Any, parse_strategy: ParseFn
) -> Tuple[str, bytes, dict[str, Any], str]:
    """
    Parses the incoming Shopify webhook request using the provided strategy.

    Args:
        req (Any): The request object to parse.
        parse_strategy (ParseFn): A callable that implements the parsing logic.

    Returns:
        Tuple[str, bytes, dict[str, Any], str, str]: A tuple containing the online store name,
        request body in bytes, headers, HMAC SHA256 string, and topic.

    Raises:
        ValueError: If the parsing strategy fails to process the request.
    """
    try:
        return parse_strategy(req)
    except Exception as e:
        logger.error(f"Error parsing Shopify webhook request: {e}")
        raise ValueError("Failed to parse Shopify webhook request") from e


def azure_func_request_parse_strategy(
    req: func.HttpRequest,
) -> Tuple[str, bytes, dict[str, Any], str, str]:
    """
    Parses the incoming Shopify webhook request for Azure Function.

    Args:
        req (func.HttpRequest): The Azure Function HTTP request object.

    Returns:
        Tuple[str, bytes, dict[str, Any], str]: A tuple containing the online store name,
        request body in bytes, headers, and the HMAC SHA256 string.

    Raises:
        ValueError: If required headers are missing or request parsing fails.
    """
    try:
        onlinestore_name = req.headers.get("X-Shopify-Shop-Domain").split(".")[0].lower()  # type: ignore
        data_bytes = req.get_body()
        headers = req.headers
        hmac_sha256 = req.headers.get("X-Shopify-Hmac-Sha256")
        topic = req.headers.get("X-Shopify-Topic")

        if not (onlinestore_name and hmac_sha256):
            raise ValueError("Missing required Shopify headers")

        return onlinestore_name, data_bytes, headers, hmac_sha256, topic  # type: ignore
    except Exception as e:
        logger.error(f"Error in Azure Function request parse strategy: {e}")
        raise ValueError(
            "Failed to parse Azure Function Shopify webhook request"
        ) from e
