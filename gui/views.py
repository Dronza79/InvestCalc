from core.handlers import calculations
from .plots import *
from .windows import *


class MainView:
    def __init__(self):
        sg.theme('SystemDefault1')
        self.event = self.value = self.stop = None
        self.window = main_window()
        self.graph_key = '-G-'
        self.graph_data = None
        self.chart = InvestmentChart(self, self.graph_key)
        self.run()

    def run(self):
        while not self.stop:
            self.event, self.value = self.window.read()
            print(f'MainView {self.event=} {self.value=}')

            self.formatting_input_data()
            self.close_window()
            self.managing_tab_visibility()
            self.data_adjustment_in_parts()
            self.update_cursor_graph()
            self.resizable_graph()

            if self.event in ['-GO-', '\r']:
                if check_data := self.check_fullness_raw_data():
                    popup_errors_notification(self, [
                        'Расчет совершить не возможно!',
                        'Не заполнены следующие поля:'], check_data)
                    continue
                valid_data = reformat_raw_input_data(**self.value)
                # print(f'{self.value=}')
                # print(f'{valid_data=}')
                result = calculations(**valid_data)
                print(f'{result=}')

                outres = self.window['-BODYNOTE-']
                if outres.metadata:
                    self.window[f'OUTRES-{outres.metadata}'].update(visible=False)
                outres.metadata += 1

                layout_extend = (
                    layout_right_note_invest if self.value['ltab'] == '-INVEST-'
                    else layout_right_note_balance
                 )
                if result:
                    self.window.extend_layout(
                        outres,
                        [[layout_extend(f'OUTRES-{outres.metadata}', result)]])
                    self.graph_data = result['graph_data']

                if self.value['ltab'] == '-INVEST-':
                    self.chart.draw(result['graph_data'])
                    self.window['-DATA-TABLE-'].update(result['table_data'])

            elif self.event in ['-CLR-']: # 'Delete:46']:
                [self.window[val].update('') for val in key_input_format]

    def update_cursor_graph(self):
        if self.event is None:
            return
        if self.event.startswith(self.graph_key):
            self.chart.update_cursor(self.value[self.graph_key])

    def resizable_graph(self):
        if not self.graph_data:
            return
        elif self.event == '-G-+Resized':
            self.chart.draw(self.graph_data)

    def formatting_input_data(self):
        if self.event in key_input_format:
            [self.window[key].update(background_color='white') for key in key_input_format]
            format_input = (div_to_ranks if self.event in key_input_format_money else
                            clear_field_horizon if self.event == 'horizon' else clear_field_percent)
            self.window[self.event].update(value=format_input(self.value[self.event]))

    def close_window(self):
        if self.event == sg.WIN_CLOSED:
            self.window.close()
            self.stop = True

    def get_location(self):
        self.window.refresh()
        size_w, size_h = self.window.current_size_accurate()
        loc_x, loc_y = self.window.current_location()
        return loc_x + size_w // 2, loc_y + size_h // 2

    def managing_tab_visibility(self):
        if self.event != 'ltab':
            return

        visibility_map = {
            '-INVEST-': ['-NOTE-', '-GRAPH-', '-TABLE-'],
            '-BOND-': ['-NOTE-'],
            '-BALANCE-': ['-NOTE-']
        }

        first_visible_tab = None
        for tab in self.window['rtab'].Rows[0]:
            is_visible = tab.Key in visibility_map.get(self.value['ltab'], [])
            tab.update(visible=is_visible)

            # Запоминаем первую видимую вкладку для активации
            if is_visible and not first_visible_tab:
                first_visible_tab = tab
                first_visible_tab.select()

    def check_fullness_raw_data(self):
        errors = set()
        type_calc = {
            '-INVEST-': {
                'gains_capital': ['payment', 'horizon', 'rate'],
                'installment': ['capital', 'horizon', 'rate'],
                'time_to_goal': ['payment', 'capital', 'rate'],
                'percentage': ['payment', 'capital', 'horizon'],
            },
            '-BOND-': {},
            '-BALANCE-': {
                'portfolio': [
                    # ('balance_capital', 'balance_capital'),
                    ('stocks', 'percent_stocks'),
                    ('bonds', 'percent_bonds'),
                    ('funds', 'percent_funds'),
                    ('metals', 'percent_metals')
                ]
            },
        }
        tab = self.value['ltab']
        for name, group in type_calc[tab].items():
            # print(f'{name=} {group=}')
            if tab == '-INVEST-' and all(self.value[x] for x in group):
                self.value['type_calc'] = name
                return
            elif tab == '-BALANCE-' and all(bool(self.value[x]) is bool(self.value[y]) for x, y in group):
                self.value['type_calc'] = name
                return
            for val in group:
                if tab == '-INVEST-':
                    if not self.value[val]:
                        errors.add((val, fields_input[val],))
                elif tab == '-BALANCE-':
                    if not (bool(self.value[val[0]]) is bool(self.value[val[1]])):
                        field = val[0] if not self.value[val[0]] else val[1]
                        errors.add((field, fields_input[val[0]],))
        for val in errors:
            self.window[val[0]].update(background_color='Salmon')

        return [error[1] for error in errors]

    def data_adjustment_in_parts(self):
        """
        Проверка данных в группах полей и их автозаполнение
        :return:
        """
        lst_money = ['stocks', 'bonds', 'funds', 'metals']
        lst_percent = ['percent_stocks', 'percent_bonds', 'percent_funds', 'percent_metals']

        if self.event not in lst_money + lst_percent:
            return

        # if not self.value['balance_capital']:
        #     self.window['balance_capital'].update(background_color='Salmon')
        #     popup_errors_notification(self, ['ОШИБКА!!!'], ["Необходимо заполнить капитал!!!"])
        #     return

        def func(string: str):
            res = (clear_field_digits(string).replace(' ', '').replace(',', '.'))
            return float(res) if res else 0

        if self.event in lst_money:
            limit = func(self.value['balance_capital'])
            current_sum = sum(func(self.value[k]) for k in lst_money if k != self.event)
            format_func = div_to_ranks
        else:
            limit = 100
            format_func = clear_field_percent
            current_sum = sum(func(self.value[k]) for k in lst_percent if k != self.event)

        tracked_val = func(self.value[self.event])

        if current_sum + tracked_val >= limit:
            if self.event in lst_percent:
                value = limit - current_sum
                self.window[self.event].update(format_func(round(value,  2)))
                for key in lst_percent:
                    if key != self.event:
                        self.window[key].update(format_func(func(self.value[key])))
                return
            else:
                value = current_sum + tracked_val
                self.window['balance_capital'].update(format_func(round(value,  2)))
