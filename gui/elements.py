from core.utilites import *
from core.models import Period, Ratio
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
            sg.T('\u2211'),
            sg.Input('', key=key, s=15, **other_in),
            sg.T('\u20BD'),
            sg.Input('', s=5, key=f'percent_{key}', **other_in),
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
    steps = Ratio.get_steps()
    return sg.Frame('Дополнительные параметры:', [[
        sg.Col([[
            sg.Checkbox(f'{fields_input[key_1]}', key=key_1, **chbx),
            # ], [
            sg.Checkbox(f'{fields_input[key_2]}', key=key_2, **chbx),
        ]]),
        sg.Push(),
        sg.Frame('Кратность:', [[
            sg.Combo(steps, default_value=steps[0], k='ratio_step', **combo_per)
        ]])
    ]], **main_frame)


def payment_param():
    key1 = 'pay_enabled'
    key2 = 'partial_repl'
    return sg.Frame('Параметры пополнения:', [[
        sg.Checkbox(f'{fields_input[key1]}', key=key1, **chbx),
        sg.Frame('Частично пополнить:', [[
            sg.Input('', key=key2, s=15, **other_in), sg.T('\u20BD')
        ]])
    ]], **main_frame)


def periodicity_combo(key):
    list_period = Period.glp(key)
    return sg.Frame('Периодичность:', [[
        sg.Combo(
            list_period,
            default_value=list_period[1] if key != 'profit' else list_period[0],
            key=f'{key}_step', **combo_per
        ),
    ]], **main_frame)


def invest_header_output(type_calc, **data):
    param = {'font': 'Courier 20', 'pad': (5, 0)}
    layout = []
    if type_calc == 'time_to_goal':
        layout = [
            [
                sg.Text('Что бы накопить', **param),
                sg.Text(f"{div_to_ranks(str(data['capital']))}\u20BD", **param),
                sg.T('откладывая', **param),
            ], [
                sg.T(data['period_payment'], **param),
                sg.T('по', **param),
                sg.Text(f"{div_to_ranks(str(data['payment']))}\u20BD,", **param),
                sg.Text('Вам потребуется:', **param),
            ]
        ]
    elif type_calc == 'gains_capital':
        layout = [
            [
                sg.Text('Откладывая по', **param),
                sg.Text(f"{div_to_ranks(str(data['payment']))}\u20BD", **param),
                sg.T(data['period_payment'], **param)
            ], [
                sg.T('на протяжении', **param),
                sg.T(f'{format_years_genitive(data["horizon"])},', **param),
                sg.T('Вы накопите:', **param)
            ]
        ]
    elif type_calc == 'installment':
        layout = [
            [
                sg.Text('Для капитала', **param),
                sg.Text(f"{div_to_ranks(str(data['capital']))}\u20BD", **param),
                sg.T('за', **param),
                sg.T(f'{format_years_genitive(data["horizon"])},', **param),
            ], [
                sg.T('необходимо пополнять', **param),
                sg.T(data['period_payment'], **param),
                sg.T('на:', **param),
            ]
        ]
    elif type_calc == 'percentage':
        layout = [
            [
                sg.Text('Для капитала', **param),
                sg.Text(f"{div_to_ranks(str(data['capital']))}\u20BD", **param),
                sg.T('за', **param),
                sg.T(f'{format_years_genitive(data["horizon"])},', **param),
            ], [
                sg.T('пополняя', **param),
                sg.T(data['period_payment'], **param),
                sg.T(f"на {div_to_ranks(str(data['payment']))}\u20BD", **param),
                sg.T('необходимо', **param),
            ], [
                sg.T('иметь годовую ставку не менее:', **param),
            ]
        ]
    return sg.Col(layout, expand_x=True, element_justification='c', pad=20)


def balance_header_output():
    param = {'font': 'Courier 16', 'pad': (5, 0)}

    return sg.Col([
        [sg.Text("Результаты ребалансировки", **param)],
        [sg.HSeparator()],
    ], expand_x=False, justification='c', element_justification='c')


def general_info(balance_capital, extra_needed, internal_cash, partial_repl, **kwargs):
    font_param = {'font': 'Courier 12'}
    title_param = {'expand_x': True, 'justification': 'c', }
    orange = {'text_color': 'orange'}
    relay = {
        'percent_stocks': 'Акции',
        'percent_bonds': 'Облигации',
        'percent_funds': 'Фонды',
        'percent_metals': 'Драгметалы'
    }
    layout = [
        [sg.Text('Исходные данные:', p=((0, 0), (10, 0)), **title_param, **font_param)],
        [sg.HSeparator()],
        [
            sg.Text(f"- Текущий капитал:", p=0, **font_param),
            sg.Push(),
            sg.Text(div_to_ranks(round(balance_capital, 2)), p=0, **font_param),
            sg.Text(f" \u20BD", p=0, **font_param)
        ]]
    if internal_cash:
        layout += [[
            sg.Text(f"- Свободные средства:", p=0, **font_param),
            sg.Push(),
            sg.Text(div_to_ranks(round(internal_cash, 2)), p=0, **font_param),
            sg.Text(f" \u20BD", p=0, **font_param),
        ]]
    if partial_repl:
        layout += [[
            sg.Text(f"- Частичное пополнение:", p=0, **font_param),
            sg.Push(),
            sg.Text(div_to_ranks(partial_repl), p=0, **font_param),
            sg.Text(f" \u20BD", p=0, **font_param),
        ]]
    if extra_needed:
        layout += [[
            sg.Text(f"- Необходимо добавить:", p=0, **orange, **font_param),
            sg.Push(),
            sg.Text(div_to_ranks(round(extra_needed, 2)), p=0, **orange, **font_param),
            sg.Text(f" \u20BD", p=0, **orange, **font_param),
        ]]
    layout += [[sg.Text('Целевой баланс:', p=((0, 0), (10, 0)), **title_param, **font_param)], [sg.HSeparator()]]
    layout += [
        [sg.Text(f"- {relay[key]}:\t{float(kwargs[key]):<5}%", p=0, **font_param)]
        for key in relay if kwargs[key]
    ]

    return sg.Col(layout)


