import sys
import colors
import pygame as pg
import colors
import time
from generate import*
pg.init()


COLOR_INACTIVE = colors.WHITE
COLOR_ACTIVE = colors.GREEN
FONT = pg.font.Font(None, 32)


def start_point_generate(n, m):  # точка начала - один из углов
    """Функция выбора точки начала лабиринта"""
    if random.choice([True, False]):  # тогда начинаем в
        if random.choice([True, False]):  # первой
            start = (0, 0)
        else:  # или последней строке
            start = (0, m-1)
    else:  # начинаем в столбце
        if random.choice([True, False]):
            start = (n - 1, 0)
        else:
            start = (n - 1, m - 1)
    return start  # вернули тапл


def finish_point_generate(start, n, m):  # противоп угол
    """Выбор точки конца лабиринта"""
    return n - 1 - start[0], m - 1 - start[1]


def transition_choice(x, y, rm):
    """Функция выбора дальнейшего пути в генерации лабиринта"""
    choice_list = []
    if x > 0:  # если можем двигаться назад
        if not rm[x - 1][y]:  # если не посещена
            choice_list.append((x - 1, y))
    if x < len(rm) - 1:
        if not rm[x + 1][y]:
            choice_list.append((x + 1, y))
    if y > 0:
        if not rm[x][y - 1]:
            choice_list.append((x, y - 1))
    if y < len(rm[0]) - 1:
        if not rm[x][y + 1]:
            choice_list.append((x, y + 1))
    if choice_list:  # если можем куда-то пойти
        nx, ny = random.choice(choice_list)
        if x == nx:  # если переходим по строке (х не меняется)
            if ny > y:  # если перешли вперёд
                tx, ty = x * 2, ny * 2 - 1
            else:  # перешлии назад (у меньше)
                tx, ty = x * 2, ny * 2 + 1
        else:  # переходим по столбцу
            if nx > x:  # вниз
                tx, ty = nx * 2 - 1, y * 2
            else:  # вверз
                tx, ty = nx * 2 + 1, y * 2
        return nx, ny, tx, ty  # вернули номера перехода по rm(nx, ny) и tm(tx, ty)
    else:  # иначе нам некуда идти
        return -1, -1, -1, -1


def create_labyrinth(n=20, m=20):
    """Генерация лабиринта"""
    reach_matrix = []
    for i in range(n):  # создаём матрицу достижимости ячеек
        reach_matrix.append([])
        for j in range(m):
            reach_matrix[i].append(False)
    transition_matrix = []
    for i in range(n * 2 - 1):  # заполнение матрицы переходов
        transition_matrix.append([])
        for j in range(m * 2 - 1):
            if i % 2 == 0 and j % 2 == 0:
                transition_matrix[i].append(True)
            else:
                transition_matrix[i].append(False)
    start = start_point_generate(n, m)  # выбрали точку начала
    finish = finish_point_generate(start, n, m)  # точку конца
    list_transition = [start]  # список доступных точек
    x, y = start
    reach_matrix[x][y] = True
    x, y, tx, ty = transition_choice(x, y, reach_matrix)  # выбрали куда идти
    for i in range(1, m * n):  # пока не посещены все клетки
        while not (x >= 0 and y >= 0):  # пока не можем никуда идти
            x, y = list_transition[-1]
            list_transition.pop()
            x, y, tx, ty = transition_choice(x, y, reach_matrix)
        reach_matrix[x][y] = True  # посещена
        list_transition.append((x, y))
        transition_matrix[tx][ty] = True  # там проход, не стена
        x, y, tx, ty = transition_choice(x, y, reach_matrix)
    return transition_matrix, start, finish  # возвращаем матрицу проходов и начальную точку


