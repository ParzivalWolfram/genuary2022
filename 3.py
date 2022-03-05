import pygame
from time import sleep as wait
from random import randint as roll
from random import uniform as rollFloat
from random import choice as pick
import math

class Star:
        def __init__(self,rect,speedX,speedY,justMoved):
                self.speedX = speedX
                self.speedY = speedY
                self.rect = rect
                self.justMoved = justMoved

class Comet:
        def __init__(self):
                global cometColors
                self.tailList = []
                self.colorList = pick(cometColors)
                self.curveFactor = 0 + rollFloat(-1.2,1.6)
                self.moveFactor = 0.8 + rollFloat(-0.7,1.6)
                self.initialY = roll(90,resolutionY-90)
                self.size = roll(10,32)
                self.rect = pygame.Rect(resolutionX-10,self.initialY,self.size,self.size)


# pygame internal stuff
resolutionX = 1900
resolutionY = 1000
dying = False

# stars
starList = []
starTimer = 10
moving = [1,0,0,0]
weirdStarMovement = False

# debug
debug = False
textsurface = 0
cometTimerFactor = 0.01
starTimerFactor = 1

# comets
cometTimer = 0
cometList = []
spawnComet = False
cometChance = 2500
cometColors = [[255,255,255],[0,255,255],[255,255,0],[255,0,255],[255,0,0],[0,255,0],[0,0,255]]

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
        if len(starList) <= 750:
                if starTimer % 2 == 0 and roll(0,2) == 2:
                        starList.append(Star(pygame.Rect(resolutionX-10,roll(10,resolutionY-1),1,1),roll(1,3),roll(1,3),False))
                elif roll(0,3)==3:
                        starList.append(Star(pygame.Rect(resolutionX-10,roll(10,resolutionY-1),2,2),roll(1,3),roll(1,3),False))

def drawBackground():
        global window
        window.fill((0,0,0))

def drawStars():
        global window
        global starList
        if len(starList) <= 0:
                return
        for i in starList:
                pygame.draw.rect(window,(255,255,255),i.rect)

def checkRemoveStars():
        global starList
        for i in starList:
                indexOf = starList.index(i)
                if i.rect.centerx <= 0 or i.rect.centerx > resolutionX:
                        del starList[indexOf]
                if weirdStarMovement == False:
                        if i.rect.centery <= 0 or i.rect.centery > resolutionY:
                                del starList[indexOf]

def moveStars():
        global starList
        for i in starList:
                if i.justMoved == False:
                        if moving[0]:
                                starList[starList.index(i)].rect.centerx -= i.speedX
                        if moving[2]:
                                starList[starList.index(i)].rect.centerx += i.speedY
                        if weirdStarMovement:
                                if starTimer % 20 == 0:
                                        if moving[1]:
                                                starList[starList.index(i)].rect.centery -= speedX
                                        if moving[3]:
                                                starList[starList.index(i)].rect.centery += speedY
                        starList[starList.index(i)].justMoved = True
                else:
                        starList[starList.index(i)].justMoved = False

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
        starSpeedModifierY = math.sin(starTimer)*100

def addDebugText():
        positionToUse = 0
        varArray = ["len(starList)","starTimer","starTimerFactor","starSpeedModifierX","starSpeedModifierY","moving","weirdStarMovement","len(cometList)","cometTimer","cometTimerFactor"]
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
        global cometTimer
        global cometList
        cometList.append(Comet())
        loopnum = cometList[-1].size
        while loopnum >= 1:
                cometList[-1].tailList.append(pygame.Rect(resolutionX+100,resolutionY+100,loopnum,loopnum))
                loopnum -= 2

def cometMove():
        global cometList
        global cometTimer
        for i in range(0,len(cometList)):
                cometList[i].rect.centerx = cometList[i].rect.centerx - cometList[i].moveFactor
                cometList[i].rect.centery = cometList[i].initialY + (math.sin(cometTimer)*cometList[i].curveFactor*100)

def cometTailMove():
        global cometList
        for i in range(0,len(cometList)):
                cometX, cometY = cometList[i].rect.centerx, cometList[i].rect.centery
                for j in cometList[i].tailList:
                        currentIndex = cometList[i].tailList.index(j)
                        cometList[i].tailList[currentIndex].centerx = cometX+(currentIndex*8+(cometList[i].moveFactor*currentIndex))
                        cometList[i].tailList[currentIndex].centery = cometList[i].initialY+(math.sin(cometTimer-(0.01*currentIndex))*cometList[i].curveFactor*100)

def drawComet():
        global cometList
        global window
        for i in range(0,len(cometList)):
                tailLength = len(cometList[i].tailList)
                size = cometList[i].size
                for j in cometList[i].tailList:
                        currentIndex = cometList[i].tailList.index(j)
                        tempColor = (min(max(0,(cometList[i].colorList[0]/(currentIndex+1*(tailLength/16)))),255),
                                     min(max(0,(cometList[i].colorList[1]/(currentIndex+1*(tailLength/16)))),255),
                                     min(max(0,(cometList[i].colorList[2]/(currentIndex+1*(tailLength/16)))),255))
                        try:
                                pygame.draw.rect(window, tempColor, cometList[i].tailList[currentIndex]) #-(10*currentIndex)
                        except:
                                pass
                pygame.draw.rect(window, cometList[i].colorList, cometList[i].rect)

def checkCometPosition():
        global cometList
        for i in range(0,len(cometList)):
                try:
                        if cometList[i].rect.centerx <= 1:
                                del cometList[i]
                except:
                        pass


while not dying:
        # === control routine ===
        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                        dying = True

                if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_ESCAPE:
                                dying = True

                        #=== debug keys ===

                        #show debugging info
                        if event.key == pygame.K_DELETE:
                                if debug:
                                        debug = False
                                else:
                                        debug = True
                        #force spawn a comet next frame
                        if event.key == pygame.K_INSERT:
                                spawnComet = True
                        #control comet timer - granular
                        if event.key == pygame.K_KP7:
                                cometTimerFactor += 0.01
                        if event.key == pygame.K_KP4:
                                cometTimerFactor -= 0.01
                        #control comet timer - coarse
                        if event.key == pygame.K_KP8:
                                cometTimerFactor += 0.1
                        if event.key == pygame.K_KP5:
                                cometTimerFactor -= 0.1
                        #control star timer - granular
                        if event.key == pygame.K_KP1 or event.key == pygame.K_KP2: #usually, KP0 is double-wide, so this is just to make things slightly easier on the hands
                                starTimerFactor += 0.1
                        if event.key == pygame.K_KP0:
                                starTimerFactor -= 0.1
                        #control star timer - coarse
                        if event.key == pygame.K_KP3:
                                starTimerFactor += 1
                        if event.key == pygame.K_KP_PERIOD:
                                starTimerFactor -= 1


#=== logic ===

        #timers
        cometTimer += cometTimerFactor
        starTimer += starTimerFactor

        #always-on logic
        createAStar()
        drawBackground()
        drawStars()
        checkRemoveStars()
        moveStars()

        #conditional logic
        if weirdStarMovement:
                updateStarMovement()
        if roll(0,cometChance) == 0 or spawnComet == True:
                throwComet()
                spawnComet = False
        if len(cometList) != 0:
                cometMove()
                cometTailMove()
                drawComet()
                checkCometPosition()
        if debug:
                addDebugText()

        #finally, move on to next frame
        pygame.display.flip()


#=== quit ===        
pygame.display.quit()
