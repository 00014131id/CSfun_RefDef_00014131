from tkinter import *
import numpy as np
import random

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4045'
symbol_O_color = '#1232CF'
Green_color = '#7BC234'

class TicTacToe_Game:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))
        self.X_score = self.O_score = self.tie_score = 0
        self.reset_board = False

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, outline=symbol_O_color)

    def convert_logical_to_grid_position(self, logical_position):
        grid_position = [(i + 0.5) * size_of_board / 3 for i in logical_position]
        return grid_position

    def convert_grid_to_logical_position(self, grid_position):
        logical_position = [int(grid_position[0] / (size_of_board / 3)),
                            int(grid_position[1] / (size_of_board / 3))]
        return logical_position

    def display_gameover(self):
        if self.X_wins:
            self.X_score += 1
            text, color = 'Winner: Player 1 (X)', symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text, color = 'Winner: Player 2 (O)', symbol_O_color

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 40 bold", fill=color, text=text)
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text='Scores \nPlayer 1 (X): {}\nPlayer 2 (O): {}'.format(
                                    self.X_score, self.O_score))
        self.canvas.create_text(size_of_board / 2, 3.5 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text='Click to play again')
        self.reset_board = True

    def is_grid_occupied(self, logical_position):
        if self.board_status[int(logical_position[0])][int(logical_position[1])] != 0:
            return True
        else:
            return False

    def is_winner(self, player):
        player = -1 if player == 'X' else 1
        for i in range(3):
            if (self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player or
                self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player):
                return True
        return (self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player or
                self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player)

    def is_tie(self):
        return np.count_nonzero(self.board_status) == 9

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        self.O_wins = self.is_winner('O')
        self.tie = self.is_tie()
        return self.X_wins or self.O_wins or self.tie

    def bind_events(self):
        self.window.bind('<Button-1>', self.click)

    def reset_game(self):
        self.canvas.delete("all")
        self.player_X_turns = True
        self.X_wins = False
        self.O_wins = False
        self.tie = False
        self.initialize_board()
        self.board_status = np.zeros(shape=(3, 3))
        self.reset_board = False
        self.bind_events()
    def play_move(self, logical_position):
        if self.is_grid_occupied(logical_position):
            return False

        symbol = 'X' if self.player_X_turns else 'O'

        if symbol == 'X':
            self.draw_X(logical_position)
            self.board_status[logical_position[0]][logical_position[1]] = -1
        else:
            self.draw_O(logical_position)
            self.board_status[logical_position[0]][logical_position[1]] = 1

        self.player_X_turns = not self.player_X_turns
        if self.is_gameover():
            self.display_gameover()
        return True
    
    def make_random_move(self):
        available_moves = np.argwhere(self.board_status == 0)
        if len(available_moves) > 0:
            move = random.choice(available_moves)
            self.play_move(move)

    def click(self, event):
        logical_position = self.convert_grid_to_logical_position([event.x, event.y])
        if not self.reset_board:
            if self.player_X_turns and not self.is_grid_occupied(logical_position):
                self.play_move(logical_position)
                if not self.is_gameover():
                    self.make_random_move()
        else:
            self.reset_game()

game_instance = TicTacToe_Game()
game_instance.mainloop()

