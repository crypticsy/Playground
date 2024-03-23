import os
import pygame as pg

from PIL import Image, ImageSequence



# Screen components
BOARD_WIDTH = BOARD_HEIGHT = 512
HOME_SCREEN_WIDTH =  512
HOME_SCREEN_HEIGHT = 700
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8                       # a chess board is 8 X 8 cells
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15                        # for animation
BORDER_EDGE_PADDING = 60
TILE_LABEL_PADDING = 35

# color values
background_black = pg.Color("#191919")
selected_tile_color = pg.Color('#2E8BC0')
moved_tile_color = pg.Color('#BDF0D6')
movable_tile_color = '#8BD1E4'
capture_tile_color = '#D04040'
dark_grey = '#4a4949'

# Path for the current file
base_path = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(base_path, 'assets', 'fonts')
image_path = os.path.join(base_path, 'assets', 'images')
gif_path = os.path.join(base_path, 'assets', 'gif')
icon_path = os.path.join(image_path, "logo.ico")

# custom fonts
cour = os.path.join(font_path, "courbd.ttf")
intro_rust = os.path.join(font_path, "IntroRust-Base.otf")
sourceSans = os.path.join(font_path, "SourceSansProBold.ttf")
comfortaa = os.path.join(font_path, "comfortaa_bold.ttf")

        




class AnimatedSpriteObject(pg.sprite.Sprite):
    """ Create a gif animation from a list of images """
    
    def __init__(self, x, bottom, images):
        pg.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = (x, bottom)) 
        self.image_index = 0

    def update(self):
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[self.image_index]
        


def addText(screen, text, x, y, color, font, font_size=20):
    """ Adds text to the screen """
    
    font = pg.font.Font(font, font_size)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    

def loadGIF(filename):
    """ Loads a GIF file and returns a list of frames """
    
    pilImage = Image.open(filename)
    frames = []
    for frame in ImageSequence.Iterator(pilImage):
        frame = frame.convert('RGBA')
        pygameImage = pg.image.fromstring(frame.tobytes(), frame.size, frame.mode).convert_alpha()
        frames.append(pygameImage)
        
    return frames