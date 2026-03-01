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


