import pygame
import os
import time
from sprites import *
pygame.init()

colors = {"black": (0, 0, 0), "white": (255, 255, 255), "gray": (217, 217, 217),
          "litegray": (245, 235, 255), "litebrown": (245, 222, 179), "red": (255, 0, 0),
          "yellow": (255, 255, 55), "green": (0, 255, 0), "lime_green": (50, 205, 50)}
#dispx, dispy = 500, 480
dispx, dispy = 693, 526
win = pygame.display.set_mode((dispx, dispy))

pygame.display.set_caption("Wakanda 4ever")

# Make sure file format is always .ogg Convert here- https://www.media.io/
hitSound = pygame.mixer.Sound('./Sound/hit.ogg')

bg = pygame.image.load('./Images/bg.png')
#char = pygame.image.load('./Images/standing.png')

clock = pygame.time.Clock()
fps = 30
score = 0
mute = False
newGame = True
font = pygame.font.SysFont('LCD Solid', 15, True, False) #(Font, size, Bold, Itallic)

def drawGameWindow():
    win.blit(bg, (0,0))
    text = font.render("Score: " + str(score), 1, colors["white"])
    win.blit(text, (dispx - text.get_width(), 10))
    for heart in player.hearts:
        win.blit(heart[0], heart[1])
    player.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    #plats.draw(win)
    if newGame:
        introPic = pygame.image.load("./Images/BP_onScreen.png")
        pygame.draw.rect(win, colors["black"], (0, dispy - 81, 693, 200))
        font3 = pygame.font.SysFont('LCD Solid', 30, False, False)  # (Font, size, Bold, Itallic)
        font4 = pygame.font.SysFont('LCD Solid', 15, True, False)  # (Font, size, Bold, Itallic)
        text2 = font3.render("Wakanda Forever!", 1, colors["white"])
        text3 = font4.render("Continue --->", 1, colors["white"])
        win.blit(text2, (210, dispy - 70))
        win.blit(text3, (350, dispy - 30))
        win.blit(introPic, (0, dispy - 81))

    #pygame.draw.rect(win, colors["red"], (0, 390, 693, 20), 2)
    #pygame.draw.rect(win, colors["red"], (0, 397, 693, 20), 2)
    #pygame.draw.rect(win, colors["red"], (0, 247, 186, 50), 2)
    #pygame.draw.rect(win, colors["red"], (282, 187, 107, 50), 2)
    pygame.display.update()


def startGame():
    global plats, player, enemies, enemy, bullets, score, projectile, newGame
    win = pygame.display.set_mode((dispx, dispy))
    plats = platforms()
    plats.add(0, 398, 693, 20)
    plats.add(0, 248, 186, 50)
    plats.add(577, 300, 186, 50)
    plats.add(260, 188, 125, 50)
    # Note that the player is off by 18 pixels compared to the enemy
    #player = player(600, 322, 50, 76)
    player = player(654, 224, 50, 76)
    # Initialize the starting platform
    player.currentPlatform = plats.get(2)
    enemies = []
    enemies.append(enemy(0, 340, 97, 64, 600))
    enemies.append(enemy(100, 340, 97, 64, 350))
    enemies.append(enemy(0, 190, 97, 64, 150))

    bullets = []
    run = True
    # Firing bullets one at a time
    bulletCooldown = 0
    while run:
        # Frames
        clock.tick(fps)

        if bulletCooldown > 0:
            bulletCooldown += 1
        if bulletCooldown > 3:
            bulletCooldown = 0
        # Taking hit from enemies
        for enemy in enemies:
            if player.hitBox[1] < enemy.hitBox[1] + enemy.hitBox[3] and player.hitBox[1] + player.hitBox[3] > enemy.hitBox[1]:
                if player.hitBox[0] < enemy.hitBox[0] + enemy.hitBox[2] and player.hitBox[0] + player.hitBox[2] > enemy.hitBox[0]:
                    player.hit(win)
                    score -= 1
                    if score < 0:
                        score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #Shooting bullets
        for bullet in bullets:
            if bullet.x < dispx and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                # Removing the bullet if it goes out of the map
                bullets.pop(bullets.index(bullet))
        # Shooting bullets at the enemies
        for enemy in enemies:
            if enemy.isAlive:
                for bullet in bullets:
                    if round(bullet.y + bullet.height//2) < enemy.hitBox[1] + enemy.hitBox[3] and round(bullet.y + bullet.height//2) > enemy.hitBox[1]:
                        if round(bullet.x + bullet.width//2) < enemy.hitBox[0] + enemy.hitBox[2] and round(bullet.x + bullet.width//2) > enemy.hitBox[0]:
                            enemy.hit()
                            if not mute:
                                hitSound.play()
                            bullets.pop(bullets.index(bullet))
                            score += 1
            else:
                enemies.pop(enemies.index(enemy))

        keys = pygame.key.get_pressed()
        leftClick, scroll, rightClick = pygame.mouse.get_pressed()
        # Shooting bullet
        if leftClick and bulletCooldown == 0:
            newGame = False
            facing = -1
            if player.right:
                facing = 1
            if len(bullets) < 5:
                bullets.append(projectile(round(player.x + player.width//2), round(player.y + player.height//2 - 10), colors["red"], facing))
            bulletCooldown = 1
        player.move(keys)
        plats.checkCollisions(player)
        # Enemy chasing the player
        for enemy in enemies:
            enemy.chase(player)
        '''if len(enemies) == 0:
            print("You won")
            #run = False
            #ending()'''
        drawGameWindow()
def gameStartup():
    endingMusic = pygame.mixer.music.load ("./Sound/All The Stars.mp3")

    #pygame.mixer.music.stop()
    win = pygame.display.set_mode((1000, 700))
    pygame.mixer.music.play(-1)
    win.fill(colors["black"])
    dir = './Images/Ending-Frames/'
    ending_frames = []
    for dir, f, img in os.walk(dir):
        for image in img:
            img_path = os.path.join(dir, image)
            ending_frames.append(pygame.image.load(img_path))
    #print(len(ending_frames))
    introRun = True
    while introRun:
        #clock.tick(0.25)
        count = 0
        for frame in ending_frames:
            clock.tick(30)
            font3 = pygame.font.SysFont('LCD Solid', 30, False, False)  # (Font, size, Bold, Itallic)
            text1 = font3.render("Press C to start", 1, colors["white"])
            text2 = font3.render("Press C to start", 1, colors["black"])
            if count % 20 == 0:
                win.blit(text1, (1000 / 2 - (text1.get_width() / 2), 650))
            else:
                win.blit(text2, (1000 / 2 - (text2.get_width() / 2), 650))
            count += 1
            win.blit(frame, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    introRun = False
                    pygame.mixer.music.stop()
                    pygame.quit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    introRun = False
                    pygame.mixer.music.stop()
                    startGame()
            #time.sleep(0.25)
            pygame.display.update()
        count = 0

#startGame()
gameStartup()
pygame.quit()
