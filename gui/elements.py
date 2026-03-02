import PySimpleGUI as sg

from core.utilites import format_digit_years, div_to_ranks, format_years_genitive
from .models import Period
from .params import *


def capital():
    return sg.Frame('Желанный капитал:', [
                [
                    sg.Input('', key='capital', **cap_in),
                    sg.T('\u20BD', font='_ 20'),
                ]
            ], **main_frame)


def start_amount():
    return sg.Frame('Начальная сумма:', [
                [
                    sg.Input('', key='start', s=10, **other_in),
                    sg.T('\u20BD'),
                ]
            ], **main_frame)


def regular_payment():
    return sg.Frame('Регулярный платеж:', [
                [
                    sg.Input('', key='payment', s=10, **other_in),
                    sg.T('\u20BD'),
                ]
            ], **main_frame)


def invest_horizon():
    return sg.Frame('Инвест горизонт:', [
                [
                    sg.Input('', key='horizon', s=10, **other_in)
                ]
            ], **main_frame)


def plane_profit():
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


def periodicity(key):
    list_period = Period.glp()
    return sg.Frame('Периодичность:', [
                [
                    sg.Combo(list_period, default_value=list_period[1], key=key,  **combo_per),
                ]
            ],  **main_frame)


def expl_title(period_payment, payment='0', horizon='0', **kwargs):
    print(f'{kwargs=}')
    param = {'font': '_ 20', 'pad': (5, 0)}
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
    ], expand_x=True, element_justification='l', pad=20)
