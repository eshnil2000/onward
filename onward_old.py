import pygame
import random
import math
import ctypes
import time
import os 
import sys
user32 = ctypes.windll.user32

os.chdir(os.path.dirname(sys.argv[0]))

class ParralexBackground:

    def __init__(self, img, imgw, speed, height, tr):
        self.image = img
        self.imgwidth = imgw
        self.scrollspeed = speed
        self.xpos = 0
        self.prevplayerpos = 0
        self.drawheight = height
        self.type = tr

        self.poslist = []

        x = -640
        while x <= GSCREENX:
            self.poslist.append(x)
            x += 640

        self.scrolllength = x

    def init(self):
        self.poslist = []
        x = -640
        while x <= GSCREENX:
            self.poslist.append(x)
            x += 640
        self.scrolllength = x
            
        
    def draw(self):

        newlist = []

        for imgpos in self.poslist:

            if game.player.x > self.prevplayerpos:
                imgpos -= self.scrollspeed
            elif game.player.x < self.prevplayerpos:
                imgpos += self.scrollspeed

            if imgpos >= self.scrolllength:
                imgpos = -640
            elif imgpos <= -640:
                imgpos = self.scrolllength

            if self.type == 'trees': spy = self.drawheight - (game.player.y-PLAYERPOSY)/(self.scrollspeed*2.0)
            elif self.type == 'mountains': spy = self.drawheight - (game.player.y-PLAYERPOSY)/(self.scrollspeed*10.0)
            else: spy = self.drawheight
            gscreen.blit(self.image, (imgpos, spy))
            newlist.append(imgpos)
            
        self.poslist = newlist

        self.prevplayerpos = game.player.x


def Draw():

    for x in range(((game.player.x & ~15) /16)-GSCREENX//30, ((game.player.x & ~15) /16)+GSCREENX//30):
        if x < 0: continue
        count = 0
        for y in range(((game.player.y & ~15) /16)-GSCREENY//30, ((game.player.y & ~15) /16)+GSCREENY//30):
            if y > MAPDEPTH: continue
            if y < 0: continue

            if game.gamemap.tiles[(x, y)].matter == 1: count += 1
            if game.gamemap.tiles[(x, y)].matter == 2: count += 1
            
            game.gamemap.tiles[(x, y)].draw(gscreen)

            if count > 0:
                shadow.set_alpha((count-1)*40)
                gscreen.blit(shadow, ((x*16 - (game.player.x - PLAYERPOSX)), (y*16 - (game.player.y - PLAYERPOSY))))

    #daynnight
    if timeofday == 'day': val = 0
    elif timeofday == 'night': val = 150
    if timefase and timeofday == 'day':
        val = 150-(fasecounter/10)
        game.backgrounds[0].image.set_alpha(((fasecounter/10)/150.0)*255.0)
        game.backgrounds[1].image.set_alpha(255-((fasecounter/10)/150.0)*255.0)
    elif timefase and timeofday == 'night':
        val = fasecounter/10
        game.backgrounds[0].image.set_alpha(255-((fasecounter/10)/150.0)*255.0)
        game.backgrounds[1].image.set_alpha(((fasecounter/10)/150.0)*255.0)
    x = pygame.Surface((GSCREENX, GSCREENY))
    x.fill(BLACK)
    x.set_alpha(val)
    gscreen.blit(x, (0, 0))



    global LvlSwitch
    if LvlSwitch:
        #pygame.draw.rect(gscreen, (70, 70, 70), (GSCREENX/2-135, GSCREENY/2-100, 273, 50), 0)
        pygame.draw.rect(gscreen, WHITE, (GSCREENX/2-135, GSCREENY/2-100, 315, 44),5)
        myfont = pygame.font.SysFont("calibri", 40, True)
        label = myfont.render("LEVEL COMPLETE!", True, WHITE)
        gscreen.blit(label, (GSCREENX/2-130, GSCREENY/2-95))
    
    window.blit(gscreen, (0, 0))

    interface.draw()

    pygame.display.update()



# -------------- Game STATIC variables
RESX, RESY = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

WINDOWX, WINDOWY = RESX//2, RESY//2
GSCREENX, GSCREENY = WINDOWX, WINDOWY 
ISCREENX, ISCREENY = WINDOWX, 40
PLAYERPOSX, PLAYERPOSY = GSCREENX//2, GSCREENY//2





background = pygame.image.load('earth2/background.png').convert()
shotgun = pygame.image.load('earth2/weapons/shotgun.png').convert_alpha()
