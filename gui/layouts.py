from .elements import *


def layout_left_invest():
    return [
        [capital_input()],
        [amount_money_input('payment'), periodicity_combo('payment')],
        [amount_money_input('initial'), invest_horizon_input()],
        [plane_profit_input(), periodicity_combo('profit')],
        [additional_param()]
    ]


def layout_left_balance():
    return (
        [[capital_input('balance_')]] +
        [[exchange_instrument_input(k)] for k in ['stocks', 'bonds', 'funds', 'metals']] +
        [[payment_param()]]
    )


def layout_right_note():
    return [[sg.Col([[]], key='-BODYNOTE-', metadata=0, **exp_both)]]


def layout_right_graph():
    return [[sg.Canvas(key='-CANVAS-')]]


def left_part():
    return sg.Col([[
        sg.TabGroup([[
            sg.Tab('Инвестиции', layout_left_invest(), k='-INVEST-'),
            sg.Tab('Облигации', [[]], k='-BOND-'),
            sg.Tab('Баланс портфеля', layout_left_balance(), k='-BALANCE-'),
        ]], k='LTAB', **lft_tabgroup)],
        [sg.Button('РАССЧИТАТЬ', key='-GO-', button_color='white on DarkGreen', **main_btn)],
        [sg.Button('ОЧИСТИТЬ', key='-CLR-', button_color='white on FireBrick', **main_btn)]
    ], **lft_col)


def right_part():
    return sg.Col([[
        sg.TabGroup([[
            sg.Tab('Пояснения', layout_right_note(), key='-NOTE-'),
            sg.Tab('График', layout_right_graph(), k='-GRAPH-'),
            sg.Tab('Таблица', [[]], k='-TABLE-'),
        ]], k='RTAB', **rht_tabgroup)]
    ], **rht_col)


def main_layout():
    return [
        [left_part(), sg.VSep(), right_part()],
        # [sg.Push(), sg.Sizegrip()],
    ]


def layout_right_note_invest(key, kwargs):
    layout = [[invest_header_output(**kwargs)], [invest_leader_output(**kwargs)]]
    if kwargs.get('initial'):
        layout += [[invest_liner_output(key='start', **kwargs)]]
    layout += [[invest_liner_output(key='contrib', **kwargs)], [invest_liner_output(key='received', **kwargs)]]
    if kwargs.get('tax_enabled'):
        layout += [[invest_liner_output(key='paid', **kwargs)]]
    if kwargs.get('inf_enabled'):
        layout += [[invest_liner_output(key='inf', **kwargs)]]

    return sg.pin(sg.Col(layout, key=key, **exp_both))
