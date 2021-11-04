#Halloween application.
# concept:  Throw 5 bals in the ring within 10 seconds to get first price
# Every time a ball goes to the hoop, you get normal scream, when 5 within 10, special SOCK_STREAM

import pygame
import sys
import time
import math
import os
from time import sleep
import RPi.GPIO as GPIO


# Set the default path to the python directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(sourceFileDir)
Clock = 30
Score = 0
TimeOut = 30
TimeOutRemaining = TimeOut
TimeOutRunning = False
PinRing = 8 #Physcial
PinReset = 10 #Physical
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PinRing, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PinReset, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
pygame.mixer.init()
StartSound = pygame.mixer.Sound('sounds/headchop.ogg')
WonSound = pygame.mixer.Sound('sounds/won.ogg')
ScoreSound = pygame.mixer.Sound('sounds/score.ogg')
StopSound = pygame.mixer.Sound('sounds/chainsaw.ogg')

#pygame library initiation

scr = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
#scr = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Basketbal Halloween')
fontScore = pygame.font.Font('fonts/LED.ttf', 400)
fontScoreSmall = pygame.font.Font('fonts/LED.ttf', 90)
fontLabel = pygame.font.Font(
    'fonts/DejaVuSans-Bold.ttf', 80)
fontLabelSmall = pygame.font.Font(
    'fonts/DejaVuSans-Bold.ttf', 40)

LogoClub = pygame.image.load('image/hageland.png')
LogoHalloween = pygame.image.load('image/halloween.png')

textLabelHome = fontLabel.render(
    'HALLOWEEN BASKET', True, (255, 100, 100), (0, 0, 0))
textRectLabelHome = textLabelHome.get_rect(center=(640, 50))


def GetKeyboardInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            GPIO.cleanup()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                GPIO.cleanup()
            if event.key == pygame.K_SPACE:
                keystroke = "StartStop"
                return keystroke
            if event.key == pygame.K_a:
                keystroke = "Score"
                return keystroke


def BuildScreen():
    global TimeOutRemaining, Score
    textClock = fontScore.render(
        str(TimeOutRemaining), True, (255, 0, 0), (0, 0, 0))
    textScore = fontScore.render(str(Score), True, (100, 255, 0), (0, 0, 0))
    textRectClock = textClock.get_rect(center=(220, 300))
    textRectScore = textClock.get_rect(center=(720, 300))

    scr.fill((0, 0, 0))
    scr.blit(textLabelHome, textRectLabelHome)
    scr.blit(textClock, textRectClock)
    scr.blit(textScore, textRectScore)
    scr.blit(LogoClub, (100, 600))
    scr.blit(LogoHalloween, (800,50))

    pygame.display.flip()


#StartSound.play()
while True:
    TimeOutRemaining = TimeOut
    TimeOutStart = time.time()
    keystroke = GetKeyboardInput()
    if keystroke == "StartStop" or not GPIO.input(PinReset):
        TimeOutRunning = True
        StartSound.play()
        Score = 0
        time.sleep(0.3)
          

    BuildScreen()

# aftellende klok
    while TimeOutRunning:
        if TimeOutRemaining <= 0:
            TimeOutRunning = False
            StopSound.play()
        else:
            TimeOutRemaining = TimeOut - int(round(time.time()-TimeOutStart))
            BuildScreen()
            keystroke = GetKeyboardInput()
            if keystroke == "Score" or not GPIO.input(PinReset):
                Score += 1
                if Score == 5:
                    TimeOutRunning = False
                    WonSound.play()
                    time.sleep(2)
                else:
                    ScoreSound.play()
                    time.sleep(0.3)
