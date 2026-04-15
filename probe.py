import PySimpleGUI as sg

from core.utilites import format_digit_for_graph


class InvestmentChart:
    def __init__(self, graph_key='-G-'):
        self.graph_key = graph_key
        self.marker_total = None  # Маркер для общего капитала
        self.marker_dep = None  # Маркер для суммы взносов
        self.info_text = None
        self.info_text_dep = None
        self.totals = []
        self.deposits = []
        self.max_x = 0
        self.max_y = 0

    def draw(self, graph_elem, data):
        years, self.deposits, interest = data
        self.totals = [d + i for d, i in zip(self.deposits, interest)]
        self.max_x, self.max_y = max(years), max(self.totals)

        # Логика выбора "красивого" шага для оси Y
        if self.max_y <= 1_000_000:
            step_y = 50_000
        elif self.max_y <= 10_000_000:
            step_y = 500_000
        else:
            step_y = 1_000_000  # Для сумм свыше 10 млн

        # Подправляем max_y в координатах, чтобы верхняя линия сетки вписалась
        display_max_y = ((self.max_y // step_y) + 1) * step_y

        offset_x, offset_y = self.max_x * 0.15, display_max_y * 0.15
        graph_elem.change_coordinates((-offset_x, -offset_y),
                                      (self.max_x * 1.15, display_max_y * 1.2))
        graph_elem.erase()

        # 1. СЛОИ (Заливка)
        poly_total = [(0, 0)] + [(years[i], self.totals[i]) for i in range(len(years))] + [(self.max_x, 0)]
        graph_elem.draw_polygon(poly_total, fill_color='#2ecc71', line_color='#27ae60')
        poly_dep = [(0, 0)] + [(years[i], self.deposits[i]) for i in range(len(years))] + [(self.max_x, 0)]
        graph_elem.draw_polygon(poly_dep, fill_color='#3498db', line_color='#2980b9')

        # 2. СЕТКА С ОКРУГЛЕНИЕМ
        # Рисуем горизонтальные линии с выбранным шагом до тех пор, пока не покроем максимум
        current_y = 0
        while current_y <= display_max_y:
            graph_elem.draw_line((0, current_y), (self.max_x, current_y), color='#D0D0D0')
            graph_elem.draw_text(f'{format_digit_for_graph(current_y)}', (-self.max_x * 0.02, current_y),
                                 text_location='e',
                                 font='Arial 8')
            current_y += step_y

        # Сетка лет (не более 7 значений)
        import math
        x_step = max(1, math.ceil(self.max_x / 6))

        for x in range(0, int(self.max_x) + 1, int(x_step)):
            graph_elem.draw_line((x, 0), (x, display_max_y), color='#D0D0D0')
            graph_elem.draw_text(x, (x, -display_max_y * 0.05), font='Arial 8')

        # 3. ОСИ
        graph_elem.draw_line((0, 0), (0, display_max_y * 1.15), width=2)
        graph_elem.draw_line((0, 0), (self.max_x * 1.1, 0), width=2)
        graph_elem.draw_text('Капитал', (0, display_max_y * 1.18), font='Arial 9 bold')
        graph_elem.draw_text('Годы', (self.max_x * 1.1, -display_max_y * 0.05), font='Arial 9 bold')

    def update_cursor(self, graph_elem, mouse_coords):
        if mouse_coords is None:
            return
        mx, my = mouse_coords

        if 0 <= mx <= self.max_x:
            idx = int(round(mx))
            if 0 <= idx < len(self.totals):
                val_total = self.totals[idx]
                val_dep = self.deposits[idx]

                # Удаляем старые маркеры и текст
                for item in [self.marker_total, self.marker_dep, self.info_text, self.info_text_dep]:
                    if item:
                        graph_elem.delete_figure(item)

                # Рисуем кружок на общем капитале (верхний слой)
                self.marker_total = graph_elem.draw_circle((idx, val_total), self.max_x * 0.015,
                                                           fill_color='orange', line_color='white')
                # Текст подсказки (с информацией по обоим значениям)
                self.info_text = graph_elem.draw_text(format_digit_for_graph(val_total),
                                                      (idx, val_total + self.max_y * 0.08),
                                                      color='black', font='Arial 9 bold', text_location='s'
                                                      )

                # Рисуем кружок на взносах (синий слой)
                self.marker_dep = graph_elem.draw_circle((idx, val_dep), self.max_x * 0.015,
                                                         fill_color='orange', line_color='white')
                # Текст подсказки (с информацией по обоим значениям)
                self.info_text_dep = graph_elem.draw_text(format_digit_for_graph(val_dep),
                                                          (idx, val_dep - self.max_y * 0.05),
                                                          color='black', font='Arial 9 bold', text_location='n'
                                                          )


def main():
    # data = [
    #     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    #     [15000, 195000, 375000, 555000, 735000, 915000, 1095000,
    #      1275000, 1455000, 1635000, 1815000, 1995000, 2175000,
    #      2355000, 2535000, 2700000],
    #     [0, 15369, 62409, 146133, 272526, 448424, 682098, 982581,
    #      1360806, 1829173, 2402873, 3098270, 3935304, 4936518,
    #      6129712, 7544601]
    # ]

    data = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [15000, 195000, 375000, 555000, 735000, 915000, 1095000, 1275000, 1455000, 1635000, 1800000],
            [0, 15369, 62409, 146133, 272526, 448424, 682098, 982581, 1360806, 1829173, 2402873]]

    layout = [[sg.Graph(canvas_size=(800, 700), graph_bottom_left=(0, 0), graph_top_right=(1, 1),
                        key='-G-', background_color='white',
                        enable_events=True, drag_submits=True, motion_events=True)]]

    window = sg.Window('Investment Analysis', layout, finalize=True)
    chart = InvestmentChart()
    chart.draw(window['-G-'], data)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'): break

        if event.startswith('-G-'):
            chart.update_cursor(window['-G-'], values['-G-'])

    window.close()


if __name__ == '__main__':
    main()
