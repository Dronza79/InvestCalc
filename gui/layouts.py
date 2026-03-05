from .elements import *


def layout_left_invest():
    return [[
        capital_input(),
    ], [
        regular_payment_input(),
        periodicity_combo('payment'),
    ], [
        start_amount_input(),
        invest_horizon_input(),
    ], [
        plane_profit_input(),
        periodicity_combo('profit'),
    ], [
        additional_param(),
    ]]


def layout_right_explan_invest(key, kwargs):
    # print(f'layout_right_explan_invest({key=}, {kwargs=})')

    layout = [[invest_header_output(**kwargs)], [invest_leader_output(**kwargs)]]
    if kwargs.get('initial'):
        layout += [[invest_liner_output(key='start', **kwargs)]]
    layout += [[invest_liner_output(key='contrib', **kwargs)], [invest_liner_output(key='received', **kwargs)]]
    if kwargs.get('tax_enabled'):
        layout += [[invest_liner_output(key='paid', **kwargs)]]
    if kwargs.get('inf_enabled'):
        layout += [[invest_liner_output(key='inf', **kwargs)]]

    return sg.pin(sg.Col(layout, key=key, **exp_both))


def left_part():
    return sg.Col([[
        sg.TabGroup([[
            sg.Tab('Инвестиции', layout_left_invest(), k='-INVEST-'),
            sg.Tab('Облигации', [[]], k='-BOND-'),
            sg.Tab('Что-то', [[]], k='-DUNNO-'),
        ]], k='LTAB', **lft_tabgroup)
    ], [
        sg.Button('РАССЧИТАТЬ', key='-GO-', button_color='white on DarkGreen', **main_btn),
    ], [
        sg.Button('ОЧИСТИТЬ', key='-CLR-', button_color='white on FireBrick', **main_btn),
    ]], **lft_col)


def right_part():
    return sg.Col([[
        sg.TabGroup([[
            sg.Tab('Пояснения', [[sg.Col([[]], key='-BODYNOTE-', metadata=0, **exp_both)]], key='-NOTE-'),
            sg.Tab('График', [[sg.Canvas(key='-CANVAS-')]], k='-GRAPH-'),
            sg.Tab('Таблица', [], k='-TABLE-'),
        ]], k='RTAB', **rht_tabgroup)
    ]], **rht_col)


def main_layout():
    return [[
        left_part(), sg.VSep(), right_part()
        # ], [
        #     sg.Push(),
        #     sg.Sizegrip(),
    ]]
