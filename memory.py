import pygame
import os
import sys
import random
import time
from pygame.locals import *
from math import *
MIN_WIDTH = 1200
MIN_HEIGHT = 800

GEAR_X = MIN_WIDTH-64-50
GEAR_Y = 50

FRAME_RATE = 120

PI = 3.141592653

BACK_BUTTON_X = 50
BACK_BUTTON_Y = 50

SETTINGS_PADDING = 150
SETTINGS_PADDING_Y = 100
COLOUR_BLIND_MODE = False #Default setting
COLOUR_BLIND_ICON_X = 100
COLOUR_BLIND_ICON_Y = 150
CURRENT_PATH = os.path.dirname(sys.executable)
RESOURCES_PATH = os.path.join(CURRENT_PATH, 'Resources')

SQUARE_DIMENSION = 20 # Height and width of square
REVEALSPEED = 10
SHAPES = ()
COLOURS = ()

WAIT_TIME = 200 # FOR APPLYING SETTINGS. (So events don't overlap one another.)
MOUSE_CLICKED = False

MIN_PADDING = 200
BOX_SIZE = 40
SPACING = 20
BOARD_SIZE = 4 # Will generate a perfect square board e.g 6x6, 7x7, 8x8
X_MARGIN = int((MIN_WIDTH - (BOARD_SIZE * (BOX_SIZE + SPACING))) / 2)
Y_MARGIN = int((MIN_HEIGHT - (BOARD_SIZE * (BOX_SIZE + SPACING))) / 2)

BLUE_SPACE_CADET = (29, 53, 87) # Reserved for background.

HONEYDEW = (241, 250, 238)
RED_DESIRE = (230, 57, 70)
LIGHT_BLUE = (168,218,220)
QUEEN_BLUE = (69,123,157)
JET_BLACK = (54,53,55) # Used for some icons, but not in-game
PARADISE_PINK = (238,66,102)
GREEN_GO = (14,173,105)
PISTACHIO_GREEN = (140,216,103)
ORANGE = (215,100,51)
LIGHT_PURPLE = (63,39,96)
LIGHT_PINK = (237,118,243)
REDDISH_BROWN = (101,46,36)
DARK_YELLOW = (211,192,34)

BLACK = (0,0,0)
LIGHT_BLUE_HIGH_CONTRAST = (0,255,255)
WHITE = (255,255,255)
YELLOW_HIGH_CONTRAST = (255,255,0)
PINK_HIGH_CONTRAST = (255,124,255)
WEIRD_PINK_SKIN_HC = (255,124,124)
GREEN_HIGH_CONTRAST = (125,255,124)
BLUISH_PURPLE_HIGH_CONTRAST = (125,142,255)
DARKER_GREEN_HIGH_CONTRAST = (0,208,108)
ORANGE_HIGH_CONTRAST = (255,134,33)
GOLD = (255,187,0)
MAGENTA = (255,33,122)


SKIN_COLOUR = (246,180,174)
# One for high contrast, the other is normal. 
COLOUR_SCHEMES = ()

CIRCLE = 0
SQUARE = 1
TRIANGLE = 2
TILTED_HOURGLASS = 3
PENTAGON = 4
DIAMOND = 5
HEXAGON = 6
CROSS = 7
SHAPES = (CIRCLE,DIAMOND, PENTAGON, TILTED_HOURGLASS, TRIANGLE, SQUARE, HEXAGON, CROSS)
COLOURS = (HONEYDEW, RED_DESIRE, LIGHT_BLUE, QUEEN_BLUE, PARADISE_PINK, GREEN_GO, PISTACHIO_GREEN, ORANGE, LIGHT_PURPLE, LIGHT_PINK, REDDISH_BROWN, DARK_YELLOW, GOLD)
COLOUR_BLIND_SCHEME = (LIGHT_BLUE_HIGH_CONTRAST, WHITE, YELLOW_HIGH_CONTRAST, PINK_HIGH_CONTRAST, WEIRD_PINK_SKIN_HC, GREEN_HIGH_CONTRAST, BLUISH_PURPLE_HIGH_CONTRAST, DARKER_GREEN_HIGH_CONTRAST, ORANGE_HIGH_CONTRAST,GOLD, MAGENTA, PISTACHIO_GREEN)
COLOUR_SCHEMES = (COLOURS, COLOUR_BLIND_SCHEME)

PLAY_AUDIO = True
INPUT_HANDLER = pygame.USEREVENT + 1

quitGame = False
restartGame = False

gearColour = gearHighlightColour = backIconColour = backIconHC = None
settingsMenuColour = mainMenuColour = None
toggleOn = toggleOnHC = None
toggleOff = toggleOffHC = None
mouse_x_pos = 0
mouse_y_pos = 0
boxes = []
highScore = -1
# LIST OF ALL SLIDERS TO ITERATE THROUGH. 
# KEYBOARD CONTROLS
'''
To go down, increase the index by one
To go up, decrease the index by one
To go right, increase the index by the column number
To go left, decrease the index by the column number

Make sure the index doesn't exceed the size of the board
'''
currentlySelected = 0 # Variable to store box index for keyboard use. 
# Returns whether the mouse is current in use, in which case it will stop highlighting with keyboard.
isMouseMoving = False 
buttonPress = False # Was there a button press?
KEYBOARD_DELAY = 100
pressedEnter = False

