from core.utilites import div_to_ranks, clear_field_horizon, clear_field_percent, reformat_raw_input_data
from .models import update_chart
from .windows import *


class MainView:
    def __init__(self):
        sg.theme('SystemDefault1')
        self.event = self.value = self.stop = None
        self.window = main_window()
        self.init_build_graph()
        self.run()

    def run(self):
        while not self.stop:
            self.event, self.value = self.window.read()
            # print(f'MainView {self.event=} {self.value=}')

            self.formatting_input_data()
            self.close_window()
            self.managing_tab_visibility()

            if self.event in ['-GO-', '\r']:
                if check_data := self.check_fullness_raw_data():
                    sg.popup_error('Расчет не возможен', 'не заполнены поля:', *check_data)
                    continue
                valid_data = reformat_raw_input_data(**self.value)
                print(f'{valid_data=}')

                outres = self.window['-BODYNOTE-']
                # if outres.metadata:
                #     self.window[f'OUTRES-{outres.metadata}'].update(visible=False)
                #
                # outres.metadata += 1
                # self.window.extend_layout(
                #     outres,
                #     [[layout_right_explan_invest(f'OUTRES-{outres.metadata}', self.value)]])

            elif self.event in ['-CLR-', 'Delete:46']:
                [self.window[val].update('') for val in fields_input]

    def init_build_graph(self):
        update_chart(self.window['-CANVAS-'], [[0], [0], [0]])
        self.window.refresh()
        self.window.move_to_center()

    def formatting_input_data(self):
        if self.event in ['capital', 'payment', 'initial', 'horizon', 'rate']:
            self.window[self.event].update(background_color='white')
            format_input = (div_to_ranks if self.event in ['capital', 'payment', 'initial'] else
                            clear_field_horizon if self.event == 'horizon' else clear_field_percent)
            self.window[self.event].update(value=format_input(self.value[self.event]))

    def close_window(self):
        if self.event == sg.WIN_CLOSED:
            self.window.close()
            self.stop = True

    def managing_tab_visibility(self):
        if self.event != 'LTAB':
            return

        visibility_map = {
            '-INVEST-': ['-NOTE-', '-GRAPH-', '-TABLE-'],
            '-BOND-': ['-NOTE-'],
            '-DUNNO-': ['-TABLE-']
        }

        first_visible_tab = None

        for tab in self.window['RTAB'].Rows[0]:
            is_visible = tab.Key in visibility_map.get(self.value['LTAB'], [])
            tab.update(visible=is_visible)

            # Запоминаем первую видимую вкладку для активации
            if is_visible and not first_visible_tab:
                first_visible_tab = tab
                first_visible_tab.select()

    def check_fullness_raw_data(self):
        errors = set()
        type_calc = {
            'gains_capital': ['payment', 'horizon', 'rate'],
            'installment': ['capital', 'horizon', 'rate'],
            'time_to_goal': ['payment', 'capital', 'rate'],
        }

        for name, group in type_calc.items():
            if all(self.value[x] for x in group):
                self.value['type_calc'] = name
                return

            for val in group:
                if not self.value[val]:
                    errors.add((val, fields_input[val],))
        for val in errors:
            self.window[val[0]].update(background_color='Salmon')
        return [error[1] for error in errors]
