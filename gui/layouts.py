import PySimpleGUI as sg

from .params import *


def main_layout():
    return [[sg.Col([[
        sg.Frame('Капитал', [[
            sg.Input('', key='capital', **cap_in),
            sg.T('\u20BD'),
        ]], **main_frame),
        sg.Frame('Инвест горизонт', [[
                    sg.Input('', key='horizon', **other_in),
                ]], **main_frame),
        ], [
        sg.Frame('Регулярный платеж', [[
            sg.Input('', key='payment', **other_in),
            sg.T('\u20BD'),
        ]], **main_frame),
        sg.Frame('Годовая ставка', [[
            sg.Input('', key='rate', **other_in),
        ]], **main_frame)
        ], [sg.VPush()], [
            sg.Push(),
            sg.Button('Расчитать', key="-GO-"),
            sg.Push(),
        ]], element_justification='c', vertical_alignment='t', background_color='blue'),
        sg.Col([[
            sg.Multiline(default_text='', expand_x=True, expand_y=True, background_color='yellow', disabled=True)
        ]], key='body', background_color='red', visible=False, expand_x=True, expand_y=True)
    ]]