# INVERTED COLOURS SETTING
''' 
The basic math behind this is that you take the 8 bit number away from 255. 
So in RGB colours
Inverted Colour = (255-R, 255-G, 255-B)
This inverts black to white, orange to blue and so on...
'''
invertedColours = False
SMALL_MODE = 0
MEDIUM_MODE = 1
LARGE_MODE = 2
XTREME_MODE = 3
CURRENT_MODE = SMALL_MODE

SMALL_MODE_HS = "0"
MEDIUM_MODE_HS = "0"
LARGE_MODE_HS = "0"
XTREME_MODE_HS = "0"



def button(msg, x, y, w, h, ic, ac, action=None):
    mousePos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if ((x+w > mousePos[0] > x) and (y+h > mousePos[1] > y)):
        pygame.draw.rect(DISPLAY,ac,(x,y,w,h))
        if (clicked[0] == 1 and action != None):
            action()
    else:
        pygame.draw.rect(DISPLAY, ic, (x,y,w,h))

def adjustColourScheme():
    global gearColour, gearHighlightColour, backIconColour, backIconHC
    global settingsMenuColour, mainMenuColour
    global toggleOff, toggleOffHC
    global toggleOn, toggleOnHC
    if (COLOUR_BLIND_MODE):
        gearColour = PINK_HIGH_CONTRAST
        gearHighlightColour = WEIRD_PINK_SKIN_HC
        backIconColour = JET_BLACK
        backIconHC = BLACK
        mainMenuColour = BLACK
        settingsMenuColour = WHITE
        toggleOff = PINK_HIGH_CONTRAST
        toggleOffHC = WEIRD_PINK_SKIN_HC
        toggleOn = GREEN_HIGH_CONTRAST
        toggleOnHC = DARKER_GREEN_HIGH_CONTRAST
    else:
        gearColour = QUEEN_BLUE
        gearHighlightColour = LIGHT_BLUE
        backIconColour = JET_BLACK
        backIconHC = HONEYDEW
        mainMenuColour = BLUE_SPACE_CADET
        settingsMenuColour=LIGHT_BLUE
        toggleOff = RED_DESIRE
        toggleOffHC = PARADISE_PINK
        toggleOn = GREEN_GO
        toggleOnHC = PISTACHIO_GREEN
# Function Kivy calls. Cannot be individual reference, must be function
def initial():
    global quitGame
    quitGame = False

