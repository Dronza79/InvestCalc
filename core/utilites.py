import re
from datetime import datetime as dd

from dateutil.relativedelta import relativedelta

from core.models import Period


def clear_field_digits(string):
    string = re.sub(r'[^\d,]', '', str(string).replace('.', ','))
    string = string.lstrip(',')
    if ',' in string:
        int_part, decimal_part = string.split(',', 1)
        decimal_part = decimal_part.replace(',', '')
        if len(decimal_part) == 1:
            decimal_part += '0'
        elif len(decimal_part) > 2:
            decimal_part = decimal_part[:1] + decimal_part[-1]
        string = f"{int_part},{decimal_part}"
    return string


def div_to_ranks(string):
    digit_string = clear_field_digits(string)
    if ',' in digit_string:
        integer_part, decimal_part = digit_string.split(',', 1)
        integer_part = re.sub(r'(?<!,)\d(?=(\d{3})+(?:,|$))', r'\g<0> ', integer_part).strip()
        return f"{integer_part},{decimal_part}"
    else:
        return re.sub(r'\d(?=(\d{3})+(?!\d))', r'\g<0> ', digit_string)


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
    string = f'{horizon.year} лет'

    if horizon.year % 10 == 1 and horizon.year % 100 != 11:
        string = f'{horizon.year} года'

    if horizon.month:
        string += f' {horizon.month} месяцев'

    return string


def format_horizon(horizon):
    def get_plural(n, forms):
        if n % 10 == 1 and n % 100 != 11:
            return forms[0]  # год / месяц
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            return forms[1]  # года / месяца
        else:
            return forms[2]  # лет / месяцев

    res = []
    if horizon.year:
        res.append(f"{horizon.year} {get_plural(horizon.year, ['год', 'года', 'лет'])}")

    if horizon.month:
        res.append(f"{horizon.month} {get_plural(horizon.month, ['месяц', 'месяца', 'месяцев'])}")

    return " ".join(res)


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
            'ratio': ratio,
            'tax_enabled': tax_enabled,
            'inf_enabled': inf_enabled,
        }

        if rate:
            valid_data['rate'] = float(rate.replace(',', '.'))

        if horizon:
            start_date = dd.now().date()
            try:
                end_date = dd.strptime(horizon, '%d.%m.%Y').date()
                horizon = Period('horizon', relativedelta(end_date, start_date))
            except ValueError:
                y = float(horizon.replace(',', '.'))
                m = (y - int(y)) * 12
                d = (m - int(m)) * 30.44
                horizon = Period('horizon', relativedelta(years=int(y), months=int(m), days=int(d)))
                end_date = start_date + horizon
            valid_data.update({'horizon': horizon, 'start_date': start_date, 'end_date': end_date})
        else:
            valid_data['start_date'] = dd.now().date()

    elif ltab == '-BALANCE-':
        field_money_input = [
            'balance_capital', 'stocks', 'bonds', 'funds', 'metals',
            'partial_repl', 'percent_stocks', 'percent_bonds',
            'percent_funds', 'percent_metals'
        ]

        valid_data['pay_enabled'] = pay_enabled

    for key in field_money_input:
        value = (
            int(raw_data[key].replace(' ', '')) if raw_data[key].replace(' ', '').isdigit()
            else round(float(raw_data[key].replace(' ', '').replace(',', '.')), 2) if raw_data[key]
            else 0
        )
        # if key == 'payment' and not value:
        #     continue
        valid_data[key] = value

    valid_data['type_calc'] = type_calc

    return valid_data


def check_for_day_week(date_value):
    return date_value
    # week_day = date_value.weekday()
    # return (
    #     date_value if week_day < 5 else
    #     date_value + relativedelta(days=1) if week_day > 5 else
    #     date_value + relativedelta(days=2)
    # )


def format_digit_for_graph(digit):
    try:
        digit = float(digit)
    except (ValueError, TypeError):
        return '0'

    if digit <= 0:
        return '0'

        # МИЛЛИАРДЫ: до 1 знака (1.1М)
    if digit >= 1e9:
        val = f"{digit / 1e9:.1f}".rstrip('0').rstrip('.')
        return f"{val}М".replace('.', ',')

        # МИЛЛИОНЫ: до 2 знаков (1,1кк или 1,12кк)
    if digit >= 1e6:
        # :.2f сделает 1.101 -> "1.10", а rstrip('0') уберет ноль -> "1.1"
        val = f"{digit / 1e6:.2f}".rstrip('0').rstrip('.')
        return f"{val}кк".replace('.', ',')

        # ТЫСЯЧИ: целые (12к)
    if digit >= 1e3:
        return f"{int(digit / 1e3)}к"

        # ОСТАЛЬНОЕ: целые (999)
    return str(int(digit))


def get_color(val):
    return 'Darkred' if val < 0 else 'Darkgreen' if val > 0 else 'DimGrey'


def get_text(val):
    return (
        f'КУПИТЬ на {div_to_ranks(abs(val))}\u20BD' if val > 0 else
        f'ПРОДАТЬ на {div_to_ranks(abs(val))}\u20BD' if val < 0 else
        "ДЕРЖАТЬ"
    )
