
from tkinter import *
import numpy as np
import random
import pygame
import sys
import math


my_tk = Tk()
my_tk.title("Connect 4 game")
my_tk.geometry("750x500")

img = PhotoImage(file="game_photo.png")
label = Label(  my_tk,image=img)
label.place(x=0, y=0)

my_label = Label(my_tk, text="All rights reserved to Mohammad Mubaslat & Hamzeh Saleh")
my_label.pack()
my_label.place(x=160, y=440)
my_label.config(font=("Courier", 11))


BLUE = (30, 144, 255)
BLACK = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
SQUARESIZE = 60
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                    board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True



def easy_button_fun():

    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def score_position(board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        return score

    def is_terminal_node(board):
        return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(
            get_valid_locations(board)) == 0

    def minimax(board, depth, alpha, beta, maximizingPlayer):
        valid_locations = get_valid_locations(board)
        is_terminal = is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, AI_PIECE):
                    return (None, 100000000000000)
                elif winning_move(board, PLAYER_PIECE):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, score_position(board, AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations



    def draw_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == PLAYER_PIECE:
                    pygame.draw.circle(screen, RED, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif board[r][c] == AI_PIECE:
                    pygame.draw.circle(screen, YELLOW, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()



    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 30)

    turn = random.randint(PLAYER, AI)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("You win!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        # # Ask for Player 2 Input
        if turn == AI and not game_over:

            # col = random.randint(0, COLUMN_COUNT-1)
            # col = pick_best_move(board, AI_PIECE)
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                # pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Computer win!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(1500)
            my_tk.destroy()




def friend_button_fun():
 #   newWindow = Toplevel(my_tk)
 #   newWindow.geometry("750x500")
 #   Label(newWindow, image=img).pack()

    def draw_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    pygame.init()
    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()
    myfont = pygame.font.SysFont("monospace", 30)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True


                # # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                print_board(board)
                draw_board(board)
                turn += 1
                turn = turn % 2
                if game_over:
                    pygame.time.wait(1500)
                    my_tk.destroy()



def computer_button_fun():
    newWindow2 = Toplevel(my_tk)
    newWindow2.geometry("750x500")
    Label(newWindow2, image=img).pack()

    my_label = Label(newWindow2, text="Select game level :" )
    my_label.pack()
    my_label.place(x=270, y=170)
    my_label.config(font=("Courier", 15))

    easy_button = Button(newWindow2, text='Easy',height=2 , width=20 ,  command= easy_button_fun)
    easy_button.pack()
    easy_button.place(x=320, y=230)

    med_button = Button(newWindow2, text='Normal',height=2 , width=20 ,  command= easy_button_fun)
    med_button.pack()
    med_button.place(x=320, y=300)

    hard_button = Button(newWindow2, text='Hard', height=2, width=20 ,  command= easy_button_fun)
    hard_button.pack()
    hard_button.place(x=320, y=370)

friend_button = Button(my_tk, text='Play with friend',height=2 , width=30, command= friend_button_fun)
friend_button.pack()
friend_button.place(x=300, y=250)

computer_button = Button(my_tk, text='Play with computer',height=2 , width=30, command=computer_button_fun)
computer_button.pack()
computer_button.place(x=300, y=350)

my_tk.mainloop()


