import ChessEngine
import pygame as pg

WIDTH = HEIGHT = 512
DIMENSION = 8
SQSIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}






def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pg.image.load("./images/" + piece + ".png")






def drawBoard(screen):
    colors  = [pg.Color("white"),pg.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            pg.draw.rect(screen, color, pg.Rect(c*SQSIZE, r*SQSIZE, SQSIZE, SQSIZE)) 


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(c*SQSIZE, r*SQSIZE, SQSIZE, SQSIZE))


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)






def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))

    # initialization
    gs = ChessEngine.GameState()
    load_images()
    running = True
    sqSelected = ()         # store last click of the user
    playerClick = []        # store clicks upto two clicks 

    # infinite loop
    while running:

        for e in pg.event.get():
            # Event handling
            if e.type == pg.QUIT:   # trigger for ending infinite loop
                running = False
            
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()       # (x, y) location fot the mouse
                col = location[0] // SQSIZE
                row = location[1] // SQSIZE


                # storing player clicks
                if sqSelected == (row, col):    # check for same input
                    sqSelected = ()
                    playerClick = []

                else:
                    sqSelected = (row, col)
                    playerClick.append(sqSelected)

                
                if len(playerClick) == 2:
                    move = ChessEngine.Move( playerClick[0], playerClick[1], gs.board )
                    print(move.getChessNotation())
                    gs.makeMove(move)

                    # reset input
                    sqSelected = ()
                    playerClick.clear()

            
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    gs.undoMove()
                
                

                





        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()




if __name__ == "__main__":
    main()