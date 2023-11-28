import pygame
from pygame.locals import *
import time
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Initialize pygame
pygame.init()

#Regulate frame speed
fpsClock = pygame.time.Clock()
fps = 60

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PITFALL!")

slide = 0
font = pygame.font.SysFont('Javanese', 60)
donefont = pygame.font.SysFont('Javanese', 200)
score = 2000
above = 1
below = 0
background = (48,111,21)
heart = pygame.image.load('images/heart.png')
ladderimg = pygame.image.load('images/ladder.png')
laddercrop = pygame.image.load('images/laddercrop.png')
wallimg = pygame.image.load('images/wall.jpg')
background = pygame.image.load('images/background.jpg')
starry_night = pygame.image.load('images/starry_night.jpg')
mona_lisa = pygame.image.load('images/mona_lisa.jpg')
scream = pygame.image.load('images/scream.jpg')
paintings = [starry_night, mona_lisa, scream]


def write(text, font, color, x, y):
    img = font.render(str(text), True, color)
    screen.blit(img, (x,y))

class Person:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(x, y, 20, 40)
        self.speed = 4
        self.up = 0
        self.jump = 0
        self.falling = 0
        self.laddering = 0
        self.margladdering = 0
        self.farright = 0
        self.farleft = 0
        self.onfloor = 0
        self.swinging = 0
        self.lives = 3
        self.pickup = 0
    
    def draw(self):
        pygame.draw.rect(screen, (255,255,255), self.rect)
    
    def move(self):
        print(pit2.swingtip.x)
        key = pygame.key.get_pressed()
        for ladder in pits[slide].ladders:
            if self.rect.x > ladder.x - 20 and self.rect.x < ladder.x +20 and self.rect.y >= pits[slide].rect.y - 50 and self.rect.y < pits[slide].rect.y + 75:
                self.rect.x = ladder.x+5
                if key[pygame.K_UP]:
                    self.rect.y -= self.speed/3
                    self.laddering = 1
                if key[pygame.K_DOWN]:
                    self.rect.y += self.speed/3
                    self.laddering = 1
                #if key[pygame.K_RIGHT] and self.rect.y 
                self.laddering = 1
            else:
                self.laddering = 0
            if self.rect.x > ladder.x - 20 and self.rect.x < ladder.x +20 and self.rect.y < pits[slide].rect.y + 75:
                self.margladdering = 1
            else:
                self.margladdering = 0


        if pits[slide].swing == True or pits[slide].swing == 1:
            if self.rect.colliderect(pits[slide].swingtip):
                if key[pygame.K_x]:
                    self.rect.x = pits[slide].swingtip.x
                    self.rect.y = pits[slide].swingtip.y
                    self.swinging = 1
                    self.up = 0
                else:
                    self.rect.y += 4
                    self.falling = 1
                    self.swinging = 0

        if key[pygame.K_c]:
            self.pickup = 1
        else:
            self.pickup = 0

        for floor in floors[slide].rects:
            if self.rect.colliderect(floor) and self.rect.y <= floor.y + 50 and self.rect.y >= floor.y - 30:
                if self.rect.x > floor.x:
                    self.rect.x = floor.right + 2
                else:
                    self.rect.x = floor.left - 22
                self.up = 0
                self.falling = 1
        if key[pygame.K_LEFT] and self.falling == 0 and self.laddering == 0 and self.farleft == 0 and self.swinging == 0:
            if pits[slide].walls:
                for wall in pits[slide].walls:
                    if self.rect.colliderect(wall) and self.rect.left > wall.x:
                        None
                    else:
                        self.rect.x -= self.speed
                        self.farleft = 0
            else:
                self.rect.x -= self.speed
                self.farleft = 0

        elif key[pygame.K_RIGHT] and self.falling == 0 and self.laddering == 0 and self.farright == 0 and self.swinging == 0:
            if pits[slide].walls:
                for wall in pits[slide].walls:
                    if self.rect.colliderect(wall) and self.rect.left < wall.x:
                        None
                    else:
                        self.rect.x += self.speed
                        self.farright = 0
            else:
                self.rect.x += self.speed
                self.farright = 0

        if key[pygame.K_UP] == True and self.laddering == 0 and self.falling == 0:
            self.up = 1
        if self.up == 1 and self.jump < 19:
            self.rect.y -= self.speed/1.5
            self.jump += 1
        elif self.up == 1 and self.jump >= 19:
            self.rect.y += self.speed/1.5
            self.jump += 1
        for floor in floors[slide].rects:
            if self.rect.colliderect(pits[slide].bottom) or self.rect.colliderect(floor) or self.laddering == 1:
                self.jump = 0
                self.up = 0
        

        for floor in floors[slide].rects:
            if self.rect.colliderect(floor):
                self.onfloor = 1

        if self.rect.colliderect(pits[slide].bottom) or self.up == 1 or self.onfloor == 1:
            self.falling = 0
        else:
            if self.margladdering == 0 and self.swinging == 0:
                self.falling = 1
                self.rect.y += self.speed/2

        self.onfloor = 0

        if pits[slide].swing == True or pits[slide].swing == 1:
            if self.rect.y >= pits[slide].fallscreen.y+self.speed:
                self.lives -= 1
                time.sleep(2)
                self.rect.x = 100
                self.rect.y = 275


