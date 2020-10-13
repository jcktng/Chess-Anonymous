"""
Main driver code to set up chess board.
"""
import pygame
import ChessEngine
from constants import WIDTH, HEIGHT, DIMENSION, SQ_SIZE, LIGHT, DARK
pygame.init()
IMAGES = {}
SOUNDS = {}
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')
colors = [LIGHT, DARK]

def loadSounds():
    """Loads sound effects for various events during the chess game."""
    events = ['start', 'end', 'move', 'capture', 'check', 'illegal', 'castle']
    for event in events:
        SOUNDS[event] = pygame.mixer.Sound("sounds/" + event + ".wav")

def loadImages():
    """Loads images for each piece."""
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wP", "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.smoothscale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    run = True
    clock = pygame.time.Clock()
    loadImages()
    loadSounds()

    game = ChessEngine.Chess()
    validMoves = game.validMoves()
    moveMade = False
    gameOver = False
    animate = False

    sqSelected = ()
    clicks = []
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # if 'z' is pressed, undo move
            # pops most recent move from movelog
            # ********subject to change*********
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    game.undo_move()
                    moveMade = True             # generate new valid moves if move is undone
                    animate = False
                    gameOver = False
                
                # reset game
                if event.key == pygame.K_r:
                    game = ChessEngine.Chess()
                    validMoves = game.validMoves()
                    sqSelected = ()
                    clicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

            if not gameOver:
                if event.type == pygame.MOUSEBUTTONDOWN:

                    loc = pygame.mouse.get_pos() # (x, y) position of mouse
                    col = loc[0] // SQ_SIZE
                    row = loc[1] // SQ_SIZE

                    piece = game.board[row][col]
                    # first click doesn't have a piece
                    if len(clicks) == 0 and piece == "--":
                        continue
                    
                    # second click is same as first click, cancel move
                    elif len(clicks) == 1 and (row, col) == sqSelected:
                        sqSelected = ()
                        clicks = []

                    else:
                        sqSelected = (row, col)
                        clicks.append(sqSelected)

                    # two valid clicks, make the move
                    if len(clicks) == 2:
                        move = ChessEngine.Move(clicks[0], clicks[1], game.board)

                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                game.make_move(validMoves[i])
                                if game.inCheck():
                                    SOUNDS['check'].play()
                                else:
                                    if validMoves[i].isCastle:
                                        SOUNDS['castle'].play()
                                    elif validMoves[i].isEnpassantMove:
                                        SOUNDS['capture'].play()
                                    elif move.endPiece == "--":
                                        SOUNDS['move'].play()
                                    else:
                                        SOUNDS['capture'].play()

                                moveMade = True
                                animate = True
                                print(move.chessNotation(clicks[0], clicks[1]))
                                sqSelected, clicks = (), []

                        if not moveMade:
                            print("Could not execute:", move.chessNotation(clicks[0], clicks[1]))
                            clicks = [sqSelected]

        if moveMade:
            if animate:
                animate_move(game.moveLog[-1], WIN, game.board, clock)
            validMoves = game.validMoves()
            moveMade = False
            animate = False

        draw_squares(WIN)
        highlightSquares(WIN, game, validMoves, sqSelected)
        draw_pieces(WIN, game.board)

        if game.checkmate:
            gameOver = True
            if game.whiteTurn:
                drawText(WIN, 'Black wins by checkmate!')
            else:
                drawText(WIN, 'White wins by checkmate!')

        elif game.stalemate:
            gameOver = True
            drawText(WIN, 'Stalemate!')
        pygame.display.update()
        
    # pygame.quit()

def drawText(win, text):
    font = pygame.font.SysFont("Helvetica", 32, True, False)
    textObj = font.render(text, 0, pygame.Color('Gray'))
    textLoc = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObj.get_width()/2, HEIGHT/2 - textObj.get_height()/2)
    win.blit(textObj, textLoc)
    textObj = font.render(text, 0, pygame.Color('Black'))
    win.blit(textObj, textLoc.move(2, 2))

def highlightSquares(win, gs, moves, sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if (gs.board[row][col][0] == 'w' and gs.whiteTurn) or (gs.board[row][col][0] == 'b' and not gs.whiteTurn):
            # highlight selected piece's square
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(pygame.Color('yellow'))
            win.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            # highlight moves available from the selected piece
            s.fill(pygame.Color('orange'))
            for move in moves:
                if move.startRow == row and move.startCol == col:
                    win.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def draw_squares(win):
    """Draws the chessboard."""
    win.fill(DARK)
    for row in range(DIMENSION):
        for col in range(row % 2, DIMENSION, 2):
            pygame.draw.rect(win, LIGHT, (row*SQ_SIZE, col*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(win, board):
    """Draws pieces on squares."""
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            # draw pieces on non-empty squares
            if piece != "--":
                # blit draws surface on top of another surface
                win.blit(IMAGES[piece], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animate_move(move, win, board, clock):
    """Adds some animation to moves."""
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSq = 3
    frameCount = (abs(dR) + abs(dC)) * framesPerSq
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        draw_squares(win)
        draw_pieces(win, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pygame.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(win, color, endSquare)
        if move.endPiece != "--":
            win.blit(IMAGES[move.endPiece], endSquare)
        
        win.blit(IMAGES[move.startPiece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)
    



if __name__ == "__main__":
    main()