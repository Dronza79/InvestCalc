from core.utilites import div_to_ranks
from .windows import *


class MainView:
    def __init__(self):
        self.window = main_window()
        self.run()

    def run(self):
        while True:
            ev, val = self.window.read()
            print(f'MainView {ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
            elif ev == 'capital':
                self.window[ev].update(value=div_to_ranks(val[ev]))
        self.window.close()
