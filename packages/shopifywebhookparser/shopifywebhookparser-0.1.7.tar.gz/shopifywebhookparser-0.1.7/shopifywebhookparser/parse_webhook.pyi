# webhook_parser.pyi

from typing import Any, Callable, Tuple, Dict

ParseFn = Callable[[Any], Tuple[str, bytes, Dict[str, Any], str, str]]

def parse_shopify_webhook_request(req: Any, parse_strategy: ParseFn) -> Tuple[str, bytes, Dict[str, Any], str, str]: ...

def azure_func_request_parse_strategy(req: Any) -> Tuple[str, bytes, Dict[str, Any], str, str]: ...
