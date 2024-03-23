""" 
--⪢ Handling the AI moves.
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"                   # Hide pygame support information

import glob, sys
import pygame as pg
import pygame_menu
from multiprocessing import Process, Queue
from pygame._sdl2.video import Window, WINDOWPOS_CENTERED

import ChessEngine
import ChessAI

from Utils import *






# Image dictionary
IMAGES = {}

# Load all the images of each individual chess piece to be displayed
for file in glob.glob(os.path.join(image_path, '*')):           # find all the file in the images directory regardless of extension
    piece_name = os.path.split(file)[1].split('.')[0]           # find the piece name for the particular image
    IMAGES[piece_name] = pg.image.load(file)






def draw_board(screen):
    """ Draw the squares on the board """

    global colors
    colors  = [ pg.Color("white"), pg.Color("grey") ]                                               # colors of the board
    
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c)%2)]                                                             # find the color based on even or odd position
            # draw the rectangle shape in the row and column
            pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE + BORDER_EDGE_PADDING, r*SQ_SIZE + BORDER_EDGE_PADDING, SQ_SIZE, SQ_SIZE) )
                
        
    
def highlight_squares(screen, game_state, valid_moves, square_selected):
    """ Highlight square selected and moves for the particular piece. """

    if len(game_state.move_log) > 0:
        last_move = game_state.move_log[-1]
        s = pg.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(150)
        s.fill(moved_tile_color)
        screen.blit(s, (last_move.end_col * SQ_SIZE + BORDER_EDGE_PADDING, last_move.end_row * SQ_SIZE + BORDER_EDGE_PADDING))

    if square_selected != ():
        row, col = square_selected

        if game_state.board[row][col][0] == ('w' if game_state.white_to_move else 'b'):             # square_selected is a piece that can be moved
            
            # highlight selected square
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(200)               
            s.fill(selected_tile_color)
            screen.blit(s, (col * SQ_SIZE + BORDER_EDGE_PADDING, row * SQ_SIZE + BORDER_EDGE_PADDING))

            s.set_alpha(130)  
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    hightlight_color = movable_tile_color if move.piece_captured == "--" else capture_tile_color
                    s.fill(pg.Color(hightlight_color))                                              # highlight moves from that square
                    screen.blit(s, (move.end_col * SQ_SIZE + BORDER_EDGE_PADDING, move.end_row * SQ_SIZE + BORDER_EDGE_PADDING))



def draw_pieces(screen, board):
    """ Draw the pieces on the board using the current game state """

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]                                                                     # get the piece from the board
            if piece != "--":                                                                       # if empty piece go to the next piece
                screen.blit( IMAGES[piece], pg.Rect(c*SQ_SIZE + BORDER_EDGE_PADDING, r*SQ_SIZE + BORDER_EDGE_PADDING, SQ_SIZE, SQ_SIZE))        # draw piece in the row and column



def draw_move_log(screen, game_state, font):
    """ Draw the move log at the right side of the screen """

    move_log_rect = pg.Rect(BOARD_WIDTH + BORDER_EDGE_PADDING, BORDER_EDGE_PADDING, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    pg.draw.rect(screen, background_black, move_log_rect)

    move_log = game_state.move_log
    column_length = 15
    
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1).rjust(4, " ") + '. ' + str(move_log[i]).ljust(column_length, " ") + " "
        if i + 1 < len(move_log):                                                                   # make sure black made a move
            move_string += str(move_log[i + 1]).ljust(column_length, " ")
        move_texts.append(move_string)
    
    # Styling values
    moves_per_row = 1
    move_limit = 20
    padding = 10
    line_spacing = 8
    text_y = padding + move_limit * (line_spacing + 16)
    
    move_texts= move_texts[::-1][:move_limit]                                                      # reverse the list so the most recent move is at the top

    # add a text saying "last move"
    addText(screen, "Last move", BOARD_WIDTH + BORDER_EDGE_PADDING * 2 - padding * 2, text_y + BORDER_EDGE_PADDING + padding, pg.Color('grey'), intro_rust, 8)
    
    # add a label for each color
    label_string = " "*4 + "White".center(column_length, " ") + " " + "Black".center(column_length, " ")
    addText(screen, label_string, BOARD_WIDTH + BORDER_EDGE_PADDING * 3.25, BORDER_EDGE_PADDING + padding//2, pg.Color('grey'), intro_rust, 10)
    
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, pg.Color('white'))
        text_location = move_log_rect.move(padding + BORDER_EDGE_PADDING, text_y)
        screen.blit(text_object, text_location)
        text_y -= text_object.get_height() + line_spacing    



def draw_GameState(screen, game_state, valid_moves, square_selected, move_log_font):
    """ Responsible for all the graphics within a game state """

    draw_board(screen)                                                              # draw squares on the board
    highlight_squares(screen, game_state, valid_moves, square_selected )            # add in piece highlighting and move suggestion (later)
    draw_pieces(screen, game_state.board)                                           # draw pieces on top of the board
    draw_move_log(screen, game_state, move_log_font)                                # draw the move log






def animate_move(move, screen, board, clock):
    """ Animating a move """

    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col

    frames_per_square = 10                                                          # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square

    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        
        draw_board(screen)
        draw_pieces(screen, board)
        
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = pg.Rect(move.end_col * SQ_SIZE + BORDER_EDGE_PADDING, move.end_row * SQ_SIZE + BORDER_EDGE_PADDING, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(screen, color, end_square)
        
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = pg.Rect(move.end_col * SQ_SIZE + BORDER_EDGE_PADDING, enpassant_row * SQ_SIZE + BORDER_EDGE_PADDING, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)

        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], pg.Rect(col * SQ_SIZE + BORDER_EDGE_PADDING, row * SQ_SIZE + BORDER_EDGE_PADDING, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        
        clock.tick(200)



def draw_player_turn(screen, player):
    """ Draw the player turn at the top of the screen """
    white_color, black_color = ('White', dark_grey) if player else (dark_grey, 'White')
    
    # add a black rectangle behind the text
    turn_log_rect = pg.Rect(0, 0, BORDER_EDGE_PADDING * 2 + BOARD_WIDTH, BORDER_EDGE_PADDING)
    pg.draw.rect(screen, background_black, turn_log_rect)
    
    # add the label for white player
    font = pg.font.Font(intro_rust, 18)
    text_object = font.render('White turn', True, pg.Color(white_color))
    text_location = pg.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT ).move(BORDER_EDGE_PADDING, BORDER_EDGE_PADDING//3)
    screen.blit(text_object, text_location)
    
    # add the label for black player
    text_object = font.render('Black turn', True, pg.Color(black_color))
    text_location = pg.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT ).move(BOARD_WIDTH - BORDER_EDGE_PADDING , BORDER_EDGE_PADDING//3)
    screen.blit(text_object, text_location)
    
    pg.display.flip()
    


def draw_end_game_text(screen, text):
    """ Draw the end text. """
    
    font = pg.font.Font(intro_rust, 28)
    text_object = font.render(text, True, pg.Color(dark_grey))
    
    # Create a transparent surface.
    alpha_img = pg.Surface(screen.get_size(), pg.SRCALPHA)
    # Fill it with white and the desired alpha value.
    alpha_img.fill((255, 255, 255, 140))
    
    # Blit the alpha surface onto the text surface and pass BLEND_RGBA_MULT.
    screen.blit(alpha_img, (0,0), special_flags=pg.BLEND_RGBA_MULT)
    
    
    # Center the font by using font BOARD_WIDTH and BOARD_HEIGHT 
    text_location = pg.Rect(0, 0, BOARD_WIDTH , BOARD_HEIGHT ).move(BOARD_WIDTH / 2 - text_object.get_width() / 2 + BORDER_EDGE_PADDING, BOARD_HEIGHT / 2 - text_object.get_height() / 2 + BORDER_EDGE_PADDING)

    screen.blit(text_object, text_location)
    text_object = font.render(text, True, pg.Color("#ffeb00"))
    screen.blit(text_object, text_location.move(1, 0))












def chess_game():
    """ Main function that handles user input and graphics """
    
    # PyGame initialization
    pg.init()
    clock = pg.time.Clock()
    pg.display.set_icon(IMAGES['logo'])                # add icon to the pg window
    pg.display.set_caption(' Chess')                   # add title to the pg window
    
    # set size of the pg window
    screen = pg.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH + BORDER_EDGE_PADDING * 2, BOARD_HEIGHT + BORDER_EDGE_PADDING * 2))               
    screen.fill(background_black)                              # add background color to the pg window

    # align the game in the center of screen
    window = Window.from_display_module()
    window.position = WINDOWPOS_CENTERED
    
    move_log_font = pg.font.Font(sourceSans, 13)

    # GameEngine initialization
    game_state = ChessEngine.GameState()
    running = True
    sq_selected = ()             # store last click of the user
    player_click = []            # store clicks up to two clicks 
    move_finder_process = None   # allow multi processing      
    
    valid_moves = game_state.get_all_valid_moves()
    move_made = False           # flag variable for when a move is made
    animate = False             # flag variable for when a move needs to be animated
    game_over = False           # flag variable for when game is over
    ai_thinking = False         # flag variable for when the AI is finding best move
    move_undone = False         # flag variable for when the move is undone
    
    # add the labels to the chess board
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # add text at the top left corner of the square
            text_color = pg.Color(dark_grey)
            font = pg.font.Font(sourceSans, 12)
            
            # if the first coloumn, then add the row number
            if c == 0:
                text = font.render(str(8-r), True, text_color)
                text_rect = text.get_rect(center=(c*SQ_SIZE + SQ_SIZE//8 + TILE_LABEL_PADDING, r*SQ_SIZE + SQ_SIZE//2 + BORDER_EDGE_PADDING))
                screen.blit(text, text_rect)
            
            # if the last row, then add the column label
            if r == DIMENSION - 1:
                text = font.render(chr(ord('a') + c), True, text_color)
                text_rect = text.get_rect(center=(c*SQ_SIZE + SQ_SIZE//2 + BORDER_EDGE_PADDING, r*SQ_SIZE + SQ_SIZE - 10 + BORDER_EDGE_PADDING * 2 - TILE_LABEL_PADDING))
                screen.blit(text, text_rect)    
    
    # draw the first turn
    draw_player_turn(screen, game_state.white_to_move)     

    # infinite loop
    while running:

        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)                 # check if the human is controlling the turn

        for e in pg.event.get():                            # for each event in event queue

            if e.type == pg.QUIT:                           # trigger for ending infinite loop
                running = False
                return homeScreen()

            elif not game_over and e.type == pg.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = pg.mouse.get_pos()               # (x, y) location fot the mouse
                    col = (location[0] - BORDER_EDGE_PADDING) // SQ_SIZE
                    row = (location[1] - BORDER_EDGE_PADDING) // SQ_SIZE

                    # storing player clicks
                    if sq_selected == (row, col) or col >= 8:   # in case the click is same as previous click, reset player clicks
                        sq_selected = ()
                        player_click.clear()

                    else:                                       # else update the new click position
                        sq_selected = (row, col)
                        player_click.append(sq_selected)

                    
                    if len(player_click) == 2:              # when 2 unique clicks have been identified
                        move = ChessEngine.Move( player_click[0], player_click[1], game_state.board )
                        
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])

                                move_made = True
                                animate = True

                                # reset input
                                sq_selected = ()
                                player_click.clear()
                                break
                            
                        else:
                            player_click = [sq_selected]


            elif e.type == pg.KEYDOWN and e.key == pg.K_z:      # trigger for undoing a move
                game_state.undo_move()
                move_made = True
                animate = False
                game_over = False

                if ai_thinking:
                    move_finder_process.terminate()
                    ai_thinking = False

                move_undone = True
            
            elif e.type == pg.KEYDOWN and e.key == pg.K_r:      # trigger for resetting the board
                game_state = ChessEngine.GameState()
                valid_moves = game_state.get_all_valid_moves()
                sq_selected = ()
                player_click.clear()
                move_made = False
                animate = False
                game_over = False

                if ai_thinking:
                    move_finder_process.terminate()
                    ai_thinking = False
                    
                move_undone = True

        # AI move finder
        if not game_over and not human_turn and not move_undone:

            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()                          # store and pass data between threads
                move_finder_process = Process(target=ChessAI.find_best_move, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None: 
                    ai_move = ChessAI.find_random_move(valid_moves)
                 
                game_state.make_move(ai_move)
                move_made = True
                animate = True
                ai_thinking = False


        if move_made:
            if animate : animate_move(game_state.move_log[-1], screen, game_state.board, clock )             # animate the move made by the user
            valid_moves = game_state.get_all_valid_moves()
            move_made = False
            animate = False
            move_undone = False
            draw_player_turn(screen, game_state.white_to_move)
            
        if not game_over:
            draw_GameState(screen, game_state, valid_moves, sq_selected, move_log_font)
        
        if game_state.check_mate or game_state.stale_mate: 
            game_over = True
            win_txt = 'Stalemate' if game_state.stale_mate else 'Black wins by checkmate' if game_state.white_to_move else 'White wins by checkmate'
            draw_end_game_text(screen, win_txt)


        clock.tick(MAX_FPS)
        pg.display.flip()



def splashScreen():
    
    pg.init()
    screen = pg.display.set_mode((500, 300), pg.NOFRAME)
    screen.fill(background_black)
    
    window = Window.from_display_module()
    window.position = WINDOWPOS_CENTERED
    

    CLOCK = pg.time.Clock()
    CLOCK.tick(200)

    # add gif to the screen
    gifFrameList = loadGIF(os.path.join(gif_path, "giphy.gif"))
    animated_sprite = AnimatedSpriteObject(500 // 2, 280, gifFrameList)
    all_sprites = pg.sprite.Group(animated_sprite)

    val = 0
    pg.display.update() 
    
    # Game loop
    while True:
        pg.display.set_icon(pg.image.load(icon_path))          # add icon to the pg window
        pg.display.set_caption(' Chess')                       # add title to the pg window

        all_sprites.update()
        all_sprites.draw(screen)
                
        # add a progress bar at the bottom of the window
        pg.draw.rect(screen, background_black, (0, 280, 500, 20))
        pg.draw.rect(screen, pg.Color('White'), (0, 280, val, 20))
        
        addText(screen, "{:.0f} %".format(val/500 * 100), 475, 265, background_black, sourceSans, font_size=16)
        addText(screen, "V 0.1", 475, 15, pg.Color('#212121'), sourceSans, font_size=12)
        addText(screen, "Loading . . . ", 45, 270, pg.Color('Grey'), sourceSans, font_size=12)
        
        if val >= 500: break
        val += 10
            
        CLOCK.tick(23)
        pg.display.flip()
        
        


def upate_player_one(index, value):
    global player_one
    
    player_one = value
    
def update_player_two(index, value):
    global player_two
    
    player_two = value
        
def homeScreen():
    global player_one, player_two
        
    # if a human is playing white, then this will be True, else False
    player_one = True       

    # if a human is playing black, then this will be True, else False
    player_two = True  
    
    pg.init()
    screen = pg.display.set_mode((HOME_SCREEN_WIDTH, HOME_SCREEN_HEIGHT), pg.NOFRAME)
    
    darker_grey = "#808080"
    
    window = Window.from_display_module()
    window.position = WINDOWPOS_CENTERED
    
    pg.display.set_icon(pg.image.load(icon_path))          # add icon to the pg window
    pg.display.set_caption(' Chess')                       # add title to the pg window
    
    background_image = pygame_menu.baseimage.BaseImage(
        image_path=os.path.join(image_path, "main_chess.png"),
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    
    theme = pygame_menu.themes.Theme(   title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                                        cursor_color=background_black,
                                        selection_color=background_black,
                                        background_color=background_image,
                                        widget_font=pygame_menu.font.FONT_OPEN_SANS_BOLD,
                                        widget_font_color=pg.Color(darker_grey),
                                        widget_font_antialias=True,
                                        widget_selection_effect=pygame_menu.widgets.LeftArrowSelection())

    menu = pygame_menu.Menu(    height=HOME_SCREEN_HEIGHT, 
                                width=HOME_SCREEN_WIDTH, 
                                title="", 
                                theme=theme)
    
    # add the selector for white piece as either a human or AI
    menu.add.selector(  'White : ', 
                        [('AI', False), ('Human', True)], 
                        default=player_one, 
                        onchange=upate_player_one,
                        align=pygame_menu.locals.ALIGN_CENTER, 
                        font_name=intro_rust, 
                        font_color=pg.Color(darker_grey), 
                        font_size=18, 
                        margin=(0, 10))
    
    # add the selector for black piece as either a human or AI
    menu.add.selector(  'Black : ', 
                        [('AI', False), ('Human', True)],
                        default=player_two, 
                        onchange=update_player_two,
                        align=pygame_menu.locals.ALIGN_CENTER, 
                        font_name=intro_rust, 
                        font_color=pg.Color(darker_grey), 
                        font_size=18, 
                        margin=(0, 10))
    
    # add the play button to start the game
    menu.add.button(    'Play', 
                        chess_game, 
                        align=pygame_menu.locals.ALIGN_CENTER, 
                        font_name=intro_rust, 
                        font_color=pg.Color(darker_grey), 
                        font_size=18, 
                        margin=(0, 10))
    
    # add the quit button to exit the game
    menu.add.button(    'Quit', 
                        sys.exit, 
                        align=pygame_menu.locals.ALIGN_CENTER, 
                        font_name=intro_rust, 
                        font_color=pg.Color(darker_grey), 
                        font_size=18, 
                        margin=(0, 220))
    
    menu.add.label('')

    menu.mainloop(screen)

    pg.display.flip()

    

if __name__ == "__main__":
    # initialize the game
    
    splashScreen()
    homeScreen()