from .layouts import *
from .params import *


def main_window():
    return sg.Window('Calc', main_layout(), **main_win_param)
