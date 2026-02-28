from gui.elements import *


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
        ]
    ]


def explanations():
    return [[
        sg.Text(**expl_t)
    ]]


def left_part():
    return sg.Col([
        [
            sg.TabGroup([[
                sg.Tab('Инвестиции', layout_left_invest()),
                sg.Tab('Облигации', [[]], expand_x=True),
                sg.Tab('Что-то', [[]], expand_x=True, disabled=True),
            ]], k='LTAB', **lft_tabgroup)
        ], [
            sg.Button('РАССЧИТАТЬ', key='-GO-', **main_btn),
        ]
    ], **lft_col)


def right_part():
    return sg.Col([
        [sg.TabGroup([[
            sg.Tab('Пояснения', explanations(), key='explan'),  # **rht_tab),
            sg.Tab('График', [[sg.Canvas(key='-CANVAS-', **cvs)]]), #**rht_tab),
            sg.Tab('Таблица', []), #**rht_tab),
        ]], k='RTAB', **rht_tabgroup)],
    ], **rht_col)


def main_layout():
    return [
        [
            left_part(), sg.VSep(), right_part()
        # ], [
        #     sg.Push(),
        #     sg.Sizegrip(),
        ]
    ]