class Floor:
    def __init__(self, rects):
        self.rects = rects
    
    def draw(self):
        for rect in self.rects:
            pygame.draw.rect(screen, (166,139,113), rect)


class Pit:
    def __init__(self, ladders, walls, ifswing, x, y):
        self.ladders = ladders
        self.walls = walls
        self.swing = ifswing
        self.rect = Rect(x, y, 1000, 140)
        self.bottom = Rect(x, y+140, 1000, 20)
        self.ropelen = 200
        self.speed = 2
        self.xspeed = self.speed
        self.yspeed = self.speed
        self.sqrt2 = 2**(1/2)
        self.deg45 = 500 - self.ropelen*self.sqrt2/2
        self.rdeg45 = self.ropelen*self.sqrt2/2
        self.swingx = self.deg45
        self.swingy = self.deg45
        self.forward = 1
        self.swingtip = Rect(self.swingx, self.swingy-5, 7, 5)
        self.fallscreen = Rect(320, 440, 380, 50)

    def draw(self):
        pygame.draw.rect(screen, (0,0,0), self.rect)
        for ladder in self.ladders:
            for i in range(5):
                screen.blit(ladderimg, (ladder.x, ladder.y+30*i))
            screen.blit(laddercrop, (ladder.x, ladder.y+150))

        for wall in self.walls:
            screen.blit(wallimg, (wall.x, wall.y))
       
        pygame.draw.rect(screen, (166,139,113), self.bottom)
        
        if self.swing == True or self.swing == 1:
            pygame.draw.polygon(screen, (255,255,255), [(495, 0), (505, 0), (self.swingx+7, self.swingy), (self.swingx, self.swingy)])
            
    def draw_fallscreen(self):
        if self.swing == True or self.swing == 1:
            pygame.draw.rect(screen, (0,0,0), self.fallscreen)
    
    def move_swing(self):
        if self.swing == True or self.swing == 1:
            if self.forward == 1:
                if self.swingx < 500:
                    self.xspeed = ((self.swingx-self.deg45)/(self.rdeg45)*self.speed)+self.speed
                    self.yspeed = -1*self.xspeed+self.speed*2
                else:
                    self.xspeed = -1*(((self.swingx-self.deg45)/(self.rdeg45)*self.speed)+self.speed)+self.speed*4
                    self.yspeed = self.xspeed-self.speed*2
            elif self.forward == 0:
                if self.swingx < 500:
                    self.xspeed = -1*self.speed*(self.swingx-self.deg45)/(self.rdeg45)-self.speed
                    self.yspeed = (-1*self.xspeed-self.speed*2)/2
                else:
                    self.xspeed = self.speed*((self.swingx-500)/self.rdeg45)-self.speed*2
                    self.yspeed = (-1*self.xspeed-self.speed*2)/-2
                    
            if self.swingx <= 500 - self.rdeg45 - 50:
                self.forward = 1
            if self.swingx >= 500 + self.rdeg45 + 50:
                self.forward = 0
            self.swingx += self.xspeed
            self.swingy += self.yspeed*0.5
            self.swingtip.x = self.swingx
            self.swingtip.y = self.swingy