def draw_labyrinth(matrix, start, finish, width_line=20, width_walls=5, color_way=(255, 255, 255),
                   color_wall=(0, 0, 0),
                   border=5, color_start=(0, 0, 0), color_finish=(0, 0, 0)):
    """Рисование лабиринта"""
    # w_maze = len(matrix[0])
    # h_maze = len(matrix)
    # if w_maze >= h_maze:
    #     width = width_window
    #     height = int(float(width * (h_maze/w_maze)))
    # else:
    #     height = width_window
    #     width = int(float(height * (w_maze / h_maze)))
    width = (len(matrix) // 2 + 1) * width_line + (len(matrix) // 2) * width_walls + border * 2
    height = (len(matrix[0]) // 2 + 1) * width_line + (len(matrix[0]) // 2) * width_walls + border * 2
    surf2 = pg.Surface((width, height))
    for i in range(width):
        for j in range(height):
            if i < border or width - i <= border or j < border or height - j <= border:  # отображение границ лабиринта
                pg.draw.line(surf2, color_wall, [i, j], [i, j], 1)
            else:
                if (i - border) % (width_line + width_walls) <= width_line:
                    x = (i - border) // (width_line + width_walls) * 2
                else:
                    x = (i - border) // (width_line + width_walls) * 2 + 1
                if (j - border) % (width_line + width_walls) <= width_line:
                    y = (j - border) // (width_line + width_walls) * 2
                else:
                    y = (j - border) // (width_line + width_walls) * 2 + 1
                if matrix[x][y]:
                    pg.draw.line(surf2, color_way, [i, j], [i, j], 1)
                else:
                    pg.draw.line(surf2, color_wall, [i, j], [i, j], 1)
    place = surf2.get_rect(center=(width_window / 2, height_window / 2))
    pg.draw.rect(surf2, color_start, (  # точка начала
        border + start[0] * (width_line + width_walls), border + start[1] * (width_line + width_walls), width_line,
        width_line))
    pg.draw.rect(surf2, color_finish, (  # точка конца
        border + finish[0] * (width_line + width_walls), border + finish[1] * (width_line + width_walls), width_line,
        width_line))
    screen.blit(surf2, place)


  # def convert():


class InputBox:  # класс для ввода данных

    def __init__(self, x, y, w, h, text=''):  # x, y, w, h - координаты
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.poss = True

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):  # если кликнули на него
                # Toggle the active variable.
                if not self.active and self.poss:
                    self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            if self.poss:
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            else:
                self.color = colors.BLACK
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                    self.color = colors.BLACK
                    self.poss = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def sz_inpt():
    global width_window, height_window
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)  # height
    input_box2 = InputBox(100, 300, 140, 32)  # width
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if (not input_box1.poss and not input_box2.poss) or event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)

    return int(input_box1.text), int(input_box2.text)

#main
width_window = 800  # ширина экрана
height_window = 800  # высота экрана
SIZE = (width_window, height_window)  # размер
FPS = 60  # время
screen = pg.display.set_mode(SIZE)  # создали экран
screen.fill(colors.BLACK)  # покрасили чёрным
clock = pg.time.Clock()  # время

#кнопка start
f = pg.font.SysFont('serif', 150)
point_start = f.render("START", True, colors.WHITE)
place = point_start.get_rect(center=(width_window/2, height_window/2))
screen.blit(point_start, place)
pg.display.update()

start = False
while not start:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif i.type == pg.MOUSEBUTTONDOWN:
            if place.collidepoint(i.pos):
                start = True
    clock.tick(FPS)

# кнопки создать и загрузить
f2 = pg.font.SysFont('serif', 100)
point_generate = f2.render("generate", True, colors.WHITE)
point_upload = f2.render("upload", True, colors.WHITE)
place_gen = point_start.get_rect(center=(width_window*3/5, height_window/3))
place_upl = point_start.get_rect(center=(width_window*3/5, height_window * (2/3)))
screen.fill(colors.BLACK)
screen.blit(point_generate, place_gen)
screen.blit(point_upload, place_upl)
pg.display.update()
start = False
typ = True
while start == False:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif i.type == pg.MOUSEBUTTONDOWN:
            if place_gen.collidepoint(i.pos):  # если создаём
                start = True
            if place_upl.collidepoint(i.pos):  # если создаём
                start = True
                typ = False
    clock.tick(FPS)


width = 65 #размер лабиринта, до 65
height = 65

if typ:
    height, width = sz_inpt()  # ввели размеры
    msz = max(width, height)
    width_walls = width_window // (msz * 6)
    width_line = width_walls * 5
    border = width_walls
    matrix_base = []
    window = pg.display.set_mode((width_window, height_window))  # создали окно
    pg.display.set_caption("Лабиринт")
    font = pg.font.Font(None, 25)  # шрифт
    flag_game = True  # пока работаем
    matrix, start, finish = create_labyrinth(width, height)  # создали лабиринт
    draw_labyrinth(matrix, start, finish, width_line, width_walls, colors.WHITE,
                   colors.BLACK,
                   border)
    pg.display.update()
    while True:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                pg.quit()
                sys.exit()
        clock.tick(FPS)

  # else:  # загружаем лабиринт и разворачиваем его



