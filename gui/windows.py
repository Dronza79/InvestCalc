from .layouts import *


def main_window():
    return sg.Window('Инвест калькулятор', [main_layout()], **main_win_param)
