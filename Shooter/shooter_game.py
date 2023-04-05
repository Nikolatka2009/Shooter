#Создай собственный Шутер!

from pygame import *
from random import *
from time import sleep


#Создание экрана, фона и подключение музыки
window = display.set_mode((700, 500))
display.set_caption("Space")
background = transform.scale(image.load('fon1.jpg'), (700, 500))
FPS = 60
clock = time.Clock()
game = True
lost = 0
score = 0
k = 0
l = 0 

mixer.init()
mixer.music.load("soundtrack.mp3")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#установка шрифтов для надписей
font.init()
font1 = font.SysFont('Impact', 36)
font2 = font.SysFont('Impact', 24)

###########################################

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): #класс управляемого игрока
    def update(self):
        keys = key.get_pressed() #все нажатые клавиши
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 390 :
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('vrag2.png', self.rect.centerx, self.rect.top, 30, 40, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.rect.x += randint(-30, 30)
        global lost
        if self.rect.y > 600:
            self.rect.y = randint(-30, 0)
            self.rect.x = randint(30, 750)
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.rect.x += randint(-30, 30)
        if self.rect.y > 600:
            self.rect.y = randint(-30, 0)
            self.rect.x = randint(30, 750)
##################################################

#создание объектов
ship = Player("mario.png", 300, 380, 80, 100, 4)
enemies = sprite.Group() #группа спрайтов

for i in range(int(input("Сколько врагов вы хотите?"))):
    enemy = Enemy("vrag.png", randint(30, 750), randint(-30, 0), 64, 40, randint(1, 5))
    enemies.add(enemy)

asteroids = sprite.Group()
for i in range(int(input("Сколько дополнительных врагов вы хотите?"))):
    asteroid = Asteroid("vrag3.png", randint(30, 670), -40, 56, 49, randint(5, 10))
    asteroids.add(asteroid)

bullets = sprite.Group() #группа пуль


#игровой цикл
while game:
    for ev in event.get():
        if ev.type  == QUIT:
            game = False

        if ev.type == KEYDOWN: #выстрел по нажатию на пробел
            if ev.key == K_SPACE:
                ship.fire()
                fire_sound.play()
            
    window.blit(background, (0, 0))
    ship.update()
    enemies.update()
    bullets.update()
    asteroids.update()

    ship.reset()
    enemies.draw(window)
    bullets.draw(window)
    asteroids.draw(window)

    if sprite.spritecollide(ship, enemies, False) or lost > 9 or sprite.spritecollide(ship, asteroids, False):
        lost = 0
        score = 0
        k = 1

    if k == 1:
        text_lose = font1.render('Wasted', 1, (250, 0, 0))
        window.blit(text_lose, (300, 150))
        text_pause = font2.render('Please, hold space', 1, (250, 0, 0))
        window.blit(text_pause, (270, 200))

    if ev.type == KEYDOWN: #выстрел по нажатию на пробел
        if ev.key == K_SPACE:
            k = 0
            l = 0

    if score > 9:
        lost = 0
        score = 0
        l = 1
        text_win = font1.render('Complete', 1, (0, 250, 0))
        window.blit(text_win, (300, 150))

    if l == 1:
        text_win = font1.render('Complete', 1, (0, 250, 0))
        window.blit(text_win, (300, 150))
        text_pause = font2.render('Please, hold space', 1, (0, 250, 0))
        window.blit(text_pause, (270, 200))


    text_lost = font1.render(
        'Пропущено:' + str(lost), 1, (239, 239, 0)
    )
    text_score = font1.render(
        'Сбито:' + str(score), 1, (239, 239, 0)
    )
    window.blit(text_lost, (10, 40))
    window.blit(text_score, (10, 10))
    


    collides = sprite.groupcollide(enemies, bullets, True, True)
    for c in collides:
        enemy = Enemy("vrag.png", randint(30, 750), randint(-30, 0), 64, 40, randint(1, 5))
        enemies.add(enemy)
        score += 1

    collides1 = sprite.groupcollide(asteroids, bullets, True, True)
    for s in collides1:
        asteroid = Asteroid("vrag3.png", randint(30, 670), -40, 56, 49, randint(5, 10))
        asteroids.add(asteroid)

    display.update()
    clock.tick(FPS)




