SEPARATOR = ','


def _recursive_translate(num: str, group: int) -> str:
    if len(num) > group:
        return _recursive_translate(num[:-group], group) + SEPARATOR + num[-group:]

    return num


def translate(number: int, group:int=3) -> str:
    '''
    Takes an integer and returns a string representation of
    that integer with commas separating groups of digits,
    by default 3 digits per group.
    '''
    str_number = str(abs(number))

    result = _recursive_translate(str_number, group)

    if number < 0:
        result = '-' + result

    return result
