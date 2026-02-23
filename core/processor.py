import datetime
import re
from datetime import datetime as dd

import matplotlib.pyplot as plt


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


def get_value_graph(payment, month, annual_rate, capital):
    rate = annual_rate / 1200
    for i in range(1, month + 1):
        yield {
            'month': i,
            'all_payment': payment * i,
            'sum_capital': int(payment * (((1 + rate) ** i - 1) / rate)),
            'capital': capital
        }


def main():
    data = get_month_payment()
    months = list()
    payments = list()
    capital = list()
    for val in get_value_graph(**data):
        months.append(val['month'])
        payments.append(val['all_payment'])
        capital.append(val['sum_capital'])

    # print(months)
    # print(payments)
    # print(capital)

    plt.plot(months, payments, label="Платежи", color="blue")
    plt.plot(months, capital, label="Сложный процент", color="red")

    plt.legend()  # Добавляет легенду, чтобы различать линии
    plt.flag()
    plt.show()

