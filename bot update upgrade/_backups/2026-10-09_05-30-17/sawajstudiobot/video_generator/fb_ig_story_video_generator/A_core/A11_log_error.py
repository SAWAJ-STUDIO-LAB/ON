from A_core.A6_print_logger import log


def log_error(name, error, tb=""):
    """
    Log error details to the console and possibly to Telegram.

    Args:
        name (str): Name of the module.
        error (str): Error message.
        tb (str, optional): Optional traceback details. Defaults to "".
    """
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    try:
        from A_core.A21_tg_file_error import file_error
        file_error(name, error, tb)
    except ImportError as e:
        log(f"Import error: {str(e)} during error logging.")
