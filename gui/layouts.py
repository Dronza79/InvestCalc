import PySimpleGUI as sg

from .params import *


def layout_param_capital():
    return [
        [
            sg.Frame('Капитал', [
                [
                    sg.Input('', key='capital', **cap_in),
                    sg.T('\u20BD'),
                ]
            ], **main_frame),
        ], [
            sg.Frame('Инвест горизонт', [
                [
                    sg.Input('', key='horizon', **other_in)
                ]
            ], **main_frame),
        ], [
            sg.Frame('Регулярный платеж', [
                [
                    sg.Input('', key='payment', **other_in),
                    sg.T('\u20BD'),
                ]
            ], **main_frame),
        ], [
            sg.Frame('Годовая ставка', [
                [
                    sg.Input('', key='rate', **other_in)
                ]
            ], **main_frame)
        ]
    ]


def left_part():
    return sg.Col([
        [sg.TabGroup([[
            sg.Tab('Капитал', layout_param_capital()),
            sg.Tab('Платежи', [[]], expand_x=True),
            sg.Tab('Горизонт', [[]], expand_x=True),
        ]], **lft_tabgroup)],
        [sg.Button('РАССЧИТАТЬ', key='-GO-', **main_btn)]
    ], **lft_col)


def right_part():
    return sg.Col([
        [sg.TabGroup([[]], **rht_tabgroup)],
    ], **rht_col)


def main_layout():
    return [left_part(), sg.VSep(), right_part()]
