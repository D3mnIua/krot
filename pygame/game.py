import pygame
import time
from random import randint
import pygame.mixer

pygame.init()
pygame.mixer.init()

# Функція, яка створює вікно з кнопкою "Почати гру"
def start_game_screen():
    screen = pygame.display.set_mode((500, 360))
    screen.fill((0, 128, 0))  # Зелений колір фону вікна
    font = pygame.font.SysFont('Italic', 50)
    font3 = pygame.font.SysFont('Italic', 50)
    font2 = pygame.font.SysFont('Courier', 45)
    text = font.render('Почати гру', True, (0, 0, 0))  # Чорний текст кнопки
    text2 = font2.render('Знайди крота', True, (0, 0, 0))  # Чорний текст кнопки
    text3 = font3.render('Закінчити гру', True, (0, 0, 0))
    text_rect = text.get_rect(center=(250, 180))
    text_rect2 = text2.get_rect(center=(252, 45))
    text_rect3 = text3.get_rect(center=(250, 240))
    screen.blit(text3, text_rect3)
    screen.blit(text2, text_rect2)
    screen.blit(text, text_rect)
    pygame.display.update()
    return screen

mw = start_game_screen()
pygame.display.set_caption("Гра 'Знайди крота'")  # Назва вікна

clock = pygame.time.Clock()


waiting_for_start = True
while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if 200 <= x <= 300 and 150 <= y <= 210:  # Перевірка, чи було клікнуто на кнопку
                waiting_for_start = False

# Початок гри
back = pygame.image.load('Picture/Dirt.jpg')
mw.blit(back, (0, 0))


pygame.display.update()

clock = pygame.time.Clock()
# музика
pygame.mixer.music.load("Sound/Fon_music_krotgame.mp3")

pygame.mixer.music.play(-1)

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def outline(self, frame_color, thickness):
        pygame.draw.rect(mw, frame_color, self.rect, thickness)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(str(text), True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


Dark = (0, 0, 0)
DARK_BLUE = (0, 0, 100)
Brown = (75, 40, 25)
GREEN = (25, 90, 5)
Dark_brown = (50, 15, 1)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
Light_green = (40, 170, 5)

cards = []
num_cards = 3
x = 108
Krot_photo = pygame.image.load("Picture/Krot.jfif")
for i in range(num_cards):
    new_card = Label(x, 150, 80, 90, Dark)
    new_card.outline(Brown, 15)
    new_card.set_text("", 5)
    cards.append(new_card)
    x += 100

wait = 0
start_time = time.time()
cur_time = start_time

Krot_govorit = Label(0, 310, 600, 70, Light_green)
Krot_govorit.set_text("Крот:", 30)
font = pygame.font.SysFont('Italic', 50)
Krot_govorit2 = Label(100, 315, 390, 70, Light_green)
Krot_govorit2.set_text("Ха-ха, спробуй спіймай мене", 26)
Tip = Label(77, 0, 346, 70, Light_green)
Tip.set_text("Знайди крота в норі!", 30)
timer_text = Label(0, 0, 77, 70, Light_green)
timer_text.set_text("Час:", 25)
timer = Label(25, 25, 0, 0, Light_green)
timer.set_text("0", 40)
score_text = Label(416, 0, 83, 70, Light_green)
score_text.set_text("Score:", 25)
score = Label(450, 25, 0, 0, Light_green)
score.set_text("0", 40)
points = 0
wrong_points = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                if cards[i].collidepoint(x, y):
                    if i + 1 == click:
                        cards[i].color(GREEN)
                        points += 1
                    else:
                        cards[i].color(RED)
                        points -= 1
                        wrong_points += 1
                    score.set_text(str(points), 40)
                    score.draw(0, 0)
                    cards[i].fill()

    if wait == 0:
        wait = 20
        click = randint(2, num_cards)
        for i in range(num_cards):
            cards[i].color(Dark)
            if (i + 1) == click:
                cards[i].draw(12, 40)
            else:
                cards[i].fill()
    else:
        wait -= 1

    new_time = time.time()
    if int(new_time) - int(cur_time) == 1:
        timer.set_text(int(new_time - start_time), 40)
        timer.draw(0, 0)
        cur_time = new_time

    if new_time - start_time >= 20 or points < -3 or points >= 3:
        running = False

    mw.blit(back, (0, 0))  # Оновлення фону перед виведенням нових елементів
    Krot_govorit.draw(0, 0)
    Krot_govorit2.draw(0, 0)
    Tip.draw(0, 0)
    timer_text.draw(0, 0)
    timer.draw(0, 0)
    score_text.draw(0, 0)
    score.draw(0, 0)
    for card in cards:
        card.fill()
    pygame.display.update()
    clock.tick(40)

if points < -3 or new_time - start_time >= 20:
    wrong_sound = pygame.mixer.Sound("Sound/Wrong_answer.mp3")
    you_lose = Label(0, 0, 500, 500, RED)
    you_lose.set_text("Крот зарився!", 45)
    you_lose.draw(100, 140)
elif points >= 3:
    win = Label(0, 0, 500, 500, GREEN)
    correct_sound = pygame.mixer.Sound("Sound/Correct_answer.mp3")
    win.set_text("Ти переміг!", 50)
    win.draw(100, 100)
    result_time = Label(0, 250, 0, 0, GREEN)
    result_time.set_text("Час проходження: " + str(int(new_time - start_time)) + " секунд", 25)
    result_points = Label(0, 220, 240, 240, GREEN)
    result_points.set_text("Невірних нажать: " + str(wrong_points), 25)
    result_points.draw(107, 0)
    result_time.draw(67, 0)


pygame.display.update()
time.sleep(3)  # Затримка закриття програми на 3 секунди
pygame.quit()
