from .layouts import *


def main_window():
    # print(f'{sg.theme()=}')
    # print(f'{sg.theme_list()=}')
    return sg.Window('Инвест калькулятор', main_layout(), **main_win_param)
