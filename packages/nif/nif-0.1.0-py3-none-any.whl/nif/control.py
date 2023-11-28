from nif.exceptions import NIFException


def get_control_digit(nif: str) -> str:
    """Calculates the control digit from a NIF Ex. 99999999[0]
    >>> check_digit('99999999')
    '0'
    >>> check_digit('74089837')
    '0'
    >>> check_digit('28702400')
    '8'
    """
    if len(nif) != 8:
        raise NIFException("NIF (without the control digit) should have 8 digits")

    total = sum([int(digit) * (9 - pos) for pos, digit in enumerate(nif)])
    rest = total % 11
    if rest == 0 or rest == 1:
        return "0"
    return str(11 - rest)
