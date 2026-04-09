import importlib
from datetime import date

import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from matplotlib import ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Period:
    __ADDICTION = {
        'ежедневно': relativedelta(days=1),
        'еженедельно': relativedelta(weeks=1),
        'ежемесячно': relativedelta(months=1),
        'поквартально': relativedelta(months=3),
        'полугодично': relativedelta(months=6),
        'ежегодно': relativedelta(years=1),
    }

    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def __str__(self):
        return self.__name

    def __repr__(self):
        return f'{type(self).__name__}={self.__value}'

    def __add__(self, other):
        # Позволяет делать: period + date
        if isinstance(other, date):
            return other + self.__value
        return NotImplemented

    def __radd__(self, other):
        # Позволяет делать: date + period
        return self.__add__(other)

    def __sub__(self, other):
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, date):
            return other - self.__value
        return NotImplemented

    @property
    def duration(self):
        return self.__value

    @classmethod
    def glp(cls, key=''):
        """
        glp = get list periods
        :key: str варианты для начисления процентов и взноса платежей.
        Для процентов нет еженедельно, для пополнений нет ежедневно
        :return: List[Period]
        """
        return (
            [cls(k, v) for k, v in cls.__ADDICTION.items() if k != 'еженедельно'] if key == 'profit' else
            [cls(k, v) for k, v in cls.__ADDICTION.items() if k != 'ежедневно']
        )

    @property
    def year(self):
        return self.__value.years

    @property
    def month(self):
        return self.__value.months

    def get_year_fraction(self):  # частица года
        years = self.year
        months = self.month
        days = self.__value.days
        return years + (months / 12) + (days / 365.25)

    def times_per_year(self):  # количество раз в году
        return int(1 / self.get_year_fraction())


# --- Функции для работы с графиком ---
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=True)
    return figure_canvas_agg


def create_inscriptions_value(canvas_elem, data_list):
    format_digit = importlib.import_module("core.utilites").format_digit_for_graph
    for i, layer_values in enumerate(data_list[0][1:], start=1):
        max_val = data_list[1][i] + data_list[2][i]

        # Вычисляем Y-координату для текста (середина слоя)
        text_y = max_val + 10000 if i + 1 else max_val
        last_x = layer_values

        # label_text = f"{max_val:,}".replace(',', ' ')
        label_text = format_digit(max_val)
        # label_text1 = f"{data_list[1][i]:,}".replace(',', ' ')
        label_text1 = format_digit(data_list[1][i])

        canvas_elem.text(last_x, text_y, label_text,
                         va='top', ha='right', fontsize=9, color='black')
        canvas_elem.text(last_x, data_list[1][i], label_text1,
                         va='bottom', ha='left', fontsize=9, color='blue')


def update_chart(canvas_elem, data_list):
    # Очистка старого графика если есть
    print(f'{data_list=}')
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
    formatter = ticker.FuncFormatter(
        lambda x, p: f"{int(x / 1e6)}кк" if x == 1e6
        else f"{x / 1e6:.1f}кк" if x > 1e6
        else f"{int(x / 1e3)}к"
    )
    ax.yaxis.set_major_formatter(formatter)

    # Построение самого графика
    ax.stackplot(*data_list, labels=['Внесено', "Доход"])
    ax.legend(loc='upper left')

    # Оформление значений на графике
    create_inscriptions_value(ax, data_list)

    fig.tight_layout()

    update_chart.current_canvas = draw_figure(canvas_elem.TKCanvas, fig)


class Ratio:
    __STEPS = [1, 100, 500, 1000]

    def __init__(self, step):
        self.__step = step

    def __str__(self):
        return str(self.__step)

    def __repr__(self):
        return f'{type(self).__name__}={self.__step}'

    def up(self, number):
        return (number + self.__step - 1) // self.__step * self.__step

    def down(self, number):
        return number // self.__step * self.__step

    @classmethod
    def get_steps(cls):
        return [cls(v) for v in cls.__STEPS]

