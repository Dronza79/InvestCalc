import PySimpleGUI as sg

from core.utilites import div_to_ranks, format_years_genitive
from .models import Period
from .params import *


def capital_input(clone=''):
    key = 'capital'
    return sg.Frame(f'{fields_input[key]}:', [[
        sg.Input('', key=f'{clone}{key}', **cap_in),
        sg.T('\u20BD', font='_ 20'),
    ]], **main_frame)


def amount_money_input(key):
    return sg.Frame(f'{fields_input[key]}:', [[
        sg.Input('', key=key, s=10, **other_in),
        sg.T('\u20BD'),
    ]], **main_frame)


def exchange_instrument_input(key):
    return sg.Frame(f'{fields_input[key]}:', [
        [
            sg.Input('', key=key, s=15, **other_in),
            sg.T('\u20BD'),
            sg. Input('', s=5, key=f'percent_{key}', **other_in),
            sg.Text('%')
        ]
    ], **main_frame)


def invest_horizon_input():
    key = 'horizon'
    return sg.Frame(f'{fields_input[key]}:', [[
        sg.Input('', key=key, s=10, **other_in)
    ]], **main_frame)


def plane_profit_input():
    key = 'rate'
    return sg.Frame(f'{fields_input[key]}:', [[
        sg.Input('', key=key, s=8, **other_in),
        sg.Text('%'),
    ]], **main_frame)


def additional_param():
    key_1 = 'tax_enabled'
    key_2 = 'inf_enabled'
    return sg.Frame('Дополнительные параметры:', [[
        sg.Col([[
            sg.Checkbox(f'{fields_input[key_1]}', key=key_1, **chbx),
            # ], [
            sg.Checkbox(f'{fields_input[key_2]}', key=key_2, **chbx),
        ]]),
        sg.Push(),
        sg.Frame('Кратность:', [[
            sg.Combo(['1', '100', '500', '1000'], default_value=500, k='ratio', **combo_per)
        ]])
    ]], **main_frame)


def payment_param():
    key1 = 'pay_enabled'
    key2 = 'partial_repl'
    return sg.Frame('Дополнительные параметры:', [
        [
            sg.Checkbox(f'{fields_input[key1]}', key=key1, **chbx),
            sg.Input('', key=key2, s=10, **other_in),
            sg.T('\u20BD'),
        ]
    ], **main_frame)


def periodicity_combo(key):
    list_period = Period.glp(key)
    return sg.Frame('Периодичность:', [[
        sg.Combo(
            list_period,
            default_value=list_period[1] if key != 'profit' else list_period[0],
            key=f'{key}_step', **combo_per
        ),
    ]], **main_frame)


def invest_header_output(period_payment, payment, horizon, **kwargs):
    param = {'font': 'Courier 20', 'pad': (5, 0)}
    return sg.Col([[
        sg.Text('Откладывая по', **param),
        sg.Text(div_to_ranks(str(payment)), **param),
        sg.T('\u20BD', **param),
        sg.T(period_payment, **param)
    ], [
        sg.T('на протяжении', **param),
        sg.T(f'{format_years_genitive(horizon)},', **param),
        sg.T('вы накопите:', **param)
    ]], expand_x=True, element_justification='c', pad=20)


def invest_leader_output(capital_gans, **kwargs):
    param = {'font': 'Courier 50 bold', 'pad': (5, 0)}
    return sg.Col([[
        sg.Text(div_to_ranks(str(capital_gans)), **param),
        sg.T('\u20BD', **param),
    ]], expand_x=True, element_justification='c', pad=10)


def invest_liner_output(key, **kwargs):
    param = {'font': 'Courier 18', 'pad': (5, 0)}  # 'background_color': 'red'}
    ADD = {
        'start': ('initial', 'Начальная сумма:'),
        'contrib': ('deposit', 'Сумма пополнений:'),
        'received': ('income', 'Полученный доход:'),
        'paid': ('total_taxes', 'Уплачено налогов:'),
        'inf': ('inflation', 'Инфляция:'),

    }
    return sg.Col([[
        sg.Text(f'{ADD[key][1]:.<35}', **param),
        # sg.Push(),
        sg.Text(div_to_ranks(kwargs[ADD[key][0]]), **param),
        sg.T('\u20BD', **param),
    ]], expand_x=True, element_justification='l', pad=10)
