from .layouts import *

pa = {'expand_x': True, 'expand_y': True}


def main_window():
    return sg.Window('Инвест калькулятор', main_layout(), **main_win_param)
    # return sg.Window('Инвест калькулятор', [[
    #     sg.Col([[sg.Multiline(**pa)]], **pa)
    # ]], **main_win_param)
