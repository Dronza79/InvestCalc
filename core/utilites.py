import re
from datetime import datetime as dd


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
    string = re.sub(r'[^\d.,]', '', string.replace('.', ','))

    if re.fullmatch(r'\d{0,3}(?:,\d{0,3})?', string):
        return string
    return string[:-1]


def clear_field_horizon(string: str):
    string = re.sub(r'[^\d.,]', '', string)
    count_sep = string.count('.') + string.count(',')
    string = (
        string.replace(',', '.') if count_sep > 1 else
        string.replace('.', ',')
    )

    day_p = r'(?:0[1-9]|[12][0-9]|3[01]|[1-9])'
    month_p = r'(?:0[1-9]|1[0-2]|[1-9])'
    year_p = r'(?:2(?:0(?:[2-9]\d?)?)?)'
    number = r'(?:\d|[1-4]\d)'
    dec = r'\d{0,3}'

    valid_states = [
        fr'^(?:{number}|50)$',
        fr'^{number},{dec}$',
        rf'^{day_p}[.,]?$',
        rf'^{day_p}[.,]{month_p}?$',
        rf'^{day_p}[.,]{month_p}[,.]{year_p}?$',
    ]

    if not any(re.fullmatch(p, string) for p in valid_states):
        return string[:-1]

    if re.search(r'\.(\d{4})$', string):
        try:
            input_date = dd.strptime(string, '%d.%m.%Y').date()
            today = dd.now().date()
            if input_date <= today:
                return string[:-1]
        except ValueError:
            # Если дата не существует блокирую ввод
            return string[:-1]

    return string

