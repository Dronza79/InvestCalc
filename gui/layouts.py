from gui.elements import *


def layout_left_invest():
    return [
        [
            capital(),
        ], [
            regular_payment(),
            periodicity('PER-PAYMENT'),
        ], [
            start_amount(),
            invest_horizon(),
        ], [
            plane_profit(),
            periodicity('PER-PROFIT'),
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
                sg.Tab('Инвестиции', layout_left_invest(), k='-INVEST-'),
                sg.Tab('Облигации', [[]], k='-BOND-'),
                sg.Tab('Что-то', [[]], k='-DUNNO-'),
            ]], k='LTAB', **lft_tabgroup)
        ], [
            sg.Button('РАССЧИТАТЬ', key='-GO-', **main_btn),
        ]
    ], **lft_col)


def right_part():
    return sg.Col([
        [sg.TabGroup([[
            sg.Tab('Пояснения', explanations(), key='-NOTE-'),  # **rht_tab),
            sg.Tab('График', [[sg.Canvas(key='-CANVAS-', **cvs)]], k='-GRAPH-'), #**rht_tab),
            sg.Tab('Таблица', [], k='-TABLE-'), #**rht_tab),
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
