"""Helpers for error handling."""

from typing import Literal, NoReturn, Union, overload

ErrorMode = Literal["ignore", "raise", "return"]


@overload
def error_handler(error: Exception, error_mode: Literal["ignore"]) -> None: ...


@overload
def error_handler(error: Exception, error_mode: Literal["return"]) -> Exception: ...


@overload
def error_handler(error: Exception, error_mode: Literal["raise"]) -> NoReturn: ...


def error_handler(
    error: Exception,
    error_mode: ErrorMode,
) -> Union[None, Exception]:
    """Provide consistent error handling based on standardised error mode.

    Args:
        error (Exception): any caught Exception that needs to be handled.
        error_mode (ErrorMode): the error mode passed into caller function's args.

    Raises:
        error: raises the error object passed as args if error mode is raise.
        ValueError: if error mode is invalid, raises a ValueError.

    Returns:
        Union[None, Exception]: depending on mode, can return None (ignore),
            the error object (return) or raise the error again (raise).

    """
    validate_error_mode(error_mode)
    if error_mode == "ignore":
        return None
    if error_mode == "return":
        return error
    if error_mode == "raise":
        raise error


def validate_error_mode(error_mode: str) -> None:
    """Validate error_mode.

    Args:
        error_mode: Error mode value to validate.

    Raises:
        ValueError: If error_mode is invalid, raises ValueError.

    """
    if error_mode not in ("ignore", "raise", "return"):
        raise ValueError(f"Invalid error_mode: {error_mode!r}")
