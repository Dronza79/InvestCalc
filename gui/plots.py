import math

from core.utilites import format_digit_for_graph
from gui.params import COLOR_PROFIT, COLOR_INITIAL, COLOR_DEPOSIT


class InvestmentChart:
    def __init__(self, parent, graph_key='-G-'):
        self.graph_elem = parent.window[graph_key]
        self.graph_elem.bind('<Configure>', '+Resized')
        self.interactive_elements = []
        self.totals = []
        self.payments = []
        self.profits = []
        self.initial = 0
        self.max_x = 0
        self.max_y = 0
        self.display_max_y = 0

    def draw(self, data):
        self.graph_elem.CanvasSize = self.graph_elem.get_size()
        self.initial, years, self.payments, self.profits = data
        self.totals = [d + i + self.initial for d, i in zip(self.payments, self.profits)]
        self.max_x, self.max_y = max(years), max(self.totals)

        # Выбор шага Y
        cap = 10 ** (len(str(self.max_y)) - 2)
        step_y = ((self.max_y + cap - 1) // cap * cap) // 4

        self.display_max_y = ((self.max_y // step_y) + 1) * step_y

        # Настройка масштаба (увеличиваем отступы под новые позиции названий)
        offset_x, offset_y = self.max_x * 0.18, self.display_max_y * 0.15
        self.graph_elem.change_coordinates((-offset_x, -offset_y), (self.max_x * 1.1, self.display_max_y * 1.1))
        self.graph_elem.erase()

        # 1. СЛОИ
        start = (0, self.initial)
        end = (self.max_x, self.initial)
        poly_total = [start] + [(years[i], self.totals[i]) for i in range(len(years))] + [end]
        self.graph_elem.draw_polygon(poly_total, fill_color=COLOR_PROFIT[0], line_color=COLOR_PROFIT[1])
        poly_dep = [start] + [(years[i], self.payments[i] + self.initial) for i in range(len(years))] + [end]
        self.graph_elem.draw_polygon(poly_dep, fill_color=COLOR_DEPOSIT[0], line_color=COLOR_DEPOSIT[1])
        self.graph_elem.draw_rectangle(start, (self.max_x, 0), fill_color=COLOR_INITIAL[0], line_width=0)

        # 2. СЕТКА
        curr_y = step_y
        # self.graph_elem.draw_text('0', (-self.max_x * 0.03, 0), color='#D0D0D0', text_location='e', font='Courier 10')
        while curr_y <= self.display_max_y:
            self.graph_elem.draw_line((0, curr_y), (self.max_x * 1.01, curr_y), color='#D0D0D0')
            self.graph_elem.draw_text(
                format_digit_for_graph(curr_y), (-self.max_x * 0.03, curr_y),
                color='#D0D0D0', text_location='e', font='Courier 10')
            curr_y += step_y

        x_step = max(1, math.ceil(self.max_x / 6))
        for x in range(0, int(self.max_x) + 1, int(x_step)):
            self.graph_elem.draw_line((x, 0), (x, self.display_max_y * 1.01), color='#D0D0D0')
            self.graph_elem.draw_text(str(x), (x, -self.display_max_y * 0.05), color='#D0D0D0', font='Courier 11')

        # 3. ОСИ И НАЗВАНИЯ (Новое расположение)
        self.graph_elem.draw_line((0, 0), (0, self.display_max_y * 1.01), width=2)
        self.graph_elem.draw_line((0, 0), (self.max_x * 1.01, 0), width=2)

        # Y Слева вертикально
        self.graph_elem.draw_text('Размер капитала (\u20BD)', (-self.max_x * 0.15, self.display_max_y / 2), angle=90,
                                  font='Courier 12 bold')
        # X Снизу горизонтально
        self.graph_elem.draw_text('Инвест горизонт (срок, годы)', (self.max_x / 2, -self.display_max_y * 0.1),
                                  font='Courier 12 bold')

        # 4. ЛЕГЕНДА
        self.draw_legend()

    def update_cursor(self, mouse_coords):
        if mouse_coords is None:
            return
        mx, my = mouse_coords

        if 0 <= mx <= self.max_x:
            idx = int(round(mx))
            if 0 <= idx < len(self.totals):
                for item in self.interactive_elements:
                    self.graph_elem.delete_figure(item)
                self.interactive_elements.clear()

                v_total, v_dep, v_int = self.totals[idx], self.payments[idx], self.profits[idx]

                # Прицелы
                l1 = self.graph_elem.draw_line((idx, 0), (idx, v_total), color='gray', width=1)
                l2 = self.graph_elem.draw_line((0, v_total), (idx, v_total), color='gray', width=1)

                self.interactive_elements.extend([l1, l2])

                # МАРКЕРЫ
                if idx > 0:
                    m1 = self.graph_elem.draw_circle((idx, v_total), self.max_x * 0.005, fill_color='orange',
                                                     line_color='white')
                    m2 = self.graph_elem.draw_circle((idx, v_dep + self.initial), self.max_x * 0.005,
                                                     fill_color='orange', line_color='white')

                    # ПОДПИСИ
                    offset = self.display_max_y * 0.005

                    # Доход (СВЕРХУ - text_location='s')
                    txt_int = self.graph_elem.draw_text(
                        f'Доход: {format_digit_for_graph(v_int)}', (idx, v_total + offset),
                        # f'Доход: {format_digit_for_graph(v_int - self.initial)}', (idx, v_total + offset),
                        color='#1b5e20', font='Courier 9 bold', text_location='s')

                    # Внесено (СНИЗУ - text_location='n')
                    txt_dep = self.graph_elem.draw_text(
                        f'Внесено: {format_digit_for_graph(v_dep)}', (idx, v_dep - offset + self.initial),
                        # f'Внесено: {format_digit_for_graph(v_dep - self.initial)}', (idx, v_dep - offset),
                        color='#0d47a1', font='Courier 9 bold', text_location='n')

                    self.interactive_elements.extend([m1, m2, txt_int, txt_dep])

                # ПОДСВЕТКА ОСЕЙ (С перекрытием старых цифр белым фоном)

                # Ось X
                bg_x = self.graph_elem.draw_rectangle(
                    (idx - 0.5, -self.display_max_y * 0.03), (idx + 0.5, -self.display_max_y * 0.07),
                    fill_color='white', line_width=0, line_color='black')
                t_x = self.graph_elem.draw_text(
                    str(idx), (idx, -self.display_max_y * 0.05), color='#9154CE', font='Courier 12 bold')

                # Ось Y
                bg_y = self.graph_elem.draw_rectangle(
                    (-self.max_x * 0.12, v_total + self.display_max_y * 0.03),
                    (-0.2, v_total - self.display_max_y * 0.03),
                    fill_color='white', line_width=0, line_color='black')
                t_y = self.graph_elem.draw_text(
                    format_digit_for_graph(v_total), (-self.max_x * 0.03, v_total),
                    color='#9154CE', font='Courier 12 bold', text_location='e')

                self.interactive_elements.extend([l1, l2, bg_x, t_x, bg_y, t_y])

    def draw_legend(self):
        # 1. Позиция: ВНУТРИ графика (левый верхний угол)
        # Делаем отступ от осей внутрь на 2% от ширины и высоты
        lx = self.max_x * 0.02
        ly_top = self.display_max_y * 0.98  # На 2% ниже верхней границы Y

        # Габариты (в 2 раза меньше первоначальных)
        l_width = self.max_x * 0.15
        l_height = self.display_max_y * 0.08

        # 2. Белая подложка с тонкой рамкой (чтобы сетка не мешала тексту)
        self.graph_elem.draw_rectangle((lx, ly_top),
                                       (lx + l_width, ly_top - l_height),
                                       fill_color='white', line_color='#CCCCCC', line_width=1)

        # Параметры элементов (уменьшенные)
        square_w = self.max_x * 0.02
        square_h = self.display_max_y * 0.02
        text_offset_x = self.max_x * 0.04

        # 3. Элемент: Доход
        y_vneseno = ly_top - self.display_max_y * 0.015
        self.graph_elem.draw_rectangle((lx + self.max_x * 0.01, y_vneseno),
                                       (lx + self.max_x * 0.01 + square_w, y_vneseno - square_h),
                                       fill_color=COLOR_PROFIT[0], line_width=0)
        self.graph_elem.draw_text('Доход', (lx + text_offset_x, y_vneseno - square_h / 2),
                                  text_location='w', font='Courier 9')

        # 4. Элемент: Внесено
        y_dohod = y_vneseno - self.display_max_y * 0.03
        self.graph_elem.draw_rectangle((lx + self.max_x * 0.01, y_dohod),
                                       (lx + self.max_x * 0.01 + square_w, y_dohod - square_h),
                                       fill_color=COLOR_DEPOSIT[0], line_width=0)
        self.graph_elem.draw_text('Внесено', (lx + text_offset_x, y_dohod - square_h / 2),
                                  text_location='w', font='Courier 9')