def main():
    global DISPLAY
    global X_MARGIN
    global Y_MARGIN
    global SMALL_MODE_HS, MEDIUM_MODE_HS, LARGE_MODE_HS, XTREME_MODE_HS
    global PLAY_AUDIO
    global clock
    global mouse_x_pos
    global mouse_y_pos
    global highscoreText
    global gearIcon
    global backIcon
    global colourBlindIcon
    global restartButton
    global trophyIco
    clock = pygame.time.Clock()
    global passed_time
    passed_time = 0
    global start_time
    global font
    global font_colour
    font_colour = (255,255,255)
    start_time = pygame.time.get_ticks()
    
    global gearColour, gearHighlightColour
    global backIconColour, backIconHC
    global settingsMenuColour
    global mainMenuColour


    global soundIcon
    global boardSizeIcon
    global smallModeIcon
    global mediumModeIcon
    global largeModeIcon
    global xtremeModeIcon

    global first_selection
    global second_selection

    global restartGame
    global quitGame
    pygame.mixer.init()
    pygame.init()
    font = pygame.font.Font(None, 54)
    DISPLAY = pygame.display.set_mode((MIN_WIDTH,MIN_HEIGHT))
    pygame.display.set_caption("Memory")
    update_events()
    
    generateBoxes(BOARD_SIZE)
    gearIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "gear-64.png"))
    gearIcon.fill((69,123,157),special_flags=pygame.BLEND_MULT)

    restartButton = pygame.image.load(os.path.join(RESOURCES_PATH, "restart-64.png"))

    backIcon = pygame.image.load(os.path.join(RESOURCES_PATH,"back-64.png"))
    backIcon.fill((69,123,157),special_flags=pygame.BLEND_MULT)
    trophyIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "trophy.png")).convert_alpha()

    colourBlindIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "colourBlind-64.png"))
    colourBlindIcon.fill((0,0,0), special_flags=pygame.BLEND_MULT)

    boardSizeIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "board_size.png"))
    smallModeIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "small.png"))
    mediumModeIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "medium.png"))
    largeModeIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "large.png"))
    xtremeModeIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "xtreme.png"))
    soundIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "audio.png"))
    adjustColourScheme()
    pygame.mixer.music.load(os.path.join(RESOURCES_PATH, 'bgMusic.wav'))
    gameIcon = pygame.image.load(os.path.join(RESOURCES_PATH, "logo.png"))
    pygame.display.set_icon(gameIcon)
    # PLAY THE MUSIC
    pygame.mixer.music.play(-1)
    # Game Loop. 
    font_color = pygame.Color('springgreen')
    while not quitGame:
        #boxes = 
        update_events()
        adjustColourScheme()
        DISPLAY.fill(mainMenuColour)
        DISPLAY.blit(gearIcon, (GEAR_X,GEAR_Y))
        DISPLAY.blit(restartButton, (BACK_BUTTON_X, BACK_BUTTON_Y))
        drawMainBoard()
        box_manager()
        handleKeyboardInputs()
        button_manager()
        #print("Audio is playing: " + str(PLAY_AUDIO))
        if (restartGame):
            X_MARGIN = int((MIN_WIDTH - (BOARD_SIZE * (BOX_SIZE + SPACING))) / 2)
            Y_MARGIN = int((MIN_HEIGHT - (BOARD_SIZE * (BOX_SIZE + SPACING))) / 2)
            generateBoxes(BOARD_SIZE)
            first_selection = None
            second_selection = None
            start_time = pygame.time.get_ticks()
            pygame.time.wait(50)
            restartGame = False
            #box_manager()
        if (not hasWonGame()):
            passed_time = pygame.time.get_ticks() - start_time
        else:
            highscoreText = "{:02d}".format(int(passed_time/3600000)) + ":" + "{:02d}".format(int(passed_time/60000)) + ":" + "{:02d}".format(int(passed_time/1000 % 60))
            actualNum = int("".join(highscoreText.split(":")))
            smallHS = int("".join(SMALL_MODE_HS.split(":")))
            mediumHS = int("".join(MEDIUM_MODE_HS.split(":")))
            largeHS = int("".join(LARGE_MODE_HS.split(":")))
            xtremeHS = int("".join(XTREME_MODE_HS.split(":")))
            #print("Actual num is " + str(actualNum))
            #print("Small HS is " + str(smallHS))
            #print("Medium HS is " + str(mediumHS))
            #print("Large medium HS " + str(largeHS))
            #print("Xtreme mode HS is" + str(xtremeHS))
            if (CURRENT_MODE == SMALL_MODE and (actualNum < smallHS or smallHS == 0)):
                SMALL_MODE_HS = highscoreText
            elif (CURRENT_MODE == MEDIUM_MODE and (actualNum < mediumHS or mediumHS == 0)):
                MEDIUM_MODE_HS = highscoreText
            elif (CURRENT_MODE == LARGE_MODE and (actualNum < largeHS or largeHS == 0)):
                LARGE_MODE_HS = highscoreText
            elif (CURRENT_MODE == XTREME_MODE and (actualNum < xtremeHS or xtremeHS == 0)):
                XTREME_MODE_HS = highscoreText
                #print(highscoreText)
        textToRender = None
        if (CURRENT_MODE == SMALL_MODE):
            textToRender = SMALL_MODE_HS
        elif (CURRENT_MODE == MEDIUM_MODE):
            textToRender = MEDIUM_MODE_HS
        elif (CURRENT_MODE == LARGE_MODE):
            textToRender = LARGE_MODE_HS
        elif (CURRENT_MODE == XTREME_MODE):
            textToRender = XTREME_MODE_HS
        text = font.render("{:02d}".format(int(passed_time/3600000)) + ":" + "{:02d}".format(int(passed_time/60000)) + ":" + "{:02d}".format(int(passed_time/1000 % 60)), True, font_color)
        toggleAudio()
        #highscore = font.render()
        DISPLAY.blit(text, (X_MARGIN+SPACING * (BOARD_SIZE/2)  + BOX_SIZE * ((BOARD_SIZE/2)-1)-20, Y_MARGIN-15))
        DISPLAY.blit(trophyIcon, (BACK_BUTTON_X+ 100, GEAR_Y))
        highscore = font.render(textToRender, True, font_color)
        DISPLAY.blit(highscore, (BACK_BUTTON_X+200, GEAR_Y+15))
        button_manager()
        pygame.display.update()
        clock.tick(FRAME_RATE)


#def settings():
def button_manager():
    global start_time
    global passed_time
    global restartGame
    global PLAY_AUDIO
    clicked = pygame.mouse.get_pressed()
    if (GEAR_X < mouse_x_pos < GEAR_X+gearIcon.get_width() and GEAR_Y < mouse_y_pos < GEAR_Y+gearIcon.get_height()):
        gearIcon.fill((0,0,0, 128),special_flags=pygame.BLEND_RGB_MULT)
        gearIcon.fill((gearHighlightColour),special_flags=pygame.BLEND_RGB_ADD)
        if (clicked[0] == 1):
            while(True):
                start_time = pygame.time.get_ticks() - passed_time
                #gearIcon.fill((0,0,0,0))
                #print(restartGame)
                update_events()
                adjustColourScheme()
                DISPLAY.fill(settingsMenuColour)
                DISPLAY.blit(backIcon, (BACK_BUTTON_X, BACK_BUTTON_Y))
                DISPLAY.blit(colourBlindIcon, (COLOUR_BLIND_ICON_X, COLOUR_BLIND_ICON_Y))
                DISPLAY.blit(boardSizeIcon, (COLOUR_BLIND_ICON_X, COLOUR_BLIND_ICON_Y+SETTINGS_PADDING_Y))
                DISPLAY.blit(smallModeIcon, (COLOUR_BLIND_ICON_X+SETTINGS_PADDING, COLOUR_BLIND_ICON_Y + SETTINGS_PADDING_Y))
                DISPLAY.blit(mediumModeIcon, (COLOUR_BLIND_ICON_X+SETTINGS_PADDING*2, COLOUR_BLIND_ICON_Y + SETTINGS_PADDING_Y))
                DISPLAY.blit(largeModeIcon, (COLOUR_BLIND_ICON_X+SETTINGS_PADDING*3, COLOUR_BLIND_ICON_Y + SETTINGS_PADDING_Y))
                DISPLAY.blit(xtremeModeIcon, (COLOUR_BLIND_ICON_X+SETTINGS_PADDING*4, COLOUR_BLIND_ICON_Y + SETTINGS_PADDING_Y))
                DISPLAY.blit(soundIcon, (COLOUR_BLIND_ICON_X,COLOUR_BLIND_ICON_Y+SETTINGS_PADDING_Y*2))
                #musicLoop()
                print("Audio is: " + str(PLAY_AUDIO))
                if (not settings_button_manager()):
                    pygame.time.wait(WAIT_TIME)
                    break
                toggleAudio()
                pygame.display.update()
                clock.tick(FRAME_RATE)
    elif (BACK_BUTTON_X < mouse_x_pos < BACK_BUTTON_X + restartButton.get_width() and BACK_BUTTON_Y < mouse_y_pos < BACK_BUTTON_Y+restartButton.get_height()):
        fillIcon(restartButton, gearHighlightColour)
        if (clicked[0] == 1):
            restartGame = True
            #print("k")
    else:
        gearIcon.fill((0,0,0, 128),special_flags=pygame.BLEND_RGB_MULT)
        gearIcon.fill((gearColour),special_flags=pygame.BLEND_RGB_ADD)
        fillIcon(restartButton, gearColour)


