import datetime
import re

from dateutil.relativedelta import relativedelta


def get_month_payment():
    max_capital = int(input('Введите желаемый капитал: ').replace(' ', ''))
    annual_rate = float(input('Планируемую годовую ставку в процентах: '))
    rate = annual_rate / 1200
    horizon = re.findall(r'\d+', input('Введите срок в годах: '))
    per = int(horizon[0]) * 12 + int(12 / 10 * (int(horizon[-1]) if len(horizon) != 1 else 0))
    ratio = int(input('Укажите кратность значения: '))
    pmt = int((max_capital * rate / ((1 + rate) ** per - 1) + ratio - 1) // ratio * ratio)
    return {
        'payment': pmt,
        'month': per,
        'capital': max_capital,
        'annual_rate': annual_rate,
    }


# def calculate_horizon_custom(target_fv, period_payment, annual_rate,
#                              period_delta, inflation=0.08, tax=0.13):
#     """
#     target_fv: желаемый капитал
#     period_payment: сумма пополнения за один период (раз в день/неделю/месяц)
#     annual_rate: номинальная годовая ставка (0.15 = 15%)
#     period_delta: объект relativedelta, определяющий частоту (например, months=1)
#     """
#
#     # 1. Определяем количество периодов в году (periods_per_year)
#     # Используем средние значения: год = 365.25 дней, месяц = 30.43 дней
#     total_days = (period_delta.years * 365.25 +
#                   period_delta.months * 30.4375 +
#                   period_delta.days +
#                   period_delta.weeks * 7)
#
#     if total_days <= 0:
#         return "Ошибка: период не может быть нулевым"
#
#     periods_per_year = 365.25 / total_days
#
#     # 2. Считаем реальную годовую ставку (после налогов и инфляции)
#     rate_after_tax = annual_rate * (1 - tax)
#     # Формула Фишера для реальной доходности
#     real_annual_rate = (1 + rate_after_tax) / (1 + inflation) - 1
#
#     # 3. Приводим годовую ставку к ставке за период (сложный процент)
#     # r_period = (1 + R_annual)^(1/n) - 1
#     r = (1 + real_annual_rate) ** (1 / periods_per_year) - 1
#
#     # 4. Расчет количества периодов (n)
#     try:
#         # n = ln((FV * r / PMT) + 1) / ln(1 + r)
#         n_periods = math.log((target_fv * r / period_payment) + 1) / math.log(1 + r)
#
#         # Переводим общее кол-во периодов в годы для удобства
#         total_years = n_periods / periods_per_year
#         return round(total_years, 2)
#
#     except (ValueError, ZeroDivisionError):
#         return "Цель недостижима (доходность ниже инфляции или слишком малый платеж)"


def get_gans_capital(
        start_date, end_date, initial, payment, period_payment,
        tax_enabled, inf_enabled, ratio, rate, period_profit,
        horizon: relativedelta, **kwargs
):
    payment_step = period_payment.duration
    profit_step = period_profit.duration
    current_capital = initial
    daily_rate_simple = rate / 100 / 365

    payment_date = start_date + payment_step
    profit_date = start_date + profit_step

    profit_days = (profit_date - start_date).days

    total_invested = initial
    total_interest_earned = 0
    total_taxes_paid = 0
    annual_profit_for_tax = 0

    years_list = [0]
    invested_list = [initial]
    interest_list = [0.0]
    payment_registry = []
    payment_counter = 0
    current_date = start_date

    while current_date <= end_date:

        # Начисление процентов
        if current_date == profit_date or current_date == end_date:
            current_past_rate = (
                daily_rate_simple * profit_days if current_date != end_date else
                (end_date - (profit_date - profit_step)).days * daily_rate_simple
            )
            profit = current_capital * current_past_rate
            current_capital += profit
            total_interest_earned += profit
            annual_profit_for_tax += profit
            profit_date += profit_step

        # Пополнение капитала
        if current_date == payment_date:
            current_capital += payment
            payment_date += payment_step
            payment_counter += 1
            total_invested += payment
            payment_registry.append([
                payment_counter, current_date, round(total_invested, 2),
                round(total_interest_earned, 2), round(current_capital, 2)
            ])

        # 4. Налоги и годовая статистика
        is_tax_day = (current_date.month == 12 and current_date.day == 31)
        if is_tax_day and tax_enabled:
            if annual_profit_for_tax <= 2.4e6:
                tax = annual_profit_for_tax * 0.13
            else:
                tax = (2.4e6 * 0.13) + (annual_profit_for_tax - 2.4e6) * 0.15
            current_capital -= tax
            total_taxes_paid += tax
            annual_profit_for_tax = 0

        if is_tax_day or current_date == end_date:
            x_diff = relativedelta(current_date, start_date).years
            if x_diff > 0 and x_diff not in years_list:
                years_list.append(x_diff)
                invested_list.append(round(total_invested, 2))
                interest_list.append(round(total_interest_earned, 2))

        current_date += datetime.timedelta(days=1)

    # Инфляция
    exact_years = horizon.years + (horizon.months / 12.0) + (horizon.days / 365.25)
    real_wealth = current_capital / (1.08 ** exact_years) if inf_enabled else current_capital
    inflation = current_capital - real_wealth

    result = {
        "capital_gans": round((current_capital // ratio) * ratio, 2),  # Итоговый капитал
        "capital_inflat": round((real_wealth // ratio) * ratio, 2),  # Капитал с инфляцией
        "inflation": round((inflation // ratio) * ratio, 2),  # Инфляцией
        "total_taxes": round(total_taxes_paid, 2),  # Итого налоги
        "income": round(total_interest_earned, 2),  # Доход сложного процента
        "deposit": round(total_invested - initial, 2),  # Инвестировано
        "graph_data": [years_list, invested_list, interest_list],  # Данные для Графика
        "table_data": payment_registry,  # Данные для Таблицы
        'start_date': start_date,
        'end_date': end_date,
        'horizon': horizon,
        'payment': payment,
        'period_payment': period_payment,
        'initial': initial,
        'tax_enabled': tax_enabled,
        'inf_enabled': inf_enabled,
    }

    return {**result, **kwargs}


def get_balance_portfolio(
        balance_capital, stocks, bonds, funds, metals,
        percent_stocks, percent_bonds, percent_funds,
        percent_metals, partial_repl, pay_enabled,
        **kwargs
):
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
        actions[f"action_{key}"] = diff if abs(diff) >= 1.0 else 0.0
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
    if type_calc == 'gains_capital':
        return get_gans_capital(**kwargs)
    elif type_calc == 'portfolio':
        return get_balance_portfolio(type_calc=type_calc, **kwargs)
