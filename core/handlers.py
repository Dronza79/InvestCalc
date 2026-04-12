from dateutil.relativedelta import relativedelta

from core.config import *
from core.models import Period


def calculate_tax(year_profit):
    """Расчет прогрессивного налога."""
    if year_profit <= TAX_THRESHOLD:
        return year_profit * TAX_LOW

    if year_profit > TAX_THRESHOLD:
        low_part = TAX_THRESHOLD
        high_part = year_profit - low_part
        return (low_part * TAX_LOW) + (high_part * TAX_HIGH)


def calculate_gains(start_date, end_date, initial, payment, rate, period_payment,
                    period_profit, tax_enabled, inf_enabled, ratio, **kwargs):
    """
    Основной движок с логикой капитализации и налогов.
    """
    result = {}
    current_balance = initial
    total_deposit = current_balance
    total_income = 0
    total_taxes = 0
    year_profit = 0.0
    accumulated_profit = 0.0
    profit_12_month = 0
    graph_data = [[0], [initial + payment], [0]]
    table_data = []
    calendar_year_date = start_date + relativedelta(years=1)
    count = 0

    # Указатели на даты следующих событий
    next_payment_date = start_date
    next_profit_date = start_date + period_profit
    curr_date = start_date

    while curr_date <= end_date:

        # 1. Начисление процентов (Капитализация)
        daily_rate = (rate / 100) / (curr_date + relativedelta(years=1) - curr_date).days
        day_profit = current_balance * daily_rate
        accumulated_profit += day_profit
        profit_12_month += day_profit

        if curr_date == next_profit_date:
            current_balance += accumulated_profit
            total_income += accumulated_profit
            year_profit += accumulated_profit
            next_profit_date += period_profit
            accumulated_profit = 0.0

        # 2. Пополнение счета
        if curr_date == next_payment_date and curr_date < end_date:
            current_balance += payment
            total_deposit += payment
            next_payment_date += period_payment

        # 3. Начисление налогов
        is_tax_day = (curr_date.month == 12 and curr_date.day == 31 or curr_date == end_date)
        if is_tax_day and tax_enabled:
            tax = calculate_tax(year_profit)
            year_profit = 0.0
            # current_balance -= tax
            total_taxes += tax

        # 4. Наполнение данных
        graph_day = (curr_date == calendar_year_date or curr_date == end_date)
        if graph_day:
            count += 1
            graph_data[0].append(count)
            graph_data[1].append(round(current_balance - year_profit))
            graph_data[2].append(round(year_profit))
            calendar_year_date += relativedelta(years=1)

            start_balance = current_balance - payment * 12 - profit_12_month
            table_data += [
                [count, round(start_balance), round(payment * 12), round(profit_12_month), round(current_balance)]
            ]
            profit_12_month = 0

        curr_date += relativedelta(days=1)

    if tax_enabled:
        result["total_taxes"] = ratio.up(total_taxes)

    # 4. Учет инфляции (дисконтирование итогового капитала)
    if inf_enabled:
        years = (end_date - start_date).days / 365.25
        capital_inf = current_balance / ((1 + INF_RATE) ** years)
        result['capital_inf'] = ratio.up(int(capital_inf))
        result['inflation'] = ratio.up(int(current_balance - capital_inf))

    result.update({
        "current_balance": ratio.down(int(current_balance)),
        "deposit": ratio.down(int(total_deposit)),
        "income": ratio.down(int(total_income)),
        'graph_data': graph_data,
        'table_data': table_data,
    })

    return {**result, **kwargs}


def binary_find_param(low, high, sim_func, capital, **kwargs):
    for _ in range(25):
        mid = (low + high) / 2
        sim = sim_func(mid)
        if sim['current_balance'] < capital:
            low = mid
        else:
            high = mid

    return high


