
import math
import random
import pygame
# initialise pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((900,600))


# background
bg = pygame.image.load('assets/bg.jpg')



# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('assets/ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('assets/space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

#  enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

no_of_enemies = 3

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('assets/alien.png'))
    enemyX.append(random.randint(0, 835))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.2)
    enemyY_change.append(60)


# bullets
bulletImg = pygame.image.load('assets/asteroid.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.3
# ready : cannot see the bullet
# fire : bullet is moving
bullet_state = 'ready'


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# game over text
over_text = pygame.font.Font('freesansbold.ttf',32)

def show_score(x,y):
    score = font.render('Score :' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_text(x,y):
    over_text = over_text.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (300,250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(bg, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check wheather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.2
            
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change


    # checking boundries of spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        playerX = 836

    # Enemy Movement
    for i in range(no_of_enemies):

        # gameover
        if enemyY[i] > 450:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text(345,430)
            
        

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 836:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
    
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50,150)
        
        
        enemy(enemyX[i], enemyY[i], i)



    # bullet movment
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    show_score(textX,textY)
    pygame.display.update()