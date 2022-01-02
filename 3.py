import pygame
from time import sleep as wait
from random import randint as roll
from random import uniform as rollFloat
import math


starList = []
resolutionX = 1900
resolutionY = 1000
dying = False
debug = False
starSpeedModifierX = 1
starSpeedModifierY = 1
moving = [1,0,0,0]
starTimer = 10
textsurface = 0
weirdStarMovement = False

# comets
cometTimer = 0
cometList = []
spawnComet = False
cometTailList = []
cometChance = 10000
cometColorR = 0
cometColorG = 255
cometColorB = 255
cometCurveFactorInitial = 0
cometCurveFactor = cometCurveFactorInitial
cometMoveFactorInitial = 0.8
cometMoveFactor = cometMoveFactorInitial
cometInitialY = 0


initresult = pygame.init()
if not initresult:
        print("PyGame didn't init!")
        exit()
window = pygame.display.set_mode((resolutionX,resolutionY))
fontSize = 14
fontToUse = pygame.freetype.SysFont("Sans Regular",fontSize)

def createAStar():
        global starList
        global starTimer
        #if starTimer % 1 == 0 and len(starList) <= 10000:
        if len(starList) <= 1750:
                if starTimer % 2 == 0 and roll(0,2) == 2:
                        starList.append(pygame.Rect(resolutionX-10,roll(10,resolutionY-1),2,2))
                elif roll(0,3)==3:
                        starList.append(pygame.Rect(resolutionX-10,roll(10,resolutionY-1),1,1))
        starTimer += 1
def drawBackground():
        global window
        window.fill((0,0,0))
def drawStars():
        global window
        global starList
        if len(starList) == 0:
                return
        for i in starList:
                pygame.draw.rect(window,(255,255,255),i)
def checkRemoveStars():
        global starList
        for i in starList:
                indexOf = starList.index(i)
                if i.centerx <= 0 or i.centerx > resolutionX:
                        del starList[indexOf]
                if weirdStarMovement == False:
                        if i.centery <= 0 or i.centery > resolutionY:
                                del starList[indexOf]
def moveStars():
        global starList
        for i in starList:
                if moving[0]:
                        starList[starList.index(i)].centerx -= starSpeedModifierX
                if moving[2]:
                        starList[starList.index(i)].centerx += starSpeedModifierX
                if weirdStarMovement:
                        if starTimer % 20 == 0:
                                if moving[1]:
                                        starList[starList.index(i)].centery -= starSpeedModifierY
                                if moving[3]:
                                        starList[starList.index(i)].centery += starSpeedModifierY
def updateStarMovement():
        global moving
        global starSpeedModifierX
        global starSpeedModifierY
        if starTimer % 20 == 0:
                if moving[1]:
                        moving[1] = 0
                        moving[3] = 1
                elif moving[3]:
                        moving[1] = 1
                        moving[3] = 0
        starSpeedModifierY = abs(math.sin(starTimer))*100
def addDebugText():
        positionToUse = 0
        varArray = ["len(starList)","starTimer","starSpeedModifierX","starSpeedModifierY","moving","weirdStarMovement","len(cometList)","cometTimer","cometList[0].centerx","cometList[0].centery","cometCurveFactor","cometMoveFactor"]
        for i in varArray:
                try:
                        exec("fontToUse.render_to(window,(0,positionToUse),(str(\""+str(i)+"\")+\"=\"+str("+str(i)+")),(255,0,0))")
                        positionToUse+=fontSize
                except:
                        pass
def drawDebugText(var,position):
        global textSurface
        global window
        global starList
        global starTimer
        global starSpeedModifierX
        global starSpeedModifierY
        global moving
        global weirdStarMovement
        global cometList
        global cometTimer
        fontToUse.render_to(window,(0,position),(str(var)+"="+str(stringGet)),(255,0,0))
def throwComet():
        global starList
        global starTimer
        global cometTimer
        global cometList
        global spawnComet
        global cometChance
        global cometTailList
        global cometInitialY
        global cometCurveFactorInitial
        global cometCurveFactor
        global cometMoveFactorInitial
        global cometMoveFactor
        cometMoveFactor = cometMoveFactorInitial + rollFloat(-0.2,0.6)
        cometInitialY = roll(90,resolutionY-90)
        cometCurveFactor = cometCurveFactorInitial + rollFloat(-1.0,1.6)
        cometList.append(pygame.Rect(resolutionX-10,cometInitialY,26,26))
        loopnum = 25
        while loopnum != 0:
                cometTailList.append(pygame.Rect(resolutionX+100,resolutionY+100,loopnum,loopnum))
                loopnum -= 1
        spawnComet = False
def cometMove():
        global cometList
        global cometMoveFactorInitial
        global cometMoveFactor
        global cometTimer
        cometList[0].centerx = cometList[0].centerx - cometMoveFactor
        cometList[0].centery = cometInitialY + (math.sin(cometTimer)*cometCurveFactor*100)
def cometTailMove():
        global cometList
        global cometTailList
        cometX, cometY = cometList[0].centerx, cometList[0].centery
        for i in cometTailList:
                currentIndex = cometTailList.index(i)
                cometTailList[currentIndex].centerx = cometX+(currentIndex*8+(cometMoveFactor*currentIndex))
                cometTailList[currentIndex].centery = cometInitialY + (math.sin(cometTimer-(0.01*currentIndex))*cometCurveFactor*100)
def drawComet():
        global cometList
        global cometTailList
        global window
        global cometTimer
        global cometColorR
        global cometColorG
        global cometColorB
        if len(cometList) == 1:
                for i in cometTailList:
                        currentIndex = cometTailList.index(i)
                        pygame.draw.rect(window, (cometColorR,cometColorG-(10*currentIndex),cometColorB-(10*currentIndex)), i)
                pygame.draw.rect(window, (cometColorR,cometColorB,cometColorG), cometList[0])
                cometTimer += 0.01
def checkCometPosition():
        global cometList
        global cometTailList
        if cometList[0].centerx <= 0:
                del cometList[0]
                while len(cometTailList) != 0:
                        del cometTailList[0]
while not dying:

        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                        dying = True

                if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_ESCAPE:
                                dying = True
                        if event.key == pygame.K_DOWN:
                                if debug:
                                        debug = False
                                else:
                                        debug = True
                        if event.key == pygame.K_LEFT:
                                if len(cometList) == 0:
                                        spawnComet = True
                        

        createAStar()
        drawBackground()
        drawStars()
        checkRemoveStars()
        moveStars()
        if weirdStarMovement:
                updateStarMovement()
        if len(cometList) == 0:
                if roll(0,cometChance) == 0 or spawnComet == True:
                        throwComet()
        if len(cometList) == 1:
                cometMove()
                cometTailMove()
                drawComet()
                checkCometPosition()
        if debug:
                addDebugText()
        pygame.display.flip()
        
