# Shopify Webhook Parser
The Shopify Webhook Parser is a versatile Python module designed for efficient parsing of Shopify webhook requests. While it includes a specific implementation for Azure Functions, its architecture is flexible, allowing it to be extended and adapted to various environments and requirements.

## Features
- **Strategy Pattern:** At the core of this module lies the Strategy pattern, enabling dynamic selection and interchangeability of parsing logic. This approach allows for the easy addition of new parsing strategies to accommodate different processing needs or webhook formats.
- **Extendable for Various Environments:** Initially provided with an implementation for Azure Functions, the module is structured to be easily extendable to other platforms or frameworks.
- **Robust Error Handling:** Incorporates comprehensive error handling to manage and log parsing exceptions, ensuring reliability and maintainability.
- **Customizable Parsing Strategies:** Designed to cater to a range of webhook parsing needs, from simple to complex, the module is both customizable and scalable, fitting into different project sizes and complexities.

## Implementing New Parsing Strategies
To integrate new parsing strategies, follow these guidelines:
1. **Strategy Function Signature**:
    - Implement strategies as callables conforming to the following type: `(HttpRequest) -> Tuple[bytes, Dict[str, Any]]`.
    - These functions should accept a webhook request and return a tuple with the request body in bytes and headers.
2. **Error Management**:
    - Strategies should handle and log exceptions effectively.
    - Raise a `ValueError` with a descriptive message in case of processing failure.
3. **Seamless Integration**:
    - Design strategies for easy integration with the `parse_shopify_webhook_request` function.
    - Ensure compatibility with expected input types.
4. **Comprehensive Testing**:
    - Thoroughly test each strategy to accurately parse various webhook formats.
    - Include tests for edge cases and error handling scenarios.


## Installation
```bash
pip install shopifywebhookparser
```

## Usage
To use this module in an Azure Function, import and call the parse_shopify_webhook_request function with the appropriate parsing strategy.

### Example
```python
import azure.functions as func
from shopifywebhookparser import parse_shopify_webhook_request, azure_func_request_parse_strategy

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        onlinestore_name, data_bytes, headers, hmac_sha256 = parse_shopify_webhook_request(
            req, azure_func_request_parse_strategy
        )
        # Further processing of the parsed data
        return func.HttpResponse(f"Processed webhook for store: {onlinestore_name}", status_code=200)
    except ValueError as e:
        return func.HttpResponse(f"Error: {e}", status_code=400)

```
## Development and Contributions
Feel free to contribute to the improvement of this module by submitting pull requests or reporting issues.

## Logging
The module uses Python's built-in logging to provide insights into its operations and error conditions.

## License
MIT, for details see LICENSE

