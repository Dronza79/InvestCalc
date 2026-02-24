import re


def clear_field_digits(string):
    return re.sub(r'\D', '', string)


def div_to_ranks(string):
    digit_string = clear_field_digits(string)
    return re.sub(r'(?=(?:\d{3})+(?!\d))', ' ', digit_string).strip()
