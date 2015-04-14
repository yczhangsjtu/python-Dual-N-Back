import pygame
import random
from string import lowercase

from pygame.locals import *

pygame.init()

width, height = 750, 480
screen = pygame.display.set_mode((width,height))
pygame.mixer.init()

startbutton = pygame.image.load("resources/images/start.png")
stopbutton = pygame.image.load("resources/images/stop.png")
bar = pygame.image.load("resources/images/bar.png")
circ = pygame.image.load("resources/images/circ.png")
square = pygame.image.load("resources/images/square.png")

voice = [pygame.mixer.Sound("resources/audio/%s.ogg"%(lowercase[i]))\
         for i in range(26)]

gamestate = 0
interval = 3000
number = 30
dualn = 3
squares = []
currsqr = None
prevsqr = None

running = True
amatch = False
pmatch = False
showsquare = False
pcolor = (0,0,0)
acolor = (0,0,0)
pright = 0
pwrong = 0
aright = 0
awrong = 0
numsqr = 0

while running:
    screen.fill((255,255,255))
    startx = width/2
    starty = height-startbutton.get_height()/2
    stopx = width/2
    stopy = height-stopbutton.get_height()/2
    if gamestate == 0:
        screen.blit(startbutton,((width-startbutton.get_width())/2,height-startbutton.get_height()))
        screen.blit(bar,(150,48))
        screen.blit(bar,(150,148))
        screen.blit(bar,(150,248))
        screen.blit(circ,((interval-500)/11+120,40))
        screen.blit(circ,((number-5)*9+120,140))
        screen.blit(circ,((dualn-2)*50+120,240))

        font = pygame.font.Font(None,60)
        Interval = font.render("Interval",True,(0,0,0))
        textRect = Interval.get_rect()
        textRect.topleft = [0,45]
        screen.blit(Interval,textRect)

        font = pygame.font.Font(None,60)
        nInterval = font.render(str(interval)+"ms",True,(0,0,0))
        textRect = Interval.get_rect()
        textRect.topleft = [600,45]
        screen.blit(nInterval,textRect)

        font = pygame.font.Font(None,60)
        Number = font.render("Number",True,(0,0,0))
        textRect = Number.get_rect()
        textRect.topleft = [0,145]
        screen.blit(Number,textRect)

        font = pygame.font.Font(None,60)
        nNumber = font.render(str(number),True,(0,0,0))
        textRect = nNumber.get_rect()
        textRect.topleft = [600,145]
        screen.blit(nNumber,textRect)

        font = pygame.font.Font(None,60)
        N = font.render("dual-N",True,(0,0,0))
        textRect = N.get_rect()
        textRect.topleft = [0,245]
        screen.blit(N,textRect)

        font = pygame.font.Font(None,60)
        nN = font.render(str(dualn),True,(0,0,0))
        textRect = nN.get_rect()
        textRect.topleft = [600,245]
        screen.blit(nN,textRect)
    elif gamestate == 1:
        screen.blit(stopbutton,((width-stopbutton.get_width())/2,height-stopbutton.get_height()))
        gridsize = 100
        pygame.draw.line(screen,(0,0,0),((width-gridsize*3)/2,20),((width+gridsize*3)/2,20))
        pygame.draw.line(screen,(0,0,0),((width-gridsize*3)/2,20+gridsize),((width+gridsize*3)/2,20+gridsize))
        pygame.draw.line(screen,(0,0,0),((width-gridsize*3)/2,20+gridsize*2),((width+gridsize*3)/2,20+gridsize*2))
        pygame.draw.line(screen,(0,0,0),((width-gridsize*3)/2,20+gridsize*3),((width+gridsize*3)/2,20+gridsize*3))
        pygame.draw.line(screen,(0,0,0),((width-gridsize*3)/2,20),((width-gridsize*3)/2,20+3*gridsize))
        pygame.draw.line(screen,(0,0,0),((width-gridsize)/2,20),((width-gridsize)/2,20+3*gridsize))
        pygame.draw.line(screen,(0,0,0),((width+gridsize)/2,20),((width+gridsize)/2,20+3*gridsize))
        pygame.draw.line(screen,(0,0,0),((width+gridsize*3)/2,20),((width+gridsize*3)/2,20+3*gridsize))
        if showsquare:
            screen.blit(square,(currsqr[0]*gridsize+(width-gridsize*3)/2+5,currsqr[1]*gridsize+25))

        font = pygame.font.Font(None,30)
        nPos = font.render("Position Match",True,pcolor)
        textRect = nPos.get_rect()
        textRect.topleft = [100,400]
        screen.blit(nPos,textRect)

        font = pygame.font.Font(None,30)
        nAud = font.render("Audio Match",True,acolor)
        textRect = nPos.get_rect()
        textRect.topleft = [500,400]
        screen.blit(nAud,textRect)

        font = pygame.font.Font(None,30)
        nLeft = font.render("Left: %d"%(number-numsqr),True,(0,0,0))
        textRect = nLeft.get_rect()
        textRect.topleft = [600,20]
        screen.blit(nLeft,textRect)
    elif gamestate == 2:
        font = pygame.font.Font(None,30)
        nPos = font.render("Position: %d-%d"%(pright,pwrong),True,(0,0,0))
        textRect = nPos.get_rect()
        textRect.topleft = [0,20]
        screen.blit(nPos,textRect)

        font = pygame.font.Font(None,30)
        nAud = font.render("Audio : %d-%d"%(aright,awrong),True,(0,0,0))
        textRect = nPos.get_rect()
        textRect.topleft = [0,50]
        screen.blit(nAud,textRect)

        font = pygame.font.Font(None,30)
        right = aright+pright
        total = right+awrong+pwrong
        if total == 0:
            percent = 0
        else:
            percent = right*100/total
        nPer = font.render("Score: %d"%(percent),True,(0,0,0))
        textRect = nPos.get_rect()
        textRect.topleft = [0,80]
        screen.blit(nPer,textRect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.MOUSEMOTION:
            prs = pygame.mouse.get_pressed()
            pst = pygame.mouse.get_pos()
            if gamestate == 0:
                if prs[0]:
                    if pst[0] >= 150 and pst[0] <= 566:
                        if pst[1] >= 40 and pst[1] < 100:
                            interval = (pst[0]-20 - 120)*11+500
                        if pst[1] >= 140 and pst[1] < 200:
                            number = (pst[0]-20 - 120)/9+5
                        if pst[1] >= 240 and pst[1] < 300:
                            dualn = (pst[0]-20 - 120)/50+2
        if event.type == pygame.MOUSEBUTTONDOWN:
            prs = pygame.mouse.get_pressed()
            pst = pygame.mouse.get_pos()
            if gamestate == 0:
                if pst[0] >= 150 and pst[0] <= 566:
                    if pst[1] >= 40 and pst[1] < 100:
                        interval = (pst[0]-20 - 120)*11+500
                    if pst[1] >= 140 and pst[1] < 200:
                        number = (pst[0]-20 - 120)/9+5
                    if pst[1] >= 240 and pst[1] < 300:
                        dualn = (pst[0]-20 - 120)/50+2
                dx = pst[0] - startx
                dy = pst[1] - starty
                r = startbutton.get_width()/2
                if dx*dx+dy*dy < r*r:
                    gamestate = 1
                    pygame.time.set_timer(pygame.USEREVENT+1,interval)
                    pright,pwrong,pmatch,pcolor = 0,0,False,(0,0,0)
                    numsqr = 0
            elif gamestate == 1:
                dx = pst[0] - stopx
                dy = pst[1] - stopy
                r = stopbutton.get_width()/2
                if dx*dx+dy*dy < r*r:
                    gamestate = 0
                    pygame.time.set_timer(pygame.USEREVENT+1,0)
                else:
                    if prs[0] and prevsqr and currsqr and pcolor==(0,0,0):
                        pmatch = True
                        if prevsqr[0]==currsqr[0] and prevsqr[1]==currsqr[1]:
                            pright+=1
                            pcolor=(0,255,0)
                        else:
                            pwrong+=1
                            pcolor=(255,0,0)
                    if prs[2] and prevsqr and currsqr and acolor==(0,0,0):
                        amatch = True
                        if prevsqr[2]==currsqr[2]:
                            aright+=1
                            acolor=(0,255,0)
                        else:
                            awrong+=1
                            acolor=(255,0,0)
            elif gamestate == 2:
                gamestate = 0
        if event.type == pygame.USEREVENT+1:
            if currsqr and prevsqr:
                if currsqr[0]==prevsqr[0] and currsqr[1]==prevsqr[1]:
                    if pmatch:
                        pcolor = (0,0,0)
                    else:
                        pcolor = (0,0,255)
                        pwrong+=1
                        pygame.time.set_timer(pygame.USEREVENT+2,200)
                else:
                    pcolor = (0,0,0)
                if currsqr[2]==prevsqr[2]:
                    if amatch:
                        acolor = (0,0,0)
                    else:
                        acolor = (0,0,255)
                        awrong+=1
                        pygame.time.set_timer(pygame.USEREVENT+3,200)
                else:
                    acolor = (0,0,0)
            numsqr += 1
            if numsqr > number:
                gamestate = 2
                pygame.time.set_timer(pygame.USEREVENT+1,0)
                continue
            x = random.randrange(0,3)
            y = random.randrange(0,3)
            c = random.randrange(26)
            if prevsqr:
                k = random.randrange(7)
                if k == 0: c = prevsqr[2]
                k = random.randrange(7)
                if k == 0: x,y=prevsqr[0],prevsqr[1]
            currsqr = (x,y,c)
            squares.append(currsqr)
            voice[c].play()
            showsquare = True
            pygame.time.set_timer(pygame.USEREVENT+4,200)
            if len(squares)>dualn:
                prevsqr = squares.pop(0)
        if event.type == pygame.USEREVENT+2:
            pcolor = (0,0,0)
            pygame.time.set_timer(pygame.USEREVENT+2,0)
        if event.type == pygame.USEREVENT+3:
            acolor = (0,0,0)
        if event.type == pygame.USEREVENT+4:
            showsquare = False
            pygame.time.set_timer(pygame.USEREVENT+4,0)
