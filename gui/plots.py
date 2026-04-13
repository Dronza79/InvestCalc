from matplotlib import ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from core.utilites import format_digit_for_graph


# --- Функции для работы с графиком ---
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=True)
    return figure_canvas_agg


def create_inscriptions_value(canvas_elem, data_list):
    for i, layer_values in enumerate(data_list[0][1:], start=1):
        max_val = data_list[1][i] + data_list[2][i]

        # Вычисляем Y-координату для текста (середина слоя)
        text_y = max_val + 10000 if i + 1 else max_val
        last_x = layer_values

        label_text = format_digit_for_graph(max_val)
        label_text1 = format_digit_for_graph(data_list[1][i])

        canvas_elem.text(last_x, text_y, label_text,
                         va='top', ha='right', fontsize=9, color='black')
        canvas_elem.text(last_x, data_list[1][i], label_text1,
                         va='bottom', ha='left', fontsize=9, color='blue')


def update_chart(canvas_elem, data_list):
    # Очистка старого графика если есть
    if hasattr(update_chart, "current_canvas"):
        update_chart.current_canvas.get_tk_widget().forget()

    fig, ax = plt.subplots(figsize=(8, 7), dpi=100)

    # Оформление внешнего вида графика
    ax.grid(True, axis='both', linestyle=':', alpha=0.7)
    ax.margins(x=0)
    ax.ticklabel_format(style='plain', axis='y')

    font_title = {'size': 12}
    font_label = {'size': 10}

    ax.set_title("Рост капитала", fontdict=font_title)
    ax.set_ylabel("Размер капитала (руб.)", fontdict=font_label)
    ax.set_xlabel("Срок (год/лет)", fontdict=font_label)

    # Для делений на осях (чисел)
    ax.tick_params(axis='both', labelsize=9, labelcolor='grey')
    formatter = ticker.FuncFormatter(format_digit_for_graph)
    ax.yaxis.set_major_formatter(formatter)

    # Построение самого графика
    ax.stackplot(*data_list, labels=['Внесено', "Доход"])
    ax.legend(loc='upper left')

    # Оформление значений на графике
    create_inscriptions_value(ax, data_list)

    fig.tight_layout()

    update_chart.current_canvas = draw_figure(canvas_elem.TKCanvas, fig)


