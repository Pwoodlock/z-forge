"""
Z-Forge Model Fetcher
Fetches available models from LM Studio server using the EA_LMStudio pattern.

Features:
- Cached model list with manual refresh
- Graceful error handling
- Custom model fallback option
"""
import logging
from typing import Optional

logger = logging.getLogger("ZForge")

# Module-level cache
_cached_models: list[str] = []
_last_fetch_error: Optional[str] = None

# Special option for custom model input
CUSTOM_MODEL_OPTION = ">> Custom Model <<"


def fetch_models_from_server(
    server_url: str, timeout: float = 5.0
) -> tuple[list[str], Optional[str]]:
    """
    Fetch models via /v1/models REST endpoint.

    Args:
        server_url: Base URL of LM Studio server (e.g., "http://127.0.0.1:1234")
        timeout: Request timeout in seconds

    Returns:
        Tuple of (list of model IDs, error message or None)
    """
    try:
        import requests
    except ImportError:
        return [], "requests library not installed"

    try:
        endpoint = f"{server_url.rstrip('/')}/v1/models"
        response = requests.get(endpoint, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        # Extract model IDs from response
        models = [m.get("id", "") for m in data.get("data", [])]
        return [m for m in models if m], None

    except requests.exceptions.ConnectionError:
        return [], "Connection refused - is LM Studio running with server enabled?"
    except requests.exceptions.Timeout:
        return [], f"Connection timed out after {timeout}s"
    except requests.exceptions.HTTPError as e:
        return [], f"HTTP error: {e.response.status_code}"
    except Exception as e:
        return [], str(e)


def get_model_choices() -> list[str]:
    """
    Get model choices for dropdown widget.

    Returns:
        List with custom option first, followed by cached models
    """
    choices = [CUSTOM_MODEL_OPTION]
    if _cached_models:
        choices.extend(_cached_models)
    return choices


def refresh_model_cache(server_url: str, timeout: float = 5.0) -> tuple[bool, str]:
    """
    Refresh the model cache from server.

    Args:
        server_url: Base URL of LM Studio server
        timeout: Request timeout in seconds

    Returns:
        Tuple of (success boolean, status message)
    """
    global _cached_models, _last_fetch_error

    models, error = fetch_models_from_server(server_url, timeout)

    if error:
        _last_fetch_error = error
        return False, error

    _cached_models = models
    _last_fetch_error = None
    return True, f"Found {len(models)} model(s)"


def get_last_error() -> Optional[str]:
    """Get the last fetch error, if any."""
    return _last_fetch_error


def get_cached_models() -> list[str]:
    """Get the currently cached models."""
    return _cached_models.copy()


def initialize_model_cache(host: str = "127.0.0.1", port: int = 1234) -> None:
    """
    Initialize cache at startup (silent failure).

    Called when ComfyUI loads the extension. Attempts to fetch models
    but does not raise errors if server is unavailable.

    Args:
        host: LM Studio server host
        port: LM Studio server port
    """
    server_url = f"http://{host}:{port}"
    success, msg = refresh_model_cache(server_url, timeout=3.0)

    if success:
        logger.info(f"Z-Forge: {msg}")
    else:
        logger.warning(f"Z-Forge model fetch: {msg}")


def test_connection(host: str, port: int, timeout: float = 5.0) -> tuple[bool, str]:
    """
    Test connection to LM Studio server.

    Args:
        host: Server host
        port: Server port
        timeout: Request timeout

    Returns:
        Tuple of (success boolean, status message)
    """
    try:
        import requests
    except ImportError:
        return False, "requests library not installed"

    server_url = f"http://{host}:{port}"

    try:
        # Try to hit the models endpoint
        endpoint = f"{server_url}/v1/models"
        response = requests.get(endpoint, timeout=timeout)
        response.raise_for_status()

        data = response.json()
        model_count = len(data.get("data", []))

        return True, f"Connected! {model_count} model(s) available"

    except requests.exceptions.ConnectionError:
        return False, f"Cannot connect to {server_url} - is LM Studio running?"
    except requests.exceptions.Timeout:
        return False, f"Connection timed out after {timeout}s"
    except requests.exceptions.HTTPError as e:
        return False, f"Server error: {e.response.status_code}"
    except Exception as e:
        return False, f"Error: {e}"
