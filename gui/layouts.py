from gui.elements import *


def layout_left_invest():
    return [
        [
            capital(),
        ], [
            regular_payment(),
            periodicity('period_payment'),
        ], [
            start_amount(),
            invest_horizon(),
        ], [
            plane_profit(),
            periodicity('period_profit'),
        ], [
            additional_param(),
        ]
    ]


def layout_right_explan_invest(key, **kwargs):
    print(f'layout_right_explan_invest({key=}, {kwargs=})')
    return sg.pin(sg.Col([
        [
            expl_title(**kwargs)
        ], [
            # sg.T(capital,)
        ]
    ], key=key))


def left_part():
    return sg.Col([
        [
            sg.TabGroup([[
                sg.Tab('Инвестиции', layout_left_invest(), k='-INVEST-'),
                sg.Tab('Облигации', [[]], k='-BOND-'),
                sg.Tab('Что-то', [[]], k='-DUNNO-'),
            ]], k='LTAB', **lft_tabgroup)
        ], [
            sg.Button('РАССЧИТАТЬ', key='-GO-', button_color='white on DarkGreen', **main_btn),
        ], [
            sg.Button('ОЧИСТИТЬ', key='-CLR-', button_color='white on FireBrick', **main_btn),
        ]
    ], **lft_col)


def right_part():
    return sg.Col([
        [sg.TabGroup([[
            sg.Tab('Пояснения', [[sg.Col([[]], key='-BODYNOTE-', metadata=0)]], key='-NOTE-'),
            sg.Tab('График', [[sg.Canvas(key='-CANVAS-', **cvs)]], k='-GRAPH-'),
            sg.Tab('Таблица', [], k='-TABLE-'),
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
