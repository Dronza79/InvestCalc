from core.utilites import div_to_ranks
from .windows import *


class MainView:
    def __init__(self):
        sg.theme('SystemDefault1')
        self.window = main_window()
        self.run()

    def run(self):
        while True:
            ev, val = self.window.read()
            # self.window.move_to_center()
            print(f'MainView {ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
            elif ev in ['capital', 'payment']:
                self.window[ev].update(value=div_to_ranks(val[ev]))
            elif ev == 'theme':
                sg.theme('LightGreen1')
                self.window.close()
                self.window = main_window()
            elif ev == '-GO-':
                # self.window.move(0, 0)
                self.window.maximize()
                self.window['body'].update(visible=True)
        self.window.close()
