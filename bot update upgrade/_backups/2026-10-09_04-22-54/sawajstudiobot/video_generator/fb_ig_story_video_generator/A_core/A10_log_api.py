from A_core.A6_print_logger import log


def log_api(name, api, status, detail=""):
    """
    Log API call results to the console and possibly to Telegram.

    Args:
        name (str): Name of the module.
        api (str): API being called.
        status (str): Result status of the API call.
        detail (str, optional): Additional details. Defaults to "".
    """
    log(f"  ★ {name} :: {api} → {status}")
    try:
        from A_core.A20_tg_api_call import api_call
        api_call(name, api, status, detail)
    except ImportError as e:
        log(f"Import error: {str(e)} during API logging.")
