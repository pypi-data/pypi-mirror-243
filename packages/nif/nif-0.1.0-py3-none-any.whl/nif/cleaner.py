from nif.exceptions import NIFException
import re


def coerce_to_string(nif: str | int | float) -> str:
    """
    Coerces the given NIF to string if it is an integer or a float.

    Args:
        nif (str | int | float): The NIF to be coerced.

    Returns:
        str: The coerced NIF.

    Raises:
        NIFException: If the NIF is not a string or an integer with only digits.

    Examples:
        >>> coerce_to_string("123456789")
        '123456789'

        >>> coerce_to_string(123456789)
        '123456789'

        >>> coerce_to_string(123456789.0)
        '123456789'
    """
    if isinstance(nif, int) or isinstance(nif, float):
        nif = str(int(nif))
    elif not isinstance(nif, str):
        raise NIFException("NIF should be a string or an integer with only digits")

    return nif


def clean(nif: str | int | float, coerce: bool = True) -> str:
    """
    Standardizes the given NIF by removing any spaces or dashes,
    and padding with leading zeros if it is an integer.

    Args:
        nif (str | int): The NIF to be standardized.

    Returns:
        str: The standardized NIF.

    Raises:
        NIFException: If the NIF is not a string or an integer with only digits.

    Examples:
        >>> standardise("123-456-789")
        '123456789'

        >>> standardise("123 456 789")
        '123456789'

        >>> standardise(123456789)
        '123456789'

        >>> standardise("  987654321  ")
        '987654321'
    """
    if coerce:
        nif = coerce_to_string(nif)
    nif = re.sub("[^0-9]", "", nif)

    return nif
