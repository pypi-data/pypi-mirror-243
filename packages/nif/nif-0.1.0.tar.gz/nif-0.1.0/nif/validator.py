from nif.exceptions import NIFException
from nif.control import get_control_digit
from nif import cleaner


def validate(
    nif: str | int | float,
    coerce: bool = True,
    clean: bool = True,
    raise_exceptions: bool = False,
):
    """
    Validate a NIF (Número de Identificação Fiscal) number.

    Args:
        nif (str): The NIF number to validate.
        coerce (bool, optional): Whether to coerce the NIF number to string if it's an integer or a float.
                                Defaults to True.
        clean (bool, optional): Whether to clean the NIF number by removing spaces, hyphens and special characters.
                                Defaults to True.
        raise_exceptions (bool, optional): Whether to raise exceptions when validation fails.
                                           Defaults to False.

    Returns:
        bool: True if the NIF number is valid, False otherwise.

    Raises:
        NIFException: If the NIF number is invalid and raise_exceptions is True.

    Examples:
        >>> validate('123456789')
        True

        >>> validate('987654322')
        True

        >>> validate('12345678')
        False
    """
    if raise_exceptions:
        return _validate(nif, coerce, clean)
    try:
        return _validate(nif, coerce, clean)
    except NIFException:
        return False


def _validate(nif: str | int | float, coerce: bool, clean: bool):
    if coerce and not clean:
        nif = cleaner.coerce_to_string(nif)
    elif clean:
        nif = cleaner.clean(nif, coerce)

    validate_only_digits(nif)
    if len(nif) != 9:
        raise NIFException("NIF should have 9 digits")
    expected_control_digit = get_control_digit(nif[:-1])
    control_digit = nif[-1]
    if expected_control_digit != control_digit:
        raise NIFException(
            f"Control digit does not match: expected {expected_control_digit} but got {control_digit}."
        )
    return True


def validate_only_digits(value: str) -> bool:
    """Validates if a string only contains digits
    >>> validate_only_digits('12345678')
    True
    >>> validate_only_digits('12345678a')
    False
    """
    if value is None or not value.isdigit():
        raise NIFException("NIF should only contain digits")
    return True
