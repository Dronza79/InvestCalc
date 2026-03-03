from core.utilites import div_to_ranks, clear_field_horizon, clear_field_percent
from .models import update_chart
from .windows import *


class MainView:
    def __init__(self):
        sg.theme('SystemDefault1')
        self.window = main_window()
        self.init_build_graph()
        self.run()

    def run(self):
        while True:
            ev, val = self.window.read()
            print(f'MainView {ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
            elif ev in ['capital', 'payment', 'initial']:
                self.window[ev].update(value=div_to_ranks(val[ev]))
            elif ev in ['horizon', 'rate']:
                clear_func = clear_field_horizon if ev == 'horizon' else clear_field_percent
                self.window[ev].update(value=clear_func(val[ev]))
            elif ev == 'LTAB':
                [el.update(visible=True) for el in self.window['RTAB'].Rows[0]]
                if val['LTAB'] == '-BOND-':
                    [el.update(visible=False) for el in self.window['RTAB'].Rows[0] if el.key != '-NOTE-']
                elif val['LTAB'] == '-DUNNO-':
                    [el.update(visible=False) for el in self.window['RTAB'].Rows[0] if el.key != '-TABLE-']
                el = self.window['RTAB'].Rows[0][0]
                if el.visible:
                    el.select()

            elif ev == '-GO-':
                outres = self.window['-BODYNOTE-']
                if outres.metadata:
                    self.window[f'OUTRES-{outres.metadata}'].update(visible=False)

                outres.metadata += 1
                self.window.extend_layout(
                    outres,
                    [[layout_right_explan_invest(f'OUTRES-{outres.metadata}', **val)]])


        self.window.close()

    def init_build_graph(self):
        update_chart(self.window['-CANVAS-'], [[0], [0], [0]])
        self.window.refresh()
        self.window.move_to_center()