def operations_exchange_inst(data):
    # print(f'operations_exchange_inst({data=})')
    inst_param = {'font': 'Courier 14 bold'}
    title_param = {'expand_x': True, 'justification': 'c', }
    relay = {
        'action_stocks': 'Акции',
        'action_bonds': 'Облигации',
        'action_funds': 'Фонды',
        'action_metals': 'Драгметалы',
    }
    layout = [
        [sg.Text("Действия с биржевыми инструментами:", p=((0, 0), (10, 0)), **title_param, **inst_param)],
        [sg.HSeparator()]
    ]
    layout += [
        [
            sg.Text(f"{f'{relay[key]}:':.<20}", **inst_param),
            sg.Text(get_text(data[key]), text_color=get_color(data[key]), p=(5, 0), **inst_param),
        ] for key in relay if data[key] or data[f'percent_{key.replace("action_", "")}']
    ]
    layout += [[sg.HSeparator()]]

    return sg.Col(layout)


def total_result_balance(target_total, **data):
    font_param = {'font': 'Courier 12'}
    title_param = {'expand_x': True, 'justification': 'c', }
    total_param = {'font': 'Courier 12 bold'}
    relay = {
        'total_stocks': 'Акции',
        'total_bonds': 'Облигации',
        'total_funds': 'Фонды',
        'total_metals': 'Драгметалы',
        'internal_cash': 'Свободные средства'
    }
    layout = [
        [sg.Text('Итоговое состояние портфеля:', p=((0, 0), (10, 0)), **title_param, **font_param)],
        [sg.HSeparator()]]
    layout += [
        [
            sg.Text(f'- {relay[key]}:', **font_param),
            sg.Push(),
            sg.T(div_to_ranks(data[key]), **font_param),
            sg.T("\u20BD", p=0, **font_param)] for key in relay if data[key]
    ]
    layout += [[sg.Text(f"Итоговый капитал: {div_to_ranks(target_total)} \u20BD",
                        p=((0, 0), (10, 0)), **total_param)]]

    return sg.Col(layout)


def invest_leader_output(type_calc, **data):
    param = {'font': 'Courier 50 bold', 'pad': (5, 0)}
    layout = []
    if type_calc == 'time_to_goal':
        layout = [[sg.T(f'{format_horizon(data["horizon"])}', **param)]]
    elif type_calc == 'gains_capital':
        layout = [[
            sg.Text(div_to_ranks(str(data["current_balance"])), **param),
            sg.T('\u20BD', **param),
        ]]
    elif type_calc == 'installment':
        layout = [[
            sg.Text(div_to_ranks(str(data["payment"])), **param),
            sg.T('\u20BD', **param),
        ]]
    elif type_calc == 'percentage':
        layout = [[
            sg.Text(clear_field_percent(str(data["rate"])), **param),
            sg.T('%', **param),
        ]]
    return sg.Col(layout, expand_x=True, element_justification='c', pad=10)


def invest_liner_output(key, **kwargs):
    param = {'font': 'Courier 18', 'pad': (5, 0)}  # 'background_color': 'red'}
    ADD = {
        'start': ('initial', 'Начальная сумма:'),
        'capital': ('current_balance', 'Фактический капитал:'),
        'contrib': ('deposit', 'Сумма пополнений:'),
        'received': ('income', 'Ожидаемый доход:'),
        'paid': ('total_taxes', 'Начислено к оплате НДФЛ:'),
        'inf': ('inflation', 'Потери от инфляции:'),

    }
    return sg.Col([[
        sg.Text(f'{ADD[key][1]:.<35}', **param),
        # sg.Push(),
        sg.Text(div_to_ranks(kwargs[ADD[key][0]]), **param),
        sg.T('\u20BD', **param),
    ]], expand_x=True, element_justification='l', pad=10)


def invest_inf_output(capital_inf, payment_inf, horizon, start_date, **kwargs):
    param = {'font': 'Courier 14', 'pad': (5, 0)}  # 'background_color': 'red'}
    left_col = sg.Col([[sg.Image(info_ico)]])
    right_col = sg.Col([
        [
            sg.Text(f'При средней инфляции в размере 8% через {format_horizon(horizon)}', **param),
        ], [
            sg.Text(f'на капитал можно будет приобрести столько же,', **param),
        ], [
            sg.Text(f'сколько и в настоящее время на сумму {div_to_ranks(capital_inf)}\u20BD', **param),
        ], [
            sg.Text(f'в ценах по состоянию на {start_date:%d.%m.%Y} г.', **param),
        ], [
            sg.HSeparator(),
        ], [
            sg.Text(f'Однако, с учетом инфляции через {format_horizon(horizon)}', **param),
        ], [
            sg.Text(f'регулярный платеж будет составлять {div_to_ranks(payment_inf)}\u20BD', **param),
        ]])
    return sg.Frame('', [[left_col, right_col]],
                    expand_x=True, element_justification='l', pad=10,
                    relief=sg.RELIEF_SOLID  # тольстая рамка
                    )
