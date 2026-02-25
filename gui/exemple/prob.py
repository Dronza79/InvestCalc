# import PySimpleGUI as sg
#
# layout = [
#     [sg.TabGroup([[
#         sg.Tab('Вкладка 1', [[sg.Text('Содержимое 1')]], key='-TAB1-', metadata='-TAB2-'),
#         sg.Tab('Вкладка 2', [[sg.Text('Содержимое 2')]], key='-TAB2-', metadata='-TAB1-')
#     ]], key='-GROUP-')],
#     [sg.Button('Перейти на другую вкладку', key='-GO-')]
# ]
#
# window = sg.Window('Пример переключения', layout)
#
# while True:
#     event, values = window.read()
#     print(f'{event=} {values=}')
#     if event == sg.WIN_CLOSED:
#         break
#
#     if event == '-GO-':
#         md = window[values['-GROUP-']].metadata
#         print(window['-GROUP-'].Rows[0][0].Rows)
#         window[md].select()
#
# window.close()
#
# import PySimpleGUI as sg
#
# # Настройка темы
# sg.theme('Default1')
#
# # Левая панель - Ввод
# input_column = [
#     [sg.Text('Параметры', font='Any 15 bold')],
#     [sg.Text('Начальная сумма:'), sg.Push(), sg.Input(key='-START-', size=(15, 1))],
#     [sg.Text('Ежемесячный взнос:'), sg.Push(), sg.Input(key='-ADD-', size=(15, 1))],
#     [sg.Text('Срок (лет):')],
#     [sg.Slider(range=(1, 30), orientation='h', key='-YEARS-', default_value=10)],
#     [sg.Text('Доходность (%):'), sg.Push(), sg.Input(key='-PERCENT-', size=(15, 1))],
#     [sg.Button('РАССЧИТАТЬ', size=(20, 2), button_color=('white', 'green'), pad=(0, 20))]
# ]
#
# # Правая панель - Итоги
# result_column = [
#     [sg.Text('Результат расчета', font='Any 15 bold')],
#     [sg.Frame('', [
#         [sg.Text('Итоговый капитал:', font='Any 12')],
#         [sg.Text('0.00 ₽', font='Any 20 bold', key='-TOTAL-', text_color='#FFCC00')],
#         [sg.Text('Из них пополнения:', font='Any 10'), sg.Text('0 ₽', key='-INVESTED-')],
#         [sg.Text('Чистый доход:', font='Any 10'), sg.Text('0 ₽', key='-PROFIT-', text_color='lightgreen')]
#     ], size=(300, 150), border_width=2)],
#     [sg.Text('Здесь будет график (Canvas/Matplotlib)', size=(40, 10), background_color='black')]
# ]
#
# layout = [[sg.Column(input_column), sg.VerticalSeparator(), sg.Column(result_column)]]
#
# window = sg.Window('Investment Calculator v1.0', layout, finalize=True)
#
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED:
#         break
#
# window.close()

import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --- Функции для работы с графиком ---
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def update_chart(canvas_elem, data):
    # Очистка старого графика если есть
    if hasattr(update_chart, "current_canvas"):
        update_chart.current_canvas.get_tk_widget().forget()

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    ax.plot(data, marker='o', color='#0078D7')
    ax.set_title("Рост капитала")
    ax.grid(True, linestyle='--', alpha=0.6)

    update_chart.current_canvas = draw_figure(canvas_elem.TKCanvas, fig)


# --- Интерфейс ---
sg.theme('DarkBlue12')


# Левая часть: Вкладки ввода
def input_tab(name, key_suffix):
    return sg.Tab(name, [
        [sg.Text(f'Настройка: {name}', font='Any 12 bold')],
        [sg.Text('Цель (₽):'), sg.Push(), sg.Input('1000000', key=f'-TARGET_{key_suffix}-', size=(15, 1))],
        [sg.Text('Срок (лет):'), sg.Push(), sg.Input('10', key=f'-YEARS_{key_suffix}-', size=(15, 1))],
        [sg.Text('Ставка (%):'), sg.Push(), sg.Input('15', key=f'-RATE_{key_suffix}-', size=(15, 1))],
    ], key=f'-MODE_{key_suffix}-', metadata=key_suffix)


left_col = [
    [sg.TabGroup([[
        input_tab('Капитал', 'CAP'),
        input_tab('Платеж', 'PAY'),
        input_tab('Срок', 'TIME')
    ]], key='-IN_TABS-')],
    [sg.Button('РАССЧИТАТЬ', expand_x=True, button_color='green', size=(0, 2), pad=(0, 10))]
]

# Правая часть: Вкладки вывода
right_col = [
    [sg.TabGroup([[
        sg.Tab('График', [[sg.Canvas(key='-CANVAS-')]]),
        sg.Tab('Таблица', [[sg.Table(values=[['', '']], headings=['Год', 'Баланс'],
                                     auto_size_columns=False, col_widths=[10, 20],
                                     num_rows=15, key='-TABLE-')]])
    ]])]
]

layout = [[sg.Column(left_col), sg.VerticalSeparator(), sg.Column(right_col)]]

window = sg.Window('Invest Pro Calc', layout, finalize=True)

# Инициализируем пустой график при старте
update_chart(window['-CANVAS-'], [0, 0, 0])

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'РАССЧИТАТЬ':
        # Пример простых данных для демонстрации (здесь будет ваша математика)
        try:
            # Получаем суффикс активной вкладки через метаданные
            active_tab_key = values['-IN_TABS-']
            mode = window[active_tab_key].metadata

            # Имитация расчета экспоненты
            years = int(values[f'-YEARS_{mode}-'])
            rate = float(values[f'-RATE_{mode}-']) / 100

            data_points = [1000 * (1 + rate) ** i for i in range(years + 1)]
            table_data = [[f"Год {i}", f"{v:,.2f}"] for i, v in enumerate(data_points)]

            # Обновляем интерфейс
            update_chart(window['-CANVAS-'], data_points)
            window['-TABLE-'].update(values=table_data)

        except Exception as e:
            sg.popup_error(f"Ошибка в данных: {e}")

window.close()