def fillIcon(icon, color):
    icon.fill((0,0,0), special_flags=pygame.BLEND_RGB_MULT)
    icon.fill(color, special_flags=pygame.BLEND_RGB_ADD)

def animateButton(x, y, MIN_X):
    if (x > MIN_X):
        pygame.draw.circle(DISPLAY, RED_DESIRE, (x, y), 20)
    pygame.display.update()
    clock.tick(FRAME_RATE)


def drawToggle(x, y, height, width, boolToToggle, HC_toggle_on, HC_toggle_off, toggle_on, toggle_off):
    clicked = pygame.mouse.get_pressed()
    if (x < mouse_x_pos < x+width and y < mouse_y_pos < y+height):
        # Its highlighted.
        if (boolToToggle):
            pygame.draw.rect(DISPLAY, HC_toggle_on, (x, y, width, height))
        else:
            pygame.draw.rect(DISPLAY, HC_toggle_off, (x, y, width, height))
        if (clicked[0] == 1):
            if (boolToToggle == False):
                boolToToggle = True
                pygame.time.wait(WAIT_TIME)
            else:
                boolToToggle = False
                pygame.time.wait(WAIT_TIME)
    else:
        if (boolToToggle):
            pygame.draw.rect(DISPLAY, toggle_on, (x, y, width, height))
        #pygame.time.wait(WAIT_TIME)
        else:
            pygame.draw.rect(DISPLAY, toggle_off, (x, y, width, height))
        #pygame.time.wait(WAIT_TIME)
    return boolToToggle


'''
def colourBlindMode():
    global COLOUR_BLIND_MODE
    clicked = pygame.mouse.get_pressed()
    
    if (COLOUR_BLIND_ICON_X +SETTINGS_PADDING < mouse_x_pos < COLOUR_BLIND_ICON_X+ SETTINGS_PADDING +128 and COLOUR_BLIND_ICON_Y+16< mouse_y_pos < COLOUR_BLIND_ICON_Y + colourBlindIcon.get_height()-16):
        if (COLOUR_BLIND_MODE):
            pygame.draw.rect(DISPLAY, (toggleOnHC),(COLOUR_BLIND_ICON_X+SETTINGS_PADDING, COLOUR_BLIND_ICON_Y+16, 128, 32))
        else:
            pygame.draw.rect(DISPLAY, (toggleOffHC),(COLOUR_BLIND_ICON_X+SETTINGS_PADDING, COLOUR_BLIND_ICON_Y+16, 128, 32))
        if (clicked[0] == 1):
            if (COLOUR_BLIND_MODE == False):
                COLOUR_BLIND_MODE=True
                pygame.time.wait(WAIT_TIME)
            else:
                COLOUR_BLIND_MODE=False
                pygame.time.wait(WAIT_TIME)
    else:
        if (COLOUR_BLIND_MODE):
            pygame.draw.rect(DISPLAY, (toggleOn),(COLOUR_BLIND_ICON_X+SETTINGS_PADDING, COLOUR_BLIND_ICON_Y+16, 128, 32))
        else:
            pygame.draw.rect(DISPLAY, (toggleOff),(COLOUR_BLIND_ICON_X+SETTINGS_PADDING, COLOUR_BLIND_ICON_Y+16, 128, 32))
'''

