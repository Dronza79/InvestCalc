import calendar
from datetime import date

from dateutil.relativedelta import relativedelta

from .config import *
from .models import Period
from .utilites import div_to_ranks


def calculate_tax(year_profit):
    """Расчет прогрессивного налога."""
    if year_profit <= TAX_THRESHOLD:
        return round(year_profit * TAX_LOW)

    if year_profit > TAX_THRESHOLD:
        low_part = TAX_THRESHOLD
        high_part = year_profit - low_part
        return round((low_part * TAX_LOW) + (high_part * TAX_HIGH))


def calculate_gains(start_date, end_date, initial, payment, rate, period_payment,
                    period_profit, tax_enabled, inf_enabled, ratio, **kwargs):
    """
    Основной расчет капитала с учетом периодов капитализации, периодов платежей и периодов налогов.
    """
    # Определяем границы отчетных периодов (конец года для налогов и таблицы)
    def get_next_year_end(d):
        return date(d.year + 1, d.month, d.day)

    result = {}
    table_data = []
    graph_data = [initial, [0], [payment], [0]]

    current_balance = float(initial)
    total_deposit = 0.0
    total_income = 0.0
    total_taxes = 0.0

    # Годовые накопители для таблицы/налогов
    year_profit_for_tax = 0.0
    profit_12_month = 0.0
    payment_12_month = 0.0
    accumulated_profit = 0.0
    count = 0

    curr_date = start_date

    next_payment_date = start_date
    next_profit_date = start_date + period_profit
    next_report_date = get_next_year_end(curr_date)

    # Кэшируем функции
    calc_tax = calculate_tax

    while curr_date < end_date:
        # Ищем ближайшую дату, когда что-то произойдет
        next_event = min(next_payment_date, next_profit_date, next_report_date, end_date)
        days_in_period = (next_event - curr_date).days

        if days_in_period > 0:
            # Считаем проценты только за прошедшие дни до события
            # Учитываем реальное количество дней в текущем году для точности daily_rate
            year_days = 366 if calendar.isleap(curr_date.year) else 365
            daily_rate = (rate / 100) / year_days

            # ВАЖНО: Если начисление (капитализация) не ежедневно,
            # то внутри периода проценты НЕ увеличивают базу. Это простой процент,
            # который станет сложным только в next_profit_date.
            period_profit_val = current_balance * daily_rate * days_in_period

            # Накапливаем в "буфер" капитализации
            accumulated_profit += period_profit_val
            profit_12_month += period_profit_val

        curr_date = next_event

        # 1. Событие: Капитализация (период начисления процентов)
        if curr_date == next_profit_date:
            current_balance += accumulated_profit
            total_income += accumulated_profit
            year_profit_for_tax += accumulated_profit
            accumulated_profit = 0.0
            next_profit_date += period_profit

        # 3. Событие: Конец года (Налоги и отчетность)
        if curr_date == next_report_date or curr_date == end_date:
            if tax_enabled:
                tax = calc_tax(year_profit_for_tax)
                total_taxes += tax
                year_profit_for_tax = 0.0

            # Здесь логика формирования table_data (раз в год)
            count += 1
            graph_data[1].append(count)
            graph_data[2].append(round(total_deposit))
            graph_data[3].append(round(current_balance - total_deposit - initial))

            start_balance = current_balance - payment_12_month - profit_12_month
            table_data += [
                [
                    count,
                    # f'{curr_date:%d.%m.%y}',
                    f'{div_to_ranks(round(start_balance))}\u20BD',
                    f'{div_to_ranks(round(payment_12_month))}\u20BD',
                    f'{div_to_ranks(round(profit_12_month))}\u20BD',
                    f'{div_to_ranks(calculate_tax(profit_12_month))}\u20BD' if tax_enabled else '--',
                    f'{div_to_ranks(round(current_balance))}\u20BD'
                ]
            ]
            profit_12_month = 0
            payment_12_month = 0

            next_report_date = get_next_year_end(curr_date)

        # 2. Событие: Пополнение
        if curr_date == next_payment_date and curr_date < end_date:
            current_balance += payment
            total_deposit += payment
            payment_12_month += payment
            next_payment_date += period_payment

    # Финальные расчеты инфляции (без изменений)
    if inf_enabled:
        years = (end_date - start_date).days / 365.25
        capital_inf = current_balance / ((1 + INF_RATE) ** years)
        payment_inf = payment * ((1 + INF_RATE) ** years)
        result['capital_inf'] = ratio.up(int(capital_inf))
        result['payment_inf'] = ratio.up(int(payment_inf))
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
    payment = kwargs.pop('payment', 0)
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

    internal_cash = target_total_capital - sum(totals.values())

    return {
        "balance_capital": balance_capital,
        'percent_stocks': percent_stocks,
        'percent_bonds': percent_bonds,
        'percent_funds': percent_funds,
        'percent_metals': percent_metals,
        "partial_repl": partial_repl,
        "extra_needed": round(extra_needed, 2),
        "target_total": round(target_total_capital, 2),
        'internal_cash': round(internal_cash, 2),
        **actions, **totals, **kwargs
    }


def calculations(type_calc, **kwargs):
    if type_calc == 'portfolio':
        return get_balance_portfolio(type_calc=type_calc, **kwargs)
    return main_invest_calc(type_calc=type_calc, **kwargs)
