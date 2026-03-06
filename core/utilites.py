import re
from datetime import datetime as dd, date

from dateutil.relativedelta import relativedelta

from gui.models import Period


def clear_field_digits(string):
    return re.sub(r'[^\d.,]', '', str(string)).replace('.', ',')


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


def format_years_genitive(horizon):
    string = f'{horizon.years} лет'

    if horizon.years % 10 == 1 and horizon.years % 100 != 11:
        string = f'{horizon.years} года'

    if horizon.months:
        string += f' {horizon.months} месяцев'

    return string


def clear_field_percent(string: str):
    string = re.sub(r'[^\d.,]', '', str(string).replace('.', ','))

    if re.fullmatch(r'\d{0,2}(?:,\d{0,2})?', string):
        return string
    return string[:-1]


def clear_field_horizon(string: str):
    string = re.sub(r'[^\d.,]', '', str(string))
    count_sep = string.count('.') + string.count(',')
    string = (
        string.replace(',', '.') if count_sep > 1 else
        string.replace('.', ',')
    )

    day_p = r'(?:0[1-9]|[12][0-9]|3[01]|[1-9])'
    month_p = r'(?:0[1-9]|1[0-2]|[1-9])'
    year_p = r'(?:2(?:0(?:[2-9]\d?)?)?)'
    number = r'(?:\d|[1-4]\d)'
    dec = r'\d{0,2}'

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
            # Если дата не существует блокировать ввод
            return string[:-1]

    return string


def reformat_raw_input_data(
        horizon: str, payment_step: Period, profit_step: Period, rate: str,
        ratio: str, type_calc: str, tax_enabled: bool, inf_enabled: bool,
        ltab, pay_enabled, **raw_data
):
    valid_data = {}
    field_money_input = []

    if ltab == '-INVEST-':
        field_money_input = ['capital', 'payment', 'initial']
        valid_data = {
            'period_payment': payment_step,
            'period_profit': profit_step,
            'rate': float(rate.replace(',', '.')),
            'ratio': int(ratio),
            'tax_enabled': tax_enabled,
            'inf_enabled': inf_enabled,
        }

        if horizon:
            start_date = dd.now().date()
            try:
                end_date = dd.strptime(horizon, '%d.%m.%Y').date()
                horizon = relativedelta(end_date, start_date)
            except ValueError:
                y = float(horizon.replace(',', '.'))
                m = (y - int(y)) * 12
                d = (m - int(m)) * 30.44
                horizon = relativedelta(years=int(y), months=int(m), days=int(d))
                end_date = start_date + horizon
            for key, data in {'horizon': horizon, 'start_date': start_date, 'end_date': end_date}.items():
                valid_data[key] = data

    elif ltab == '-BALANCE-':
        field_money_input = [
            'balance_capital', 'stocks', 'bonds', 'funds', 'metals',
            'percent_stocks', 'percent_bonds', 'percent_funds',
            'percent_metals', 'partial_repl'
        ]

        valid_data['pay_enabled'] = pay_enabled

    for key in field_money_input:
        valid_data[key] = round(float(raw_data[key].replace(' ', '').replace(',', '.')), 2) if raw_data[key] else 0

    valid_data['type_calc'] = type_calc

    return valid_data


def check_for_day_week(date_value):
    week_day = date_value.weekday()
    return (
        date_value if week_day < 5 else
        date_value + relativedelta(days=1) if week_day > 5 else
        date_value + relativedelta(days=2)
    )
