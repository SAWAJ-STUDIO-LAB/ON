from A_core.A6_print_logger import log
from typing import Optional

def log_api(name: str, api: str, status: str, detail: Optional[str] = "") -> None:
    """
    Log API call results to the console and send a message to Telegram.

    Args:
        name (str): The name of the module or component.
        api (str): The API endpoint or function being called.
        status (str): The status of the API call (e.g., success, failed).
        detail (str, optional): Additional details about the API call. Defaults to an empty string.

    Returns:
        None
    """
    log(f"  ★ {name} :: {api} → {status}")
    try:
        from A_core.A20_tg_api_call import api_call
        api_call(name, api, status, detail)
    except ImportError as e:
        log(f"ImportError: Failed to import A_core.A20_tg_api_call. Error: {str(e)}")
        # Log the error to a file or database for further analysis
        with open('api_errors.log', 'a') as error_log:
            error_log.write(f"ImportError: {str(e)} during API logging for {name}, {api}, {status}, {detail}\n")
