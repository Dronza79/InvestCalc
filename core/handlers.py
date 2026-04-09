from dateutil.relativedelta import relativedelta

from core.config import *
from gui.models import Period


def calculate_tax(profit_raw: float, year_profit: float) -> float:
    """Расчет прогрессивного налога."""
    if year_profit >= TAX_THRESHOLD:
        return profit_raw * TAX_HIGH

    if year_profit + profit_raw > TAX_THRESHOLD:
        low_part = TAX_THRESHOLD - year_profit
        high_part = profit_raw - low_part
        return (low_part * TAX_LOW) + (high_part * TAX_HIGH)

    return profit_raw * TAX_LOW


def calculate_gains(start_date, end_date, initial, payment, rate, period_payment,
                    period_profit, tax_enabled, inf_enabled, ratio, **kwargs):
    """
    Основной движок с логикой капитализации и налогов.
    """
    result = {}
    current_balance = float(initial)
    total_deposit = float(initial)
    total_income = 0.0
    total_taxes = 0.0

    year_profit = 0.0
    current_year = start_date.year

    # Указатели на даты следующих событий
    next_payment_date = start_date + period_payment
    next_profit_date = start_date + period_profit
    curr_date = start_date

    # Эффективная ставка за один период начисления
    # Используем метод класса Period для определения частоты в году
    rate_per_period = (rate / 100) / period_profit.times_per_year()

    while curr_date < end_date:
        curr_date = min(next_payment_date, next_profit_date, end_date)

        if curr_date > end_date:
            break

        # 1. Начисление процентов (Капитализация)
        if curr_date == next_profit_date:
            profit_raw = current_balance * rate_per_period

            if tax_enabled:
                if curr_date.year != current_year:
                    year_profit = 0.0
                    current_year = curr_date.year

                tax = calculate_tax(profit_raw, year_profit)
                profit_after_tax = profit_raw - tax
                total_taxes += tax
                year_profit += profit_raw
            else:
                profit_after_tax = profit_raw

            # КАПИТАЛИЗАЦИЯ: прибавляем доход к телу баланса
            current_balance += profit_after_tax
            total_income += profit_after_tax
            next_profit_date += period_profit

        # 2. Пополнение счета
        if curr_date == next_payment_date:
            current_balance += payment
            total_deposit += payment
            next_payment_date += period_payment

    # 3. Учет инфляции (дисконтирование итогового капитала)
    if inf_enabled:
        years = (end_date - start_date).days / 365.25
        capital_inf = current_balance / ((1 + INF_RATE) ** years)
        result['capital_inf'] = capital_inf
        result['inflation'] = current_balance - capital_inf

    result.update({
        "current_balance": ratio.down(current_balance),
        "deposit": ratio.down(total_deposit),
        "income": ratio.down(total_income),
        "total_taxes": ratio.up(total_taxes),

    })

    return {**result, **kwargs}


def main_invest_calc(type_calc, **kwargs):
    print(f'main_invest_calc({type_calc=}, {kwargs=})')

    capital = kwargs.get('capital')
    start_date = kwargs.get('start_date')
    ratio = kwargs.get('ratio')

    res = {}

    if type_calc == 'gains_capital':
        res = calculate_gains(**kwargs)

    elif type_calc == 'installment':
        low, high = 0, 10_000_000

        for _ in range(25):
            mid = (low + high) / 2
            sim = calculate_gains(payment=mid, **kwargs)

            if sim['current_balance'] < capital:
                low = mid
            else:
                high = mid

        res = calculate_gains(payment=ratio.up(high), **kwargs)
        res['payment'] = ratio.up(high)

    elif type_calc == 'time_to_goal':
        low, high = 0, 50 * 365

        for _ in range(25):
            mid = (low + high) // 2
            temp_end = start_date + relativedelta(days=mid)
            sim = calculate_gains(end_date=temp_end, **kwargs)

            if sim['current_balance'] < capital:
                low = mid
            else:
                high = mid

        end_date = start_date + relativedelta(days=high)
        res = calculate_gains(end_date=end_date, **kwargs)

        res['horizon'] = Period('horizon', relativedelta(end_date, start_date))
        res['end_date'] = end_date

    elif type_calc == 'percentage':
        low, high = 0.0, 500.0

        for _ in range(25):
            mid = (low + high) / 2
            sim = calculate_gains(rate=mid, **kwargs)

            if sim['current_balance'] < capital:
                low = mid
            else:
                high = mid

        res = calculate_gains(rate=round(high, 2), **kwargs)
        print(f'rate={high} {res=}')
        res['rate'] = round(high, 2)

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
