import PySimpleGUI as sg

from .params import *


def main_layout():
    return [[
        sg.Frame('Капитал', [[
            sg.Input('', key='capital', **cap_in)
        ]]),
        sg.Frame('Горизонт инвестирования', [[
                    sg.Input('', key='year'),
                    sg.Input('', key='month'),
                ]]),
        ], [
        sg.Frame('Регулярный платеж', [[
            sg.Input('', key='payment')
        ]]),
        sg.Frame('Годовая ставка', [[
            sg.Input('', key='rate'),
        ]]),
    ]]
