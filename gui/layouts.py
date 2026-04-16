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
    # return [[sg.Canvas(key='-CANVAS-')]]
    return [[
        sg.Graph(
            canvas_size=(800, 700), graph_bottom_left=(0, 0), graph_top_right=(1, 1),
            key='-G-', background_color='white',
            enable_events=True, drag_submits=True, motion_events=True
        )
    ]]


def layout_right_table():
    return [[sg.Table([], key='-DATA-TABLE-', **table)]]


def left_part():
    return sg.Col([[
        sg.TabGroup([[
            sg.Tab('План инвестиции', layout_left_invest(), k='-INVEST-'),
            sg.Tab('Баланс портфеля', layout_left_balance(), k='-BALANCE-'),
            # sg.Tab('Облигации', [[]], k='-BOND-', disabled=True),
        ]], k='ltab', **lft_tabgroup)],
        [sg.Button('РАССЧИТАТЬ', key='-GO-', button_color='white on DarkGreen', **main_btn)],
        [sg.Button('ОЧИСТИТЬ', key='-CLR-', button_color='white on FireBrick', **main_btn)]
    ], **lft_col)


def right_part():
    return sg.Col([[
        sg.TabGroup([[
            sg.Tab('Пояснения', layout_right_note(), key='-NOTE-'),
            sg.Tab('График', layout_right_graph(), k='-GRAPH-'),
            sg.Tab('Таблица', layout_right_table(), k='-TABLE-'),
        ]], k='rtab', **rht_tabgroup)]
    ], **rht_col)


def main_layout():
    return [
        [left_part(), sg.VSep(), right_part()],
        # [sg.Push(), sg.Sizegrip()],
    ]


def layout_right_note_invest(key, kwargs):
    # print(f'layout_right_note_invest({key=}, {kwargs=})')
    layout = [[invest_header_output(**kwargs)], [invest_leader_output(**kwargs)]]
    if kwargs.get('initial'):
        layout += [[invest_liner_output(key='start', **kwargs)]]
    if key in ['time_to_goal', 'installment', 'percentage'] and kwargs['capital'] != kwargs['current_balance']:
        layout += [[invest_liner_output(key='capital', **kwargs)]]
    layout += [
        [invest_liner_output(key='contrib', **kwargs)],
        [invest_liner_output(key='received', **kwargs)]]
    if kwargs.get('tax_enabled'):
        layout += [[invest_liner_output(key='paid', **kwargs)]]
    if kwargs.get('inf_enabled'):
        layout += [
            [invest_liner_output(key='inf', **kwargs)],
            [invest_inf_output(**kwargs)]
        ]

    return sg.pin(sg.Col(layout, key=key, **exp_both))


def layout_right_note_balance(key, data):
    layout = [
        [balance_header_output()],
        [general_info(**data)],
        [operations_exchange_inst(data)],
        [total_result_balance(**data)]
    ]
    return sg.pin(sg.Col(layout, key=key, **exp_both), expand_x=True)
