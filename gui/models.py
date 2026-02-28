import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Period:
    __ADDICTION = {
        'неделя': 52,
        'месяц': 12,
        'квартал': 4,
        'полгода': 2,
        'год': 1,
    }

    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def __str__(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @classmethod
    def glp(cls):
        """
        glp = get list periods
        :return:
        """
        return [cls(k, v) for k, v in cls.__ADDICTION.items()]


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

    # Оформление внешнего вида графика
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

    # Построение самого графика
    ax.stackplot(*data_list, labels=['Внесено', "Сложный процент"])

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
