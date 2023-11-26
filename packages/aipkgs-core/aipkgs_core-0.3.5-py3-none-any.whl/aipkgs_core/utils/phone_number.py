import phonenumbers


def is_number_format_valid(number: str) -> (bool, str):
    try:
        parsed_number = phonenumbers.parse(number, None)
        return True, parsed_number
    except:
        return False, number


def is_valid_number(number: str):
    return phonenumbers.is_valid_number(number)
