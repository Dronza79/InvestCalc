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
    num = int(float(str(digit).replace(',', '.')))
    digit = str(digit).replace('.', ',')
    if num % 10 == 1 and num % 100 != 11:
        return f'{digit} года'
    return f'{digit} лет'


def clear_field_percent(string: str):
    string = re.sub(r'[^\d.,]', '', string)
    string = string.replace(',', '.')
    if '.' in string:
        part = string.split('.')
        part.insert(1, '.')
        string = ''.join(part)
    return string


def clear_field_horizon(string: str):
    string = re.sub(r'[^\d.,]', '', string)
    string = string.replace(',', '.')
    if re.search(r'^\d{1,2}$', string):
        return string
    elif re.search(r'^(0[1-9]|[12][0-9]|3[01]\.)$|^(\d{2}\.)$', string):
        return string
    elif re.search(r'^(0[1-9]|[12][0-9]|3[01]\.[0-1])$|^(\d{2}\.\d)$', string):
        return string
    elif re.search(r'^(0[1-9]|[12][0-9]|3[01]\.(0[1-9]|1[0-2]))$|^(\d{2}\.\d{2})$', string):
        return string
    elif re.search(r'^(0[1-9]|[12][0-9]|3[01]\.(0[1-9]|1[0-2])\.)$|^(\d{2}\.\d{3})$', string):
        return string
    elif re.search(r'^(0[1-9]|[12][0-9]|3[01]\.(0[1-9]|1[0-2])\.2)$', string):
        return string
    elif re.search(r'^(0[1-9]|[12][0-9]|3[01]\.(0[1-9]|1[0-2])\.20)$', string):
        return string
    elif re.search(r'^(0[1-9]|[12][0-9]|3[01]\.(0[1-9]|1[0-2])\.20[2-9])$', string):
        return string
    elif re.search(r'^(0[1-9]|[12][0-9]|3[01]\.(0[1-9]|1[0-2])\.20[2-9]\d)$', string):
        return string
    return string[:-1]

