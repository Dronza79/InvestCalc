import math

from core.utilites import format_digit_for_graph


class InvestmentChart:
    def __init__(self, parent, graph_key='-G-'):
        self.graph_elem = parent.window[graph_key]
        self.interactive_elements = []
        self.totals = []
        self.deposits = []
        self.interests = []
        self.max_x = 0
        self.max_y = 0
        self.display_max_y = 0

    def draw(self, data):
        years, self.deposits, self.interests = data
        self.totals = [d + i for d, i in zip(self.deposits, self.interests)]
        self.max_x, self.max_y = max(years), max(self.totals)

        # Выбор шага Y
        cap = 10 ** (len(str(self.max_y)) - 2)
        step_y = ((self.max_y + cap - 1) // cap * cap) // 5

        self.display_max_y = ((self.max_y // step_y) + 1) * step_y

        # Настройка масштаба (увеличиваем отступы под новые позиции названий)
        offset_x, offset_y = self.max_x * 0.25, self.display_max_y * 0.2
        self.graph_elem.change_coordinates((-offset_x, -offset_y), (self.max_x * 1.15, self.display_max_y * 1.2))
        self.graph_elem.erase()

        # 1. СЛОИ
        poly_total = [(0, 0)] + [(years[i], self.totals[i]) for i in range(len(years))] + [(self.max_x, 0)]
        self.graph_elem.draw_polygon(poly_total, fill_color='#2ecc71', line_color='#27ae60')
        poly_dep = [(0, 0)] + [(years[i], self.deposits[i]) for i in range(len(years))] + [(self.max_x, 0)]
        self.graph_elem.draw_polygon(poly_dep, fill_color='#3498db', line_color='#2980b9')

        # 2. СЕТКА
        curr_y = step_y
        self.graph_elem.draw_text('0', (-self.max_x * 0.03, 0), text_location='e', font='Arial 8')  # Рисуем один ноль
        while curr_y <= self.display_max_y:
            self.graph_elem.draw_line((0, curr_y), (self.max_x, curr_y), color='#D0D0D0')
            self.graph_elem.draw_text(
                format_digit_for_graph(curr_y), (-self.max_x * 0.03, curr_y), text_location='e', font='Arial 8')
            curr_y += step_y

        x_step = max(1, math.ceil(self.max_x / 6))
        for x in range(int(x_step), int(self.max_x) + 1, int(x_step)):
            self.graph_elem.draw_line((x, 0), (x, self.display_max_y), color='#D0D0D0')
            self.graph_elem.draw_text(str(x), (x, -self.display_max_y * 0.05), font='Arial 8')

        # 3. ОСИ И НАЗВАНИЯ (Новое расположение)
        self.graph_elem.draw_line((0, 0), (0, self.display_max_y * 1.1), width=2)
        self.graph_elem.draw_line((0, 0), (self.max_x * 1.1, 0), width=2)

        # Y Слева вертикально
        self.graph_elem.draw_text('Капитал, руб.', (-self.max_x * 0.15, self.display_max_y / 2), angle=90,
                                  font='Arial 10 bold')
        # X Снизу горизонтально
        self.graph_elem.draw_text('Период инвестирования (годы)', (self.max_x / 2, -self.display_max_y * 0.1),
                                  font='Arial 10 bold')

        # 4. ЛЕГЕНДА
        lx, ly = self.max_x * 0.05, self.display_max_y * 1.05
        self.graph_elem.draw_rectangle((lx, ly + self.display_max_y * 0.05), (lx + self.max_x * 0.05, ly),
                                       fill_color='#2ecc71')
        self.graph_elem.draw_text('Доход', (lx + self.max_x * 0.06, ly + self.display_max_y * 0.025), text_location='w')
        lx2 = lx + self.max_x * 0.25
        self.graph_elem.draw_rectangle((lx2, ly + self.display_max_y * 0.05), (lx2 + self.max_x * 0.05, ly),
                                       fill_color='#3498db')
        self.graph_elem.draw_text('Внесено', (lx2 + self.max_x * 0.06, ly + self.display_max_y * 0.025),
                                  text_location='w')

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

                v_total, v_dep, v_int = self.totals[idx], self.deposits[idx], self.interests[idx]

                # Прицелы
                l1 = self.graph_elem.draw_line((idx, 0), (idx, v_total), color='gray', width=1)
                l2 = self.graph_elem.draw_line((0, v_total), (idx, v_total), color='gray', width=1)

                self.interactive_elements.extend([l1, l2])

                # МАРКЕРЫ
                if idx > 0:
                    m1 = self.graph_elem.draw_circle((idx, v_total), self.max_x * 0.005, fill_color='orange',
                                                     line_color='white')
                    m2 = self.graph_elem.draw_circle((idx, v_dep), self.max_x * 0.005, fill_color='orange',
                                                     line_color='white')

                    # ПОДПИСИ
                    offset = self.display_max_y * 0.005

                    # Доход (СВЕРХУ - text_location='s')
                    txt_int = self.graph_elem.draw_text(
                        f'Доход: {format_digit_for_graph(v_int)}', (idx, v_total + offset),
                        color='#1b5e20', font='Arial 9 bold', text_location='s')

                    # Внесено (СНИЗУ - text_location='n')
                    txt_dep = self.graph_elem.draw_text(
                        f'Внесено: {format_digit_for_graph(v_dep)}', (idx, v_dep - offset),
                        color='#0d47a1', font='Arial 9 bold', text_location='n')

                    self.interactive_elements.extend([m1, m2, txt_int, txt_dep])

                # ПОДСВЕТКА ОСЕЙ (С перекрытием старых цифр белым фоном)

                # Ось X
                bg_x = self.graph_elem.draw_rectangle(
                    (idx - 0.5, -self.display_max_y * 0.03), (idx + 0.5, -self.display_max_y * 0.07),
                    fill_color='white', line_width=0, line_color='black')
                t_x = self.graph_elem.draw_text(
                    str(idx), (idx, -self.display_max_y * 0.05), color='red', font='Arial 12 bold')

                # Ось Y
                bg_y = self.graph_elem.draw_rectangle(
                    (-self.max_x * 0.13, v_total + self.display_max_y * 0.03),
                    (-0.2, v_total - self.display_max_y * 0.03),
                    fill_color='white', line_width=0, line_color='black')
                t_y = self.graph_elem.draw_text(
                    format_digit_for_graph(v_total), (-self.max_x * 0.03, v_total),
                    color='red', font='Arial 12 bold', text_location='e')

                self.interactive_elements.extend([l1, l2, bg_x, t_x, bg_y, t_y])