class Logs:
    def __init__(self, placelogs, placepaintings, movelogs, movepaintings):
        self.movelogs = movelogs
        self.movepaintings = movepaintings
        self.placelogs = placelogs
        self.placepaintings = placepaintings
        self.speed = 4
    
    def draw(self):
        for log, painting in zip(self.movelogs, self.movepaintings):
            screen.blit(painting, (log.x, log.y))
        for log, painting in zip(self.placelogs, self.placepaintings):
            screen.blit(painting, (log.x, log.y))

    def move(self):
        if self.movelogs:
            for log in self.movelogs:
                log.x -= self.speed
                if log.x <= 0:
                    log.x = 970


class Gold:
    def __init__(self, x, y, isgold):
        self.x = x
        self.y = y
        self.rect = Rect(x, y, 20, 15)
        self.isgold = isgold
        self.pickedup = 0
    
    def draw(self):
        if self.rect.colliderect(person.rect) and person.pickup == 1:
            self.pickedup = 1
        if self.pickedup == 0 and self.isgold == 1:
            pygame.draw.rect(screen, (255,255,0), self.rect)

    





person = Person(100, 275)
floor1 = Floor([Rect(0, 415, 400, 50), Rect(500, 415, 500, 50)])
floor2 = Floor([Rect(0, 415, 320, 50), Rect(700, 415, 300, 50)])
floors = [floor1, floor2]
pit1 = Pit([Rect(435, 415, 30, 165)], [Rect(800, 465, 50, 115)], False, 0, 440)
pit2 = Pit([], [], True, 0, 440)
pits = [pit1, pit2]
log1 = Logs([Rect(600, 385, 30, 30)], [paintings[random.randint(0, len(paintings)-1)]], [Rect(850, 385, 30, 30), Rect(950, 385, 30, 30)], [paintings[random.randint(0, len(paintings)-1)], paintings[random.randint(0, len(paintings)-1)]])
log2 = Logs([], [], [], [])
logs = [log1, log2]
gold1 = Gold(0, 0, 0)
gold2 = Gold(800, 400, 1)
golds = [gold1, gold2]


pitfalling = True
gameovering = False

while pitfalling:
    key = pygame.key.get_pressed()


    fpsClock.tick(fps)
    screen.blit(background, (0,0))
    if person.rect.x > 980:
        if slide != 1:
            person.rect.x = 0
            slide += 1
        else:
            person.farright = 1
    else:
        person.farright = 0
    if person.rect.x < 0:
        if slide != 0:
            person.rect.x = 980
            slide -= 1
        else:
            person.farleft = 1
    else:
        person.farleft = 0

    if person.rect.y <= 380:
        above = 1
        below = 0
    else:
        if above == 1 and person.swinging == 0:
            score -= 100
            if score < 0:
                score = 0
        below = 1
        above = 0

    for log in logs[slide].placelogs:
        if person.rect.colliderect(log):
            score -= 1
            if score < 0:
                score = 0
    for log in logs[slide].movelogs:
        if person.rect.colliderect(log):
            score -= 1 
            if score < 0:
                score = 0  

    if golds[slide].pickedup == 0 and person.rect.colliderect(golds[slide].rect) and key[pygame.K_c] == True:
            score += 2000

    pygame.draw.rect(screen, (255,255,255), Rect(800, 0, 200, 50))
    write(score, font, (0,0,150), 850, 10)

    
    pits[slide].draw()
    pits[slide].move_swing()

    floors[slide].draw()

    logs[slide].draw()
    logs[slide].move()

    golds[slide].draw()

    person.draw()
    person.move()

    pits[slide].draw_fallscreen()



    for i in range(person.lives):
        screen.blit(heart, (820+60*i, 70))

    
    if person.lives == 0:
        gameovering = True
        pitfalling = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pitfalling = False
            gameovering = False
        if event.type == pygame.K_ESCAPE:
            pitfalling = False
            gameovering = False
    
    pygame.display.update()


while gameovering:
    screen.fill((148,192,204))
    write("GAME OVER", donefont, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), 100, 250)
    time.sleep(0.1)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameovering = False
        if event.type == pygame.K_ESCAPE:
            gameovering = True

pygame.quit()   