def calc_installment(**kwargs):
    ratio = kwargs.get('ratio')
    payment = binary_find_param(
        0, 10_000_000,
        lambda p: calculate_gains(payment=p, **kwargs),
        **kwargs
    )
    refined_payment = ratio.up(int(payment))
    res = calculate_gains(payment=refined_payment, **kwargs)
    return {**res, 'payment': refined_payment}


def calc_time_to_goal(**kwargs):
    start_date = kwargs.get('start_date')
    days = binary_find_param(
        0, 50 * 365,
        lambda d: calculate_gains(end_date=start_date + relativedelta(days=d), **kwargs),
        **kwargs
    )

    end_date = start_date + relativedelta(days=days)
    res = calculate_gains(end_date=end_date, **kwargs)

    return {
        **res,
        'end_date': end_date,
        'horizon': Period('horizon', relativedelta(end_date, start_date))
    }


def calc_percentage(**kwargs):
    rate = binary_find_param(0.0, 500.0, lambda r: calculate_gains(rate=r, **kwargs), **kwargs)
    rounded_rate = round(rate, 2)
    res = calculate_gains(rate=rounded_rate, **kwargs)
    return {**res, 'rate': rounded_rate}


def main_invest_calc(type_calc, **kwargs):
    print(f'main_invest_calc({type_calc=}, {kwargs=})')

    # Стратегии расчета
    strategies = {
        'gains_capital': lambda: calculate_gains(**kwargs),
        'installment': lambda: calc_installment(**kwargs),
        'time_to_goal': lambda: calc_time_to_goal(**kwargs),
        'percentage': lambda: calc_percentage(**kwargs)
    }

    res = strategies[type_calc]()

    return {
        'type_calc': type_calc,
        **kwargs,
        **res,
    }


def get_balance_portfolio(balance_capital, stocks, bonds, funds, metals, percent_stocks, percent_bonds,
                          percent_funds, percent_metals, partial_repl, pay_enabled, **kwargs):
    invested_sum = stocks + bonds + funds + metals
    internal_cash = balance_capital - invested_sum

    assets = {
        "stocks": {"curr": stocks, "target_p": percent_stocks},
        "bonds": {"curr": bonds, "target_p": percent_bonds},
        "funds": {"curr": funds, "target_p": percent_funds},
        "metals": {"curr": metals, "target_p": percent_metals}
    }

    if pay_enabled:
        # Режим только докупки: ищем капитал, при котором ни один актив не нужно продавать
        available_total = balance_capital + partial_repl
        required_totals = [data["curr"] / (data["target_p"] / 100)
                           for data in assets.values() if data["target_p"] > 0]

        ideal_total = max(required_totals) if required_totals else available_total
        target_total_capital = max(available_total, ideal_total)
        # Сколько еще нужно СВЕРХ partial_repl
        extra_needed = target_total_capital - available_total
    else:
        # Режим ребалансировки (продажа + покупка)
        target_total_capital = balance_capital + partial_repl
        extra_needed = 0

    actions = {}
    totals = {}
    for key, data in assets.items():
        target_val = target_total_capital * (data["target_p"] / 100)
        diff = round(target_val - data["curr"], 2)

        # Если разница меньше 1 рубля, считаем что баланс в норме (0)
        actions[f"action_{key}"] = diff if abs(diff) >= 100 else 0.0
        totals[f'total_{key}'] = round(target_val, 2)

    return {
        "balance_capital": balance_capital,
        'percent_stocks': percent_stocks,
        'percent_bonds': percent_bonds,
        'percent_funds': percent_funds,
        'percent_metals': percent_metals,
        "partial_repl": partial_repl,
        "extra_needed": round(extra_needed, 2),
        "target_total": round(target_total_capital, 2),
        'internal_cash': internal_cash,
        **actions, **totals, **kwargs
    }


def calculations(type_calc, **kwargs):
    if type_calc in ['gains_capital', 'time_to_goal', 'installment', 'percentage']:
        return main_invest_calc(type_calc=type_calc, **kwargs)
    elif type_calc == 'portfolio':
        return get_balance_portfolio(type_calc=type_calc, **kwargs)
