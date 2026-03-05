import datetime
import math
import re
from datetime import datetime as dd

import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

from core.utilites import check_for_day_week


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


"""
valid_data={
    'payment_step': relativedelta(months=+1), 
    'profit_step': relativedelta(days=+1), 
    'rate': 12.5, 
    'ratio': 500, 
    'ndfl': True, 
    'inf': True, 
    'capital': 750000, 
    'payment': 15000, 
    'initial': 56000, 
    'horizon': relativedelta(years=+5, months=+6), 
    'start_date': datetime.date(2026, 3, 5), 
    'end_date': datetime.date(2031, 9, 5)
}
"""


# def get_gans_capital(
#         payment, initial, period_payment,
#         period_profit, rate, ndfl, inf,
#         horizon: relativedelta, **kwargs
# ):
#     initial = initial if initial else 0
#     periodic_rate = rate / (period_profit * 100)
#     amount_days = int(round(horizon.years * 365 + horizon.months * 30.44 + horizon.days, 0))
#     amount_payment = amount_days / 365 * period_payment
#     gans_capital = initial
#     for _ in range(1, int(amount_payment + 1)):
#         for _ in range()


def get_gans_capital(
        start_date, end_date, initial, payment, payment_step,
        profit_step, tax_enabled, inf_enabled, ratio, rate,
        horizon: relativedelta, **kwargs
):

    current_capital = total_invested = initial
    rate = rate / 100

    next_payment_date = check_for_day_week(start_date + payment_step)
    next_profit_date = check_for_day_week(start_date + profit_step)

    # Статистика
    total_interest_earned = 0
    total_taxes_paid = 0

    # Данные для графиков (годовые срезы)
    years_list = [0]
    invested_list = [0]
    interest_list = [0]
    data_table_list = []

    current_date = start_date
    annual_profit_for_tax = 0
    last_profit_calc_date = start_date
    year_counter = 0

    while current_date < end_date:
        # 1. Начисление процентов
        if current_date == next_profit_date:
            days_in_period = (next_profit_date - last_profit_calc_date).days
            profit = current_capital * (rate * days_in_period / 365)

            current_capital += profit
            total_interest_earned += profit
            annual_profit_for_tax += profit

            last_profit_calc_date = next_profit_date
            next_profit_date = check_for_day_week(next_profit_date + profit_step)

        # 2. Регулярный платеж
        if current_date == next_payment_date:
            current_capital += payment
            total_invested += payment
            next_payment_date = check_for_day_week(next_payment_date + payment_step)

        # 3. Налоги (31 декабря) и сбор ежегодной статистики
        if (current_date.month == 12 and current_date.day == 31) or current_date == end_date:
            # Расчет НДФЛ
            if tax_enabled and annual_profit_for_tax > 0:
                if annual_profit_for_tax <= 2400000:
                    tax = annual_profit_for_tax * 0.13
                else:
                    tax = (2400000 * 0.13) + (annual_profit_for_tax - 2400000) * 0.15
                current_capital -= tax
                total_taxes_paid += tax

            annual_profit_for_tax = 0
            year_counter += 1

            # Запись данных для графика
            years_list.append(year_counter)
            invested_list.append(total_invested)
            interest_list.append(round(total_interest_earned, 2))

        current_date += relativedelta(days=1)

    # Итоговые расчеты
    total_years = (end_date - start_date).days / 365.25
    inf_rate = 0.08 if inf_enabled else 0.0
    real_wealth = current_capital / ((1 + inf_rate) ** total_years)

    return {
        "capital_nominal": (current_capital // ratio) * ratio,      # Итоговый капитал
        "capital_real": (real_wealth // ratio) * ratio,             # Капитал с учетом инфляции
        "total_taxes": round(total_taxes_paid, 2),                  # Итоговые налоги
        "total_income": round(total_interest_earned, 2),            # Итоговый доход
        "total_invested": total_invested,                           # Внесено средств
        "graph_data": [years_list, invested_list, interest_list]    # Данные для графика и таблицы
    }

    # Настройки
    # params = {
    #     'period_payment': relativedelta(months=1),
    #     'period_profit': relativedelta(days=1),
    #     'rate': 11.5,
    #     'ratio': 500,
    #     'ndfl': True,
    #     'inf': True,
    #     'payment': 15000,
    #     'initial': 50000,
    #     'start_date': datetime.date(2026, 3, 4),
    #     'end_date': datetime.date(2041, 9, 21)
    # }

    # res = calculate_investment_full_stats(params)
    #
    # print(f"Полученный капитал: {res['capital_nominal']:,}")
    # print(f"С учетом инфляции: {res['capital_real']:,}")
    # print(f"Уплачено налогов: {res['total_taxes']:,}")
    # print(f"Доход от процентов: {res['total_interest']:,}")
    # print(f"Внесено средств: {res['total_invested']:,}")
    # print(f"Данные для графика: {res['chart_data']}")
    #


def get_value_graph(payment, month, annual_rate, capital):
    rate = annual_rate / 1200
    for i in range(1, month + 1):
        yield {
            'month': i,
            'all_payment': payment * i,
            'sum_capital': int(payment * (((1 + rate) ** i - 1) / rate)),
            'capital': capital
        }


# def calculations(type_calc, capital, **kwargs):
#     if type_calc == 'gains_capital':
#         return get_gans_capital(**kwargs)


# import datetime
# from dateutil.relativedelta import relativedelta
#
#
# def calculate_investment_ultimate(params):
#     start_date = params['start_date']
#     end_date = params['end_date']
#     current_capital = params['initial']
#     payment = params['payment']
#     rate = params['rate'] / 100
#     ratio = params['ratio']
#
#     # Вспомогательная функция переноса на будний день
#     def adjust_to_weekday(d):
#         if d.weekday() == 5: return d + datetime.timedelta(days=2)  # Сб -> Пн
#         if d.weekday() == 6: return d + datetime.timedelta(days=1)  # Вс -> Пн
#         return d
#
#     # Инициализация дат событий
#     next_payment_date = adjust_to_weekday(start_date + params['period_payment'])
#     next_profit_date = adjust_to_weekday(start_date + params['period_profit'])
#
#     # Счётчики
#     total_invested = params['initial']
#     total_interest_earned = 0
#     total_taxes_paid = 0
#     annual_profit_for_tax = 0
#     last_profit_calc_date = start_date
#
#     # Списки для графиков (по годам)
#     years_list, invested_list, interest_list = [0], [params['initial']], [0.0]
#
#     # Реестр платежей (список списков)
#     payment_registry = []
#     payment_counter = 0
#
#     current_date = start_date
#     while current_date < end_date:
#         # 1. Начисление процентов
#         if current_date == next_profit_date:
#             days_in_period = (next_profit_date - last_profit_calc_date).days
#             profit = current_capital * (rate * days_in_period / 365)
#
#             current_capital += profit
#             total_interest_earned += profit
#             annual_profit_for_tax += profit
#
#             last_profit_calc_date = next_profit_date
#             next_profit_date = adjust_to_weekday(next_profit_date + params['period_profit'])
#
#         # 2. Регулярный платеж + запись в реестр
#         if current_date == next_payment_date:
#             payment_counter += 1
#             current_capital += payment
#             total_invested += payment
#
#             # Запись: [№, Дата, Сумма вложений, Доход на текущий момент, Весь капитал]
#             payment_registry.append([
#                 payment_counter,
#                 current_date,
#                 round(total_invested, 2),
#                 round(total_interest_earned, 2),
#                 round(current_capital, 2)
#             ])
#
#             next_payment_date = adjust_to_weekday(next_payment_date + params['period_payment'])
#
#         # 3. Налоги и годовая статистика (31 декабря)
#         if (current_date.month == 12 and current_date.day == 31) or current_date == end_date:
#             if params['ndfl'] and annual_profit_for_tax > 0:
#                 if annual_profit_for_tax <= 2400000:
#                     tax = annual_profit_for_tax * 0.13
#                 else:
#                     tax = (2400000 * 0.13) + (annual_profit_for_tax - 2400000) * 0.15
#                 current_capital -= tax
#                 total_taxes_paid += tax
#
#             annual_profit_for_tax = 0
#
#             # Данные для графика
#             years_passed = (current_date - start_date).days // 365
#             if years_passed not in years_list:
#                 years_list.append(years_passed)
#                 invested_list.append(round(total_invested, 2))
#                 interest_list.append(round(total_interest_earned, 2))
#
#         current_date += datetime.timedelta(days=1)
#
#     # Итоговые расчеты
#     total_years = (end_date - start_date).days / 365.25
#     inf_rate = 0.08 if params['inf'] else 0.0
#     real_wealth = current_capital / ((1 + inf_rate) ** total_years)
#
#     return {
#         "final_capital": (current_capital // ratio) * ratio,
#         "real_capital": (real_wealth // ratio) * ratio,
#         "total_taxes": round(total_taxes_paid, 2),
#         "total_interest": round(total_interest_earned, 2),
#         "total_invested": total_invested,
#         "chart_data": [years_list, invested_list, interest_list],
#         "payment_registry": payment_registry
#     }
#
#
# # --- Параметры из запроса ---
# params = {
#     'period_payment': relativedelta(months=1),
#     'period_profit': relativedelta(days=1),
#     'rate': 11.5,
#     'ratio': 500,
#     'ndfl': True,
#     'inf': True,
#     'payment': 15000,
#     'initial': 50000,
#     'start_date': datetime.date(2026, 3, 4),
#     'end_date': datetime.date(2041, 9, 21)
# }
#
# res = calculate_investment_ultimate(params)
#
# # Вывод результатов
# print(f"Капитал: {res['final_capital']:,} | Реальный: {res['real_capital']:,}")
# print(f"Налоги: {res['total_taxes']:,} | Проценты: {res['total_interest']:,}")
# print("-" * 30)
# print("Первые 3 записи реестра платежей:")
# for row in res['payment_registry'][:3]:
#     print(row)