#KEYBOARD_SETTINGS_X = 
mainSettings = True
keyboardSettings = False
'''
class GUI_Slider():
    global backIcon
    def __init__(self, value, maximum_right, maximum_left, x_pos, y_pos):
        self.value = value
        self.maxRight = maximum_right
        self.maxLeft = maximum_left
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.surf = pygame.surface.Surface((100, 50))
        self.clicked = False

        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, BLUE_SPACE_CADET, [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, RED_DESIRE, (10,10,80,10),0)
        pygame.draw.rect(self.surf, GREEN_GO, (10,30,80,5),0)
        
        self.buttonSurface = pygame.surface.Surface((20, 20))
        self.buttonSurface.fill((1,1,1))
        self.buttonSurface.set_colorkey((1,1,1))
        pygame.draw.circle(self.buttonSurface, BLACK, (10,10), 6, 0)
        pygame.draw.circle(self.buttonSurface, (200, 100, 50), (10,10), 4, 0)

    def draw_slider(self):
        surface = self.surf.copy()
        pos = (10+int((self.value-self.maxLeft)/(self.maxRight-self.maxLeft)*80), 33)
        self.buttonRect = self.buttonSurface.get_rect(center = pos)
        surface.blit(self.buttonSurface, self.buttonRect)
        self.buttonRect.move_ip(self.x_pos, self.y_pos)
        DISPLAY.blit(surface, (self.x_pos, self.y_pos))

    def move(self):
        self.value = pygame.mouse.get_pos()[0] - (self.x_pos-10) / 80 * (self.maxRight - self.maxLeft) + self.maxLeft
        if (self.value < self.maxLeft):
            self.value = self.maxLeft
        
        if (self.value > self.maxRight):
            self.value = self.maxRight

'''
#volumeSlider = GUI_Slider(100, 105, 1, 10,10 )
#sliders = [volumeSlider]
def settings_button_manager():
    global COLOUR_BLIND_MODE
    global CURRENT_MODE
    global BOARD_SIZE
    global PLAY_AUDIO
    global restartGame
    global mainSettings, keyboardSettings
    clicked = pygame.mouse.get_pressed()
    board_size_icon_x = COLOUR_BLIND_ICON_X
    board_size_icon_y = COLOUR_BLIND_ICON_Y+SETTINGS_PADDING_Y
    mode_select_size = 64
    if (BACK_BUTTON_X < mouse_x_pos < BACK_BUTTON_X + backIcon.get_width() and BACK_BUTTON_Y < mouse_y_pos < BACK_BUTTON_Y + backIcon.get_height()):
        #backIcon.fill((0,0,0),special_flags=pygame.BLEND_RGB_MULT)
        #backIcon.fill((HONEYDEW),special_flags=pygame.BLEND_RGB_ADD)
        fillIcon(backIcon, backIconHC)
        if (clicked[0] == 1):
            return False
            pygame.time.wait(WAIT_TIME)
    else:
        fillIcon(backIcon, backIconColour)

    if (board_size_icon_y < mouse_y_pos < board_size_icon_y + mode_select_size):
        if (board_size_icon_x+SETTINGS_PADDING < mouse_x_pos < board_size_icon_x+SETTINGS_PADDING+mode_select_size):
            # SMALL MODE SELECT
            if (clicked[0] == 1 and CURRENT_MODE != SMALL_MODE):
                CURRENT_MODE = SMALL_MODE
                restartGame = True
        elif (board_size_icon_x+SETTINGS_PADDING * 2 < mouse_x_pos < board_size_icon_x+SETTINGS_PADDING*2+mode_select_size):
            # MEDIUM MODE SELECT
            if (clicked[0] == 1 and CURRENT_MODE != MEDIUM_MODE):
                CURRENT_MODE = MEDIUM_MODE
                restartGame = True
            #pygame.draw.rect(DISPLAY, GREEN_HIGH_CONTRAST, (board_size_icon_x+SETTINGS_PADDING*2, board_size_icon_y, 64, 64), 6)
        elif (board_size_icon_x +SETTINGS_PADDING * 3 < mouse_x_pos < board_size_icon_x + SETTINGS_PADDING * 3 + mode_select_size):
            # LARGE MODE SELECT
            if (clicked[0] == 1 and CURRENT_MODE != LARGE_MODE):
                CURRENT_MODE = LARGE_MODE
                restartGame = True
            #pygame.draw.rect(DISPLAY, GREEN_HIGH_CONTRAST, (board_size_icon_x+SETTINGS_PADDING*3, board_size_icon_y, 64, 64), 6)
        elif (board_size_icon_x + SETTINGS_PADDING * 4 < mouse_x_pos < board_size_icon_x + SETTINGS_PADDING * 4 + mode_select_size):
            if (clicked[0] == 1 and CURRENT_MODE != XTREME_MODE):
                CURRENT_MODE = XTREME_MODE
                restartGame = True
            #pygame.draw.rect(DISPLAY, GREEN_HIGH_CONTRAST, (board_size_icon_x+SETTINGS_PADDING*4, board_size_icon_y, 64, 64), 6)
    #print(restartGame)
    if (CURRENT_MODE == SMALL_MODE):
        pygame.draw.rect(DISPLAY, GREEN_HIGH_CONTRAST, (board_size_icon_x+SETTINGS_PADDING, board_size_icon_y, 64, 64), 6)
        BOARD_SIZE = 4
    elif(CURRENT_MODE == MEDIUM_MODE):
        pygame.draw.rect(DISPLAY, GREEN_HIGH_CONTRAST, (board_size_icon_x+SETTINGS_PADDING*2, board_size_icon_y, 64, 64), 6)
        BOARD_SIZE = 6
    elif (CURRENT_MODE == LARGE_MODE):
        pygame.draw.rect(DISPLAY, GREEN_HIGH_CONTRAST, (board_size_icon_x+SETTINGS_PADDING*3, board_size_icon_y, 64, 64), 6)
        BOARD_SIZE = 8
    elif (CURRENT_MODE == XTREME_MODE):
        pygame.draw.rect(DISPLAY, GREEN_HIGH_CONTRAST, (board_size_icon_x+SETTINGS_PADDING*4, board_size_icon_y, 64, 64), 6)
        BOARD_SIZE = 10
    #else if ()
    else:
        #backIcon.fill((0,0,0),special_flags=pygame.BLEND_RGB_MULT)
        #backIcon.fill((JET_BLACK),special_flags=pygame.BLEND_RGB_ADD)
        fillIcon(backIcon,backIconColour)

    if (mainSettings):
        if (drawToggle(COLOUR_BLIND_ICON_X +SETTINGS_PADDING, COLOUR_BLIND_ICON_Y+16, 32, 128, COLOUR_BLIND_MODE, toggleOnHC, toggleOffHC, toggleOn, toggleOff)):
            COLOUR_BLIND_MODE = True
            restartGame = True
        else:
            COLOUR_BLIND_MODE = False
            restartGame = False

        if (drawToggle(COLOUR_BLIND_ICON_X + SETTINGS_PADDING, COLOUR_BLIND_ICON_Y + SETTINGS_PADDING_Y*2+16, 32, 128, PLAY_AUDIO, toggleOnHC, toggleOffHC, toggleOn, toggleOff)):
            PLAY_AUDIO = True
        else:
            PLAY_AUDIO = False

    #print("Audio is playing: " + str(PLAY_AUDIO))
    return True


