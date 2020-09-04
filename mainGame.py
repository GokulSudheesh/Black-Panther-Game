import pygame
import os
import time
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

class player(object):
    hearts = [[pygame.image.load('./Images/heart.png'), (610 - 24 -24 - 40, 5)],
             [pygame.image.load('./Images/heart.png'), (610 - 24 - 40, 5)],
             [pygame.image.load('./Images/heart.png'), (610 - 40, 5)]]
    walkLeft = [pygame.image.load('./Images/W0.png'), pygame.image.load('./Images/W1.png'),
                 pygame.image.load('./Images/W2.png'), pygame.image.load('./Images/W3.png'),
                 pygame.image.load('./Images/W4.png'), pygame.image.load('./Images/W5.png'),
                 pygame.image.load('./Images/W6.png'), pygame.image.load('./Images/W7.png'),
                 pygame.image.load('./Images/W8.png'), pygame.image.load('./Images/W9.png'),
                pygame.image.load('./Images/W10.png'),]
    walkRight = []
    for w in walkLeft:
        walkRight.append(pygame.transform.flip(w, True, False))

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Ideal velocity 5
        self.vel = 6
        # Ideal jumpVel = 15, maxJumpRange = 10
        self.jumpVel = 15
        self.maxJumpRange = 10
        self.jumpCounter = 0
        self.isJump = False
        self.falling = False
        self.currentPlatform = None
        self.left = False
        self.right = False
        self.standing = True
        self.walkCount = 0
        self.health = 10
        #self.hitBox = (self.x + 17, self.y + 11, 29, 52)
        self.hitBox = (self.x + 5, self.y, 30, 76)
    def draw(self, win):
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            else:
                win.blit(self.walkLeft[0], (self.x, self.y))
        #self.hitBox = (self.x + 17, self.y + 11, 29, 52)
        if self.right:
            self.hitBox = (self.x + 15, self.y, 30, 76)
        else:
            self.hitBox = (self.x + 5, self.y, 30, 76)
        #pygame.draw.rect(win, colors["red"], self.hitBox, 2)
        #pygame.draw.rect(win, colors["red"], (self.x, self.y, self.width, self.height), 2)
        #pygame.draw.rect(win, colors["red"], (self.hitBox[0], self.hitBox[1] - 20, 50, 10))
        #pygame.draw.rect(win, colors["green"], (self.hitBox[0], self.hitBox[1] - 20, 50 - (5 * (10 - self.health)), 10))
        pygame.draw.rect(win, colors["red"], (dispx - 60 - 20, 30, 70, 10))
        pygame.draw.rect(win, colors["green"], (dispx - 60 - 20, 30, 70 - (7 * (10 - self.health)), 10))
    def move(self, keys):
        # Moving Left
        # (x, y, w, h)
        if keys[pygame.K_a] and (self.hitBox[0] - self.vel >= 0):
            self.x -= self.vel
            self.left = True
            self.right = False
            self.standing = False
        # Moving Right
        # (x, y, w, h)
        elif keys[pygame.K_d] and (self.hitBox[0] + self.hitBox[2] + self.vel <= dispx):
            self.x += self.vel
            self.right = True
            self.left = False
            self.standing = False

        else:
            self.standing = True
            self.walkCount = 0
        if keys[pygame.K_SPACE] and not self.isJump and not self.falling:
            '''if keys[pygame.K_w] and (self.y - self.vel >= 0):
                self.y -= self.vel
            if keys[pygame.K_s] and (self.y + self.height + self.vel <= dispy):
                self.y += self.vel'''
            self.isJump = True
            self.jumpCounter = 0
            self.right = False
            self.left = False
            self.walkCount = 0
        if self.currentPlatform:
            if not self.currentPlatform.checkCollision(self):
                self.falling = True
                self.currentPlatform = None

        if self.isJump:
            self.y -= self.jumpVel
            self.jumpCounter += 1
            if self.jumpCounter == self.maxJumpRange:
                self.isJump = False
                self.falling = True
        elif self.falling:  # and not self.currentPlatform:
            self.y += self.jumpVel
    def hit(self):
        if self.health > 0:
            self.health -= 0.1
        elif self.health <= 0 and len(self.hearts) != 1:
            self.hearts.pop()
            self.x = 600
            self.y = 322
            #self.x = 654
            #self.y = 224
            self.walkCount = 0
            self.jumpCounter = 0
            self.isJump = False
            self.falling = False
            self.currentPlatform = None
            font1 = pygame.font.SysFont('LCD Solid', 30)
            text = font1.render('Respawning in 3 seconds...', 1, colors["white"])
            win.blit(text, (dispx/2 - (text.get_width()/2), dispy/2))
            pygame.display.update()
            pygame.time.delay(3000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.health = 10
            '''i = 0
            while i < 300:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()'''
        else:
            print ("Game Over")
            done = True
            font1 = pygame.font.SysFont('LCD Solid', 30)
            text = font1.render('Legends never die. Try again.', 1, colors["white"])
            win.blit(text, (dispx / 2 - (text.get_width() / 2), dispy / 2))
            pygame.display.update()
            while done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                '''keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    done = False
                    startGame()'''

class enemy(object):
    walkRight = [pygame.image.load('./Images/WRE1.png'), pygame.image.load('./Images/WRE2.png'),
                 pygame.image.load('./Images/WRE3.png'), pygame.image.load('./Images/WRE4.png'),
                 pygame.image.load('./Images/WRE5.png'), pygame.image.load('./Images/WRE6.png'),
                 pygame.image.load('./Images/WRE7.png'), pygame.image.load('./Images/WRE8.png'),
                 pygame.image.load('./Images/WRE9.png'), pygame.image.load('./Images/WRE10.png')]
    walkLeft = [pygame.image.load('./Images/WLE1.png'), pygame.image.load('./Images/WLE2.png'),
                pygame.image.load('./Images/WLE3.png'), pygame.image.load('./Images/WLE4.png'),
                pygame.image.load('./Images/WLE5.png'), pygame.image.load('./Images/WLE6.png'),
                pygame.image.load('./Images/WLE7.png'), pygame.image.load('./Images/WLE8.png'),
                pygame.image.load('./Images/WLE9.png'), pygame.image.load('./Images/WLE10.png')]
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = x
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.right = True
        self.left = False
        self.isChase = False
        self.isAttack = False
        self.vel = 3
        self.hitBox = (self.x + 17, self.y + 2, 31, 58)
        self.health = 10
        self.isAlive = True

    def draw(self, win):
        if self.isAlive:
            self.move()
            if self.walkCount + 1 >= 30:
                self.walkCount = 0
            if self.right:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            if self.right:
                self.hitBox = (self.x + 17, self.y + 2, 31, 58)
            else:
                self.hitBox = (self.x + 49, self.y + 2, 31, 58)
            # Health Bar:
            pygame.draw.rect(win, colors["red"], (self.hitBox[0], self.hitBox[1] -20, 50, 10))
            pygame.draw.rect(win, colors["green"], (self.hitBox[0], self.hitBox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            #pygame.draw.rect(win, colors["red"], self.hitBox, 2)
            #pygame.draw.rect(win, colors["red"], (self.x, self.y, self.width, self.height), 2)
    def move(self):
        if not self.isChase:
            self.path[0] = self.start
            self.path[1] = self.end
        if self.right: # Going right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.right = False
                self.left = True
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x -= self.vel
            else:
                self.right = True
                self.left = False
                self.walkCount = 0
    def chase(self, player):
        # If the enemy is on the same y level as the player
        if self.y == player.y + 18:
            self.isChase = True
        else:
            self.isChase = False
        if self.isChase:
            # If player is to the left of the enemy
            if player.x < enemy.x:
                self.left = True
                self.right = False
                self.path[0] = player.x
            # If player is to the right of the enemy
            if player.x > self.x:
                self.right = True
                self.left = False
                self.path[1] = player.x
            else:
                self.right = False
                self.left = True
    def hit(self):
        if self.health > 0:
            self.health -= 2
        else:
            self.isAlive = False
        #print("Hit")


class projectile(object):
    knifeR = pygame.image.load('./Images/knife.png')
    knifeL = pygame.transform.flip(knifeR, True, False)
    def __init__(self, x, y, color, facing):
        self.x = x
        self.y = y
        self.height = 32
        self.width = 32
        #self.radius = radius
        self.color = color
        self.facing = facing # Either 1 or -1
        self.vel = 15 * facing
    def draw(self, win):
        #pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        # if the player is looking left:
        if self.facing == 1:
            win.blit(self.knifeR, (self.x, self.y))
        else:
            win.blit(self.knifeL, (self.x, self.y))
class platform(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.box = (x, y, w, h)
    def checkCollision(self, player):
        # If the player is not on the platform
        if player.hitBox[0] + player.hitBox[2] < self.x or player.hitBox[0] > self.x + self.w:# + player.hitBox[2] > self.x + self.w:
            return None
        # If the player is on the platform
        if player.y + player.height <= self.y and player.y + player.height + player.jumpVel >= self.y:
            return self
        return None
class platforms(object):
    def __init__(self):
        self.platformLst = []
    def add(self, x, y,w ,h):
        p = platform(x, y, w, h)
        self.platformLst.append(p)
    def draw(self):
        for platform in self.platformLst:
            pygame.draw.rect(win, colors["red"], platform.box, 2)
    def checkCollisions(self, player):
        if not player.falling:
            return False
        for platform in self.platformLst:
            activePlat = platform.checkCollision(player)
            if activePlat:
                player.currentPlatform = activePlat
                player.y = activePlat.y - player.height
                player.falling = False
                return True
        return False
    def get(self, index):
        return self.platformLst[index]


def reDrawGameWindow():
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
    #plats.draw()
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
                    player.hit()
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
        reDrawGameWindow()
def gameStartup():
    endingMusic = pygame.mixer.music.load ("./Sound/All The Stars.mp3")
    pygame.mixer.music.play(-1)
    #pygame.mixer.music.stop()
    win = pygame.display.set_mode((1000, 700))
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