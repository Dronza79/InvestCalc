import PySimpleGUI as sg

from gui.models import Period
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
                ]
            ],  **main_frame)


def periodicity():
    list_period = Period.glp()
    return sg.Frame('Периодичность:', [
                [
                    sg.Combo(list_period, default_value=list_period[1], key='period',  **combo_per),
                ]
            ],  **main_frame)


def layout_left_invest():
    return [
        [
            capital(),
        ], [
            regular_payment(),
            periodicity(),
        ], [
            start_amount(),
            invest_horizon(),
        ], [
            plane_profit(),
            periodicity(),
        ], [
            additional_param(),
        ], [
        ]
    ]


def left_part():
    return sg.Col([
        [
            sg.TabGroup([[
                sg.Tab('Инвестиции', layout_left_invest()),
                sg.Tab('Облигации', [[]], expand_x=True),
                sg.Tab('Что-то', [[]], expand_x=True, disabled=True),
            ]], **lft_tabgroup)
        ], [
            sg.Button('РАССЧИТАТЬ', key='-GO-', **main_btn),
        ]
    ], **lft_col)


def explanations():
    return [[
        sg.Text(key='explan', **expl_t)
    ]]


def right_part():
    return sg.Col([
        [sg.TabGroup([[
            sg.Tab('Пояснения', explanations(), **rht_tab),
            sg.Tab('График', [[]], **rht_tab),
            sg.Tab('Таблица', [[]], **rht_tab),
        ]], **rht_tabgroup)],
    ], **rht_col)


def main_layout():
    return [left_part(), sg.VSep(), right_part()]