def drawShape(box):
    colour = box[4]
    boxMidpoint = BOX_SIZE/2
    boxQuarter = int(BOX_SIZE/4)
    threeEights = int(BOX_SIZE * 0.375)
    oneThird = int(BOX_SIZE * 0.33)

    x = box[0]
    y= box[1]
    if (box[3] == CIRCLE):
        # Centres the circle to the centre of the box and decreases its size to it fits. 
        print("DRawin circle")
        pygame.draw.circle(DISPLAY, colour,((box[0]+(int(BOX_SIZE*0.5))), (box[1]+int(BOX_SIZE*0.5))),BOX_SIZE-30)
    elif (box[3] == SQUARE):
        pygame.draw.rect(DISPLAY, colour,((box[0] + int(BOX_SIZE * 0.25)), (box[1]+int(BOX_SIZE * 0.25)), (BOX_SIZE/2), (BOX_SIZE/2)))
    elif (box[3] == TRIANGLE):
        pygame.draw.polygon(DISPLAY, colour, [(box[0]+boxMidpoint, box[1]), (box[0],box[1]+BOX_SIZE), (box[0]+BOX_SIZE, box[1] + BOX_SIZE)])
    elif (box[3] == TILTED_HOURGLASS):
        #print("Drawing diamond")
        pygame.draw.polygon(DISPLAY, colour, [(box[0]+boxMidpoint, box[1]), (box[0],box[1]+boxMidpoint), (box[0]+BOX_SIZE, box[1] + boxMidpoint), (box[0]+boxMidpoint, box[1]+BOX_SIZE)])
    elif (box[3] == DIAMOND):
        pygame.draw.polygon(DISPLAY, colour, [(x+boxMidpoint, y), (x, y+boxMidpoint), (x+boxMidpoint, y+BOX_SIZE), (x+BOX_SIZE, y+boxMidpoint)])
    elif (box[3] == PENTAGON):
        pygame.draw.polygon(DISPLAY, colour, [(x+boxMidpoint, y), (x,y+int((boxQuarter+boxMidpoint)/2)), (x+boxQuarter, y+BOX_SIZE), (x+boxQuarter+boxMidpoint, y+BOX_SIZE), (x+BOX_SIZE, y+int((boxQuarter+boxMidpoint)/2))])
    elif (box[3] == HEXAGON):
        pygame.draw.polygon(DISPLAY, colour, [(x+boxQuarter, y), (x,y+boxMidpoint), (x+boxQuarter, y+BOX_SIZE), (x+BOX_SIZE-boxQuarter,y+BOX_SIZE), (x+BOX_SIZE, y+boxMidpoint), (x+BOX_SIZE-boxQuarter, y)])
    elif (box[3] == CROSS):
        pygame.draw.polygon(DISPLAY, colour, [(x+oneThird, y), (x+oneThird*2, y), (x+oneThird*2, y+oneThird),(x+BOX_SIZE, y+oneThird), (x+BOX_SIZE, y+oneThird*2), (x+oneThird*2, y+oneThird*2), (x+oneThird*2, y+BOX_SIZE), (x+oneThird, y+BOX_SIZE), (x+oneThird, y+oneThird*2),(x, y+oneThird*2),(x, y+oneThird), (x+oneThird, y+oneThird)])
    #pygame.display.update()
    #clock.tick(FRAME_RATE)

def revealAndCover(box, newSize):
    # Draw Background
    rect2 = pygame.draw.rect(DISPLAY, BLUE_SPACE_CADET, (box[0], box[1], BOX_SIZE, BOX_SIZE))
    # Draw Shape on top
    # Then draw the box
    drawShape(box)
    #print("Removing box with current newsize" + str(newSize))
    if (newSize>=0):
        print(newSize)
        if (newSize == 0):
            rect1 = pygame.draw.rect(DISPLAY, HONEYDEW, (box[0], box[1], 0, 0))
        else:
            rect1 = pygame.draw.rect(DISPLAY, HONEYDEW, (box[0], box[1], newSize, BOX_SIZE))
        pygame.display.update((rect1, rect2))
    # Therefore it will be Background --> Shape --> Box (where Box is the topmost level)
    clock.tick(FRAME_RATE)

