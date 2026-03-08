from .layouts import *


def main_window():
    return sg.Window('Инвест калькулятор', main_layout(), **main_win_param)


def popup_errors_notification(parent, title_error, errors):
    x, y = parent.get_location()
    layout = [
        [sg.Col([[sg.T(title, text_color='DarkRed')] for title in title_error])],
        [sg.Col([[sg.Text(f'= {error}')] for error in errors], **col_popup_error)],
        [sg.Button('OK', s=10, p=10, button_color='white on DarkRed')]
    ]
    window = sg.Window('', layout, **popup_errors)
    w, h = window.current_size_accurate()
    window.move(x - w // 2, y - h // 2)
    window.read(close=True)
