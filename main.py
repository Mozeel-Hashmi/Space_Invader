import pygame
import random as rd
import math #For distance formuale
from pygame import mixer #For music related stuff

#Initializing Pygame
pygame.init()

#Making a screen
screen = pygame.display.set_mode((800,600))

#Background
bg = pygame.image.load('background.png')

#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1) #For looping the music we have to put -1

# Making title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


#Player
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_Change = 0
def player(x, y):
    screen.blit(playerimg, (x, y))

#Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(rd.randint(0, 730))
    enemyY.append(rd.randint(50, 150))
    enemyX_Change.append(4)
    enemyY_Change.append(40)
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

#Bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 10
bullet_state = "ready"
def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

#For collision detection
def isCollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance < 27:
        return True
    else:
        return False

#Creating a GameLoop
running = True
while running:
    # Changing the screen color
    screen.fill((0, 0, 0))

    #Background
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Checking KeyStrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -5
            if event.key == pygame.K_RIGHT:
                playerX_Change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0
        
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    
    if bullet_state is "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_Change

    playerX += playerX_Change
    if playerX < 0:
        playerX = 0
    elif playerX > 730:
        playerX = 730
    player(playerX, playerY)
    
    for i in range(no_of_enemies):
        #Gameover 
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_Change[i]
        if enemyX[i] < 0:
            enemyX_Change[i] = 4
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] > 730:
            enemyX_Change[i] = -4
            enemyY[i] += enemyY_Change[i]

    
    
        #Collision
        collision = isCollision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = rd.randint(0, 730)
            enemyY[i] = rd.randint(50, 150)
            score_value += 1
        enemy(enemyX[i], enemyY[i], i)
    show_score(textX, textY)

    #Updating the screen
    pygame.display.update()