first_selection = None
second_selection = None


def selectBox(index):
    global first_selection, second_selection
    if (first_selection == None):
        first_selection = boxes[index]
        for reveal in range(BOX_SIZE, (-REVEALSPEED)-1, - REVEALSPEED):
            revealAndCover(boxes[index],reveal)
    else:
        second_selection = boxes[index]
        for reveal in range(BOX_SIZE, (-REVEALSPEED)-1, - REVEALSPEED):
            #print(reveal)
            revealAndCover(boxes[index],reveal)

def countdown(num):
    start_time = pygame.time.get_ticks()
    while True:
        passed_time = pygame.time.get_ticks() - start_time
        if (passed_time > num):
            break
        

def box_manager():
    global first_selection
    global second_selection
    global currentlySelected
    global buttonPress
    global pressedEnter
    #print("Current selected box index " + str(currentlySelected))
    #print("Is the mouse moving " + str(isMouseMoving))
    for i in range(len(boxes)):
        mousePos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        #pygame.draw.rect(DISPLAY, (0, 0, 0), (boxes[i][0],boxes[i][1], BOX_SIZE, BOX_SIZE))
        if ((boxes[i][0] < mouse_x_pos < (boxes[i][0] + BOX_SIZE)) and (boxes[i][1] < mouse_y_pos < (boxes[i][1] + BOX_SIZE)) and not buttonPress):
            if (boxes[i][2] == False):
                pygame.draw.rect(DISPLAY, RED_DESIRE, (boxes[i][0], boxes[i][1], BOX_SIZE, BOX_SIZE))
            if (clicked[0] == 1 and boxes[i][2] == False):
                boxes[i][2] = True
                selectBox(i)
                '''
                if (first_selection == None):
                    first_selection = boxes[i]
                    for reveal in range(BOX_SIZE, (-REVEALSPEED)-1, - REVEALSPEED):
                        revealAndCover(boxes[i],reveal)
                else:
                    second_selection = boxes[i]
                    for reveal in range(BOX_SIZE, (-REVEALSPEED)-1, - REVEALSPEED):
                        revealAndCover(boxes[i],reveal)
                        '''
           # else:
                #pygame.draw.rect(DISPLAY, RED_DESIRE, (boxes[i][0], boxes[i][1], BOX_SIZE, BOX_SIZE))
                
        elif (isMouseMoving == False and buttonPress and boxes[currentlySelected][2] == False):
            pygame.draw.rect(DISPLAY, RED_DESIRE, (boxes[currentlySelected][0], boxes[currentlySelected][1], BOX_SIZE, BOX_SIZE))
            if (pressedEnter and boxes[currentlySelected][2] == False):
                pressedEnter = False
                boxes[currentlySelected][2] = True
                selectBox(currentlySelected)
                #pygame.time.wait(WAIT_TIME)


        if (first_selection != None and second_selection != None):
            #print("Its revealed.")
            if (first_selection[3] == second_selection[3] and first_selection[4] == second_selection[4]):
                print("It matches!")

            else:
                #pygame.time.wait(1000)
                countdown(500)
                for reveal in range(0, BOX_SIZE+REVEALSPEED, REVEALSPEED):
                    revealAndCover(first_selection,reveal)
                    revealAndCover(second_selection,reveal)
                first_selection[2] = False
                second_selection[2] = False
            first_selection = None
            second_selection = None
            


                
    

    #pygame.display.update()

def drawMainBoard():
    global boxes
    for i in boxes:
        if (i[2] == False):
            pygame.draw.rect(DISPLAY, HONEYDEW, (i[0],i[1], BOX_SIZE, BOX_SIZE))
        else:
            drawShape(i)
    #pygame.display.update()
    #clock.tick(FRAME_RATE)

def generateBoxes(amount):
    global boxes
    boxes = []
    icons = [] # Empty random permutation of colours and shapes.
    # This part of the code was taken from a OpenBSD licensed Github project.
    # The project is linked in the documentation. 
    currColourScheme = COLOURS
    if (COLOUR_BLIND_MODE):
        currColourScheme = COLOUR_BLIND_SCHEME
    for color in currColourScheme:
        for shapes in SHAPES:
            icons.append((shapes, color))
    #print("length of icons BEFORE is " + str(len(icons)))
    # This random seed improves on the taken algorithm, to make it "truly" random.
    random.seed() # RANDOMLY SEEDS FROM CURRENT TIME OF OS. TRULY RANDOM. 
    random.shuffle(icons) # Shuffles the array.
    numIconsUsed = int((BOARD_SIZE**2)/2)
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons) # Reshuffle. 
    #print("length of icons is " + str(len(icons)))
    for x in range(1, amount+1):
        for y in range(1, amount+1):
            #print("x is" + str(x) + " and y is " + str(y))
            #print(icons)
            tempx = X_MARGIN + SPACING * x  + BOX_SIZE * (x-1)
            tempy = Y_MARGIN + SPACING * y + BOX_SIZE * (y-1) + 50
            boxes.append([tempx, tempy, False, icons[0][0], icons[0][1]])
            del icons[0] # Deletes first element, so only two can have the same shape and colour
        
