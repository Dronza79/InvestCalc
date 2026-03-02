import re


def clear_field_digits(string):
    return re.sub(r'\D', '', string)


def div_to_ranks(string):
    digit_string = clear_field_digits(string)
    return re.sub(r'(?=(?:\d{3})+(?!\d))', ' ', digit_string).strip()


def format_digit_years(digit):  # Именительный подеж
    num = int(float(digit))
    digit = str(digit).replace('.', ',')
    if 11 <= num % 100 <= 14:
        return f'{digit} лет'
    elif num % 10 == 1:
        return f'{digit} год'
    elif 2 <= num % 10 <= 4:
        return f'{digit} года'
    return f'{digit} лет'


def format_years_genitive(digit):
    print(f'{digit=}')
    num = int(float(digit))
    digit = str(digit).replace('.', ',')
    if num % 10 == 1 and num % 100 != 11:
        return f'{digit} года'
    return f'{digit} лет'
