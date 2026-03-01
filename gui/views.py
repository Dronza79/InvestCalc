from core.utilites import div_to_ranks
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
            elif ev in ['capital', 'payment', 'start']:
                self.window[ev].update(value=div_to_ranks(val[ev]))
            elif ev == 'theme':
                sg.theme('LightGreen1')
                self.window.close()
                self.window = main_window()
            elif ev == '-GO-':
                self.window.move_to_center()
            elif ev == 'LTAB':
                [el.update(visible=True) for el in self.window['RTAB'].Rows[0]]
                if val['LTAB'] == '-BOND-':
                    [el.update(visible=False) for el in self.window['RTAB'].Rows[0] if el.key != '-NOTE-']
                elif val['LTAB'] == '-DUNNO-':
                    [el.update(visible=False) for el in self.window['RTAB'].Rows[0] if el.key != '-TABLE-']
                el = self.window['RTAB'].Rows[0][0]
                if el.visible:
                    el.select()

        self.window.close()

    def init_build_graph(self):
        update_chart(self.window['-CANVAS-'], [[0], [0], [0]])
        self.window.refresh()
        self.window.move_to_center()
