import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("The Game")
icon = pygame.image.load("robot-grab.png")
player = pygame.image.load("spaceship.png")
bulletImg = pygame.image.load("bullet.png")
background = pygame.image.load("spacebg.png")
mixer.music.load("bg.mp3")
mixer.music.play(-1)
axis_x = 370
axis_y = 480
player_key = 0
pygame.display.set_icon(icon)
enemyImg = []
enemy_x = []
enemy_y = []
enemy_xchange = []
enemy_ychange = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_xchange.append(2)
    enemy_ychange.append(40)

bullet_x = 0
bullet_y = 480
bullet_xchange = 0
bullet_ychange = 10
bullet_state = "ready"
# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over():
    score_over = game_over_font.render("Game Over ", True, (255, 57, 20))
    screen.blit(score_over, (220, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (57, 255, 20))
    screen.blit(score, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (round(x), round(y)))


def player1(x, y):
    screen.blit(player, (round(x), round(y)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (round(x + 16), round(y + 10)))


def iscollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(bullet_x - enemy_x, 2)) + (math.pow(bullet_y - enemy_y, 2)))
    if distance < 25:
        return True
    else:
        return False


run = True
while run:
    screen.fill(((0, 0, 0)))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_key = -3
            if event.key == pygame.K_RIGHT:
                player_key = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = axis_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_key = 0
    axis_x += player_key
    if axis_x <= 0:
        axis_x = 0
    if axis_x >= 736:
        axis_x = 736
    for i in range(num_of_enemies):
        if enemy_y[i] > 480:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over()
            break
        enemy_x[i] += enemy_xchange[i]
        if enemy_x[i] <= 0:
            enemy_y[i] += enemy_ychange[i]
            enemy_xchange[i] = 2
        elif enemy_x[i] >= 736:
            enemy_xchange[i] = -2
            enemy_y[i] += enemy_ychange[i]
        collision = iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_ychange

    player1(axis_x, axis_y)
    show_score(text_x, text_y)
    pygame.display.update()