def generateBoard():
    shapes = []


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

last_time_ms = int(round(time.time() * 1000))
def handleKeyboardInputs():
    global currentlySelected, buttonPress
    global last_time_ms
    keyPresses = pygame.key.get_pressed()
    oldVal = currentlySelected
    diff_time_ms = int(round(time.time() * 1000)) - last_time_ms
    #print(diff_time_ms)
    if (diff_time_ms >= KEYBOARD_DELAY and buttonPress):
        if (keyPresses[pygame.K_UP]):
            if (currentlySelected != 0):
                currentlySelected-=1
        elif (keyPresses[pygame.K_DOWN]):
            if (currentlySelected != (BOARD_SIZE**2)-1):
                oldVal = currentlySelected
                currentlySelected+=1
        elif (keyPresses[pygame.K_RIGHT]):
            if ((currentlySelected + BOARD_SIZE) <= (BOARD_SIZE**2)-1):
                currentlySelected+=BOARD_SIZE
        elif (keyPresses[pygame.K_LEFT]):
            if ((currentlySelected - BOARD_SIZE) >= 0):
                currentlySelected-=BOARD_SIZE
        
        if (keyPresses[pygame.K_RETURN] or keyPresses[pygame.K_SPACE] or keyPresses[pygame.K_KP_ENTER]):
            pressedEnter = True
            print("")
        last_time_ms = int(round(time.time() * 1000))
    # If already selected, don't select again
    if (boxes[currentlySelected] == True):
        currentlySelected = oldVal

def update_events():
    global mouse_x_pos
    global mouse_y_pos
    global currentlySelected
    global isMouseMoving
    global buttonPress
    global pressedEnter
    global sliders
    global quitGame
    #print("Pressed enter is " + str(pressedEnter))
    isMouseMoving = False
    xMove = 0
    yMove = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            quitGame = True
            #pygame.display.quit()
            print("HELLO")
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x_pos, mouse_y_pos = event.pos
            isMouseMoving = True
            buttonPress = False
        elif event.type == MOUSEBUTTONUP:
            MOUSE_CLICKED = True
            mouse_x_pos, mouse_y_pos = event.pos
            #pos = pygame.mouse.get_pos()
           # for s in sliders:
            #    if (s.buttonRect.collidepoint(pos)):
             #       s.clicked = True # The slider has been hit. 
        elif event.type == pygame.KEYDOWN:
            buttonPress = True
            #pygame.time.set_timer(INPUT_HANDLER, KEYBOARD_DELAY)
            print(event.key)
            if (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                pressedEnter = True

            #for s in sliders:
              #      s.clicked = False # The slider has been hit. 


def toggleAudio():
    global PLAY_AUDIO
    #print("PLAY AUDIO IS " + str(PLAY_AUDIO))
    if (PLAY_AUDIO):
        pygame.mixer.music.unpause()
    else:
        print("PAUSING")
        pygame.mixer.music.pause()

def blinkBoxes():
    global boxes
    for i in range(len(boxes)):
        boxes[i][4] = PINK_HIGH_CONTRAST
    pygame.time.wait(500)
    for i in range(len(boxes)):
        boxes[i][4] = GREEN_HIGH_CONTRAST 
    pygame.time.wait(500)

def fadeInTrophy(image):
    global trophyIcon
    for i in range(0, 129):
        trophyIcon.set_alpha(i)
    pygame.display.update()
    #DISPLAY.blit(trophyIcon, (500, 200))
    

def gameWonAnimation():
    global start_time
    global restartGame
    global passed_time
    global highscoreText
    # Do some animation shit here
    #blinkBoxes()
    #blinkBoxes()
    #blinkBoxes()
    #pygame.transform.scale(trophyIcon, (1,1))
    #fadeInTrophy(trophyIcon)
    #pygame.time.wait(1000)
    # Reset timer
    #restartGame = True

def hasWonGame():
    global boxes
    
    for i in range(len(boxes)):
        if (boxes[i][2] == False):
            return False

    
    #print("WON THE GAME!")
    return True
    gameWonAnimation()
            
    '''
    for s in sliders:
        if (s.clicked):
            s.move()

    for s in sliders:
        s.draw_slider()
            #pygame.time.set_timer(INPUT_HANDLER, 0)
    
            if (event.key == pygame.K_UP):
                if (currentlySelected != 0 or currentlySelected != (BOARD_SIZE**2)-1):
                    currentlySelected-=1
            elif (event.key == pygame.K_DOWN):
                if (currentlySelected != (BOARD_SIZE**2)-1):
                    currentlySelected+=1
            elif (event.key == pygame.K_RIGHT):
                if ((currentlySelected + BOARD_SIZE) <= (BOARD_SIZE**2)-1):
                    currentlySelected+=BOARD_SIZE
            elif (event.key == pygame.K_LEFT):
                if ((currentlySelected - BOARD_SIZE) >= 0):
                    currentlySelected-=BOARD_SIZE
    '''

def quit():
    global quitGame
    global font
    del font
    print("CAN YOU SEE THIS?")
    #pygame.display.quit()
    print(quitGame)
    pygame.quit()
print("LAUNCHING GAME!")
main()
#input("Wtf")
