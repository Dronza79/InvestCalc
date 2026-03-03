import PySimpleGUI as sg

from core.utilites import format_digit_years, div_to_ranks, format_years_genitive
from .models import Period
from .params import *


def capital_input():
    return sg.Frame('Желанный капитал:', [
                [
                    sg.Input('1', key='capital', **cap_in),
                    sg.T('\u20BD', font='_ 20'),
                ]
            ], **main_frame)


def start_amount_input():
    return sg.Frame('Начальная сумма:', [
                [
                    sg.Input('1', key='initial', s=10, **other_in),
                    sg.T('\u20BD'),
                ]
            ], **main_frame)


def regular_payment_input():
    return sg.Frame('Регулярный платеж:', [
                [
                    sg.Input('1', key='payment', s=10, **other_in),
                    sg.T('\u20BD'),
                ]
            ], **main_frame)


def invest_horizon_input():
    return sg.Frame('Инвест горизонт:', [
                [
                    sg.Input('', key='horizon', s=10, **other_in)
                ]
            ], **main_frame)


def plane_profit_input():
    return sg.Frame('Плановая доходность:', [
        [
            sg.Input('', key='rate', s=8, **other_in),
            sg.Text('%'),
        ]
    ], **main_frame)


def additional_param():
    return sg.Frame('Доп параметры:', [
                [
                    sg.Checkbox('НДФЛ', key='ndfl', **chbx),
                    sg.Checkbox('Инфляция', key='inf', **chbx),
                    sg.Frame('Кратность:', [[
                        sg.Combo(['100', '500', '1000'], default_value=500, k='ratio', **combo_per)
                    ]])
                ]
            ],  **main_frame)


def periodicity_combo(key):
    list_period = Period.glp()
    return sg.Frame('Периодичность:', [
                [
                    sg.Combo(list_period, default_value=list_period[1], key=key,  **combo_per),
                ]
            ],  **main_frame)


def invest_header_output(period_payment, payment='0', horizon='0', **kwargs):
    # print(f'{kwargs=}')
    param = {'font': 'Courier 20', 'pad': (5, 0)}
    if not horizon: horizon = 0
    return sg.Col([
        [
            sg.Text('Откладывая по', **param),
            sg.Text(div_to_ranks(payment), **param),
            sg.T('\u20BD', **param),
            sg.T(period_payment, **param)
        ], [
           sg.T('на протяжении', **param),
           sg.T(f'{format_years_genitive(horizon)},', **param),
           sg.T('вы накопите:', **param)
        ]
    ], expand_x=True, element_justification='c', pad=20)


def invest_leader_output(capital: str, **kwargs):
    # print(f'{kwargs=}')
    param = {'font': 'Courier 50 bold', 'pad': (5, 0)} # 'background_color': 'red'}
    if not capital: capital = 0
    return sg.Col([
        [
            sg.Text(div_to_ranks(capital), **param),
            sg.T('\u20BD', **param),
        ]
    ], expand_x=True, element_justification='c', pad=10) #, background_color='blue')


def invest_liner_output(key, **kwargs):
    param = {'font': 'Courier 18', 'pad': (5, 0)} # 'background_color': 'red'}
    ADD = {
        'start': ('initial', 'Начальная сумма:'),
        'contrib': ('deposit', 'Сумма пополнений:'),
        'received': ('income', 'Ожидаемый доход:'),
        'paid': ('taxes', 'Уплачено налогов:'),

    }
    return sg.Col([
        [
            sg.Text(f'{ADD[key][1]:.<40}', **param),
            # sg.Push(),
            sg.Text(div_to_ranks(kwargs[ADD[key][0]]), **param),
            sg.T('\u20BD', **param),
        ]
    ], expand_x=True, element_justification='l', pad=10) #, background_color='blue')
