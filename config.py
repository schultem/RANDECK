import os,sys
from src.window_rect import WindowRect
from src.coord import Coord

class config(object):
    APP_NAME = "Random Deck Generator"
    TARGET_APP_NAME = "Hearthstone"
    APP_DESCRIPTION = TARGET_APP_NAME + ' ' + APP_NAME
    PACKAGE_PATH = sys.path[0]
    ICON_PATH = os.path.join(PACKAGE_PATH.replace("library.zip",""),"img","app.ico")
                                           
    HELP_MESSAGE = 'Navigate to select a hero for a new deck and then press "Randomize"'

    CARDS_PER_PAGE = 8
    PAGES_PER_HERO = 63
    DECK_SIZE = 32

    STANDARD_SCALE = WindowRect((0,0,1024,768)) #standard resolution to scale coords to

    CHOOSE_HERO = Coord(830,660)
    HERO_COORDS = [Coord(160,220),Coord(340,220),Coord(500,220),
                                 Coord(160,380),Coord(340,380),Coord(500,380),
                                 Coord(160,560),Coord(340,560),Coord(500,560)]

    CUSTOM_DECK = Coord(630,320)
    CHOOSE_CUSTOM_DECK = Coord(680,660)
 
    NEXT_PAGE = Coord(720,100)
    CARD_PAGE_COORDS = [Coord(150,270),Coord(300,270),Coord(460,270),Coord(640,270),
                                          Coord(150,530),Coord(300,530),Coord(460,530),Coord(640,530)]

    MENU_DELAY = 1
    PAGE_DELAY = 0.05 
    CLICK_DELAY = 0.025
