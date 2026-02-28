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
from typing import List

import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --- Функции для работы с графиком ---
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def update_chart(canvas_elem, data_list, labels):
    # Очистка старого графика если есть
    print(f'{data_list=}')
    if hasattr(update_chart, "current_canvas"):
        update_chart.current_canvas.get_tk_widget().forget()

    fig, ax = plt.subplots(figsize=(8, 7), dpi=100)
    ax.stackplot(*data_list, labels=labels)
    ax.legend(loc='upper right')
    ax.grid(True, axis='both', linestyle=':', alpha=0.7)
    ax.margins(x=0)
    ax.ticklabel_format(style='plain', axis='y')

    font_title = {'size': 12}
    font_label = {'size': 10}

    ax.set_title("Накопительный итог", fontdict=font_title)
    ax.set_ylabel("Сумма (руб.)", fontdict=font_label)
    ax.set_xlabel("Срок в годах", fontdict=font_label)

    # Для делений на осях (чисел)
    ax.tick_params(axis='both', labelsize=9, labelcolor='grey')
    formatter = ticker.FuncFormatter(
        lambda x, p: f"{int(x / 1e6)}кк" if x == 1e6
        else f"{x / 1e6:.1f}кк" if x > 1e6
        else f"{int(x / 1e3)}к"
    )
    ax.yaxis.set_major_formatter(formatter)

    for i, layer_values in enumerate(data_list[0][1:], start=1):
        val = data_list[1][i] + data_list[2][i]  # Берем значение в последней точке

        # Вычисляем Y-координату для текста (середина слоя)
        text_y = val
        last_x = layer_values

        # Форматируем число (например, в 'к')
        # label_text = (
        #     f"{int(val / 1e6)}кк" if val == 1e6
        #     else f"{val / 1e6:.1f}кк" if val > 1e6
        #     else f"{int(val / 1e3)}к"
        # )
        label_text = f"{(val + 499) // 500 * 500:,}".replace(',', ' ')

        # Рисуем текст
        print(f'{last_x=} {text_y=} {label_text=}')
        ax.text(last_x, text_y, label_text,
                va='center', ha='right', fontsize=9, fontweight='bold', color='black')

        # current_bottom += val  # Сдвигаем "пол" для следующего слоя

    fig.tight_layout()

    update_chart.current_canvas = draw_figure(canvas_elem.TKCanvas, fig)


# --- Интерфейс ---
sg.theme('Default1')


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
        sg.Tab('График', [[sg.Canvas(key='-CANVAS-')]], expand_y=True, expand_x=True),
        sg.Tab('Таблица', [[sg.Table(values=[['', '']], headings=['Год', 'Баланс'],
                                     auto_size_columns=False, col_widths=[10, 20],
                                     num_rows=15, key='-TABLE-')]], expand_y=True, expand_x=True)
    ]], expand_y=True, expand_x=True)]
]

layout = [[sg.Column(left_col), sg.VerticalSeparator(), sg.Column(right_col, expand_y=True, expand_x=True)]]

window = sg.Window('Invest Pro Calc', layout, finalize=True, resizable=True)

# Инициализируем пустой график при старте
update_chart(window['-CANVAS-'], [[0], [0], [0]], ['Внесено', "Сложный процент"])

w, h = window.current_size_accurate()
window.move_to_center()
window.move(w // 2, h // 2)
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

            data_points = [
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                 28,
                 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
                 55, 56, 57, 58, 59, 60],
                [0, 12000, 24000, 36000, 48000, 60000, 72000, 84000, 96000, 108000, 120000, 132000, 144000, 156000,
                 168000,
                 180000, 192000, 204000, 216000, 228000, 240000, 252000, 264000, 276000, 288000, 300000, 312000, 324000,
                 336000, 348000, 360000, 372000, 384000, 396000, 408000, 420000, 432000, 444000, 456000, 468000, 480000,
                 492000, 504000, 516000, 528000, 540000, 552000, 564000, 576000, 588000, 600000, 612000, 624000, 636000,
                 648000, 660000, 672000, 684000, 696000, 708000, 920000],
                [0, 12000, 24140, 36421, 48846, 61416, 74132, 86997, 100012, 113179, 126500, 139975, 153608, 167401,
                 181354, 195469, 209750, 224197, 238813, 253599, 268557, 283691, 299000, 314489, 330158, 346010, 362046,
                 378270, 394683, 411288, 428086, 445081, 462273, 479666, 497263, 515064, 533073, 551292, 569724, 588371,
                 607235, 626320, 645627, 665159, 684919, 704910, 725134, 745594, 766292, 787232, 808417, 829848, 851530,
                 873464, 895655, 918104, 940815, 963792, 987036, 1010551, 2034341]]
            new_point = list(map(lambda x: x[0::12], data_points))
            for i in range(len(new_point[0])):
                new_point[0][i] = new_point[0][i] / 12
                new_point[2][i] = new_point[2][i] - new_point[1][i]
            # table_data = [[f"Год {i}", f"{v:,.2f}"] for i, v in enumerate(data_points)]
            # print(f'{data_points=}')
            # Обновляем интерфейс
            update_chart(window['-CANVAS-'], new_point, ['внесено', "сложный процент"])
            # window['-TABLE-'].update(values=table_data)

        except Exception as e:
            print(e.__traceback__.__dict__)
            sg.popup_error(f"Ошибка в данных: {e}")

window.close()
