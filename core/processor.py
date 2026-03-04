import datetime
import re
from datetime import datetime as dd

import matplotlib.pyplot as plt
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
"""
valid_data={
    'period_payment': 12, 
    'period_profit': 365, 
    'rate': 11.5, 
    'ratio': 500, 
    'type_calc': 'gains_capital', 
    'ndfl': True, 
    'inf': True, 
    'capital': 750000, 
    'payment': 15000, 
    'initial': 50000, 
    'horizon': relativedelta(years=+15, months=+6, days=+17), 
    'start_date': datetime.date(2026, 3, 4), 
    'end_date': datetime.date(2041, 9, 21)
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


def calculate_wealth_advanced(
        start_date: datetime.date,
        end_date: datetime.date = None,
        horizon: relativedelta = None,
        initial_capital: float = 0.0,
        contribution_amount: float = 0.0,
        contributions_per_year: int = 12,
        yield_rate: float = 0.15,
        compounding_per_year: int = 365,  # По умолчанию ежедневно
        inflation_rate: float = 0.08,
        apply_tax: bool = True
):
    # Определение конечной даты
    if end_date is None and horizon is not None:
        end_date = start_date + horizon
    elif end_date is None:
        raise ValueError("Необходимо указать либо end_date, либо horizon")

    total_days = (end_date - start_date).days
    current_capital = initial_capital
    daily_yield = yield_rate / 365

    # Параметры для учета платежей
    contribution_days = [start_date + relativedelta(months=i * (12 // contributions_per_year))
                         for i in range(1, (total_days // 30) + 2)]

    annual_profit = 0
    current_date = start_date

    for day in range(1, total_days + 1):
        # 1. Начисление процентов (ежедневно или по заданному графику)
        # Если compounding_per_year = 365, начисляем каждый день
        profit_today = current_capital * daily_yield
        current_capital += profit_today
        annual_profit += profit_today

        current_date += datetime.timedelta(days=1)

        # 2. Регулярный платеж
        if any(d == current_date for d in contribution_days):
            current_capital += contribution_amount

        # 3. Налоги (списываются в конце каждого календарного года или в конце срока)
        if (current_date.month == 12 and current_date.day == 31) or current_date == end_date:
            if apply_tax and annual_profit > 0:
                # Прогрессивная шкала 2025: 13% до 2.4 млн, 15% свыше
                if annual_profit <= 2400000:
                    tax = annual_profit * 0.13
                else:
                    tax = (2400000 * 0.13) + (annual_profit - 2400000) * 0.15
                current_capital -= tax
            annual_profit = 0  # Сброс счетчика прибыли на новый год

    # 4. Учет инфляции (приведение к сегодняшним ценам)
    years_passed = total_days / 365.25
    real_wealth = current_capital / ((1 + inflation_rate) ** years_passed)

    return {
        "nominal_wealth": round(current_capital, 2),
        "real_wealth": round(real_wealth, 2),
        "period_years": round(years_passed, 1)
    }


# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ ---
start = datetime.date(2024, 1, 1)
period = relativedelta(years=10, months=6)

result = calculate_wealth_advanced(
    start_date=start,
    horizon=period,
    initial_capital=1000000,
    contribution_amount=50000,
    contributions_per_year=12,  # Ежемесячно
    yield_rate=0.20,  # 20% годовых
    inflation_rate=0.08  # 8% инфляция
)

print(f"Номинальный капитал: {result['nominal_wealth']:,} руб.")
print(f"Реальная покупательная способность: {result['real_wealth']:,} руб.")


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
