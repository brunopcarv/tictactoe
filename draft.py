# Authors: aqeelanwar and brunocarvalho
# Created by aqeelanwar: 12 March,2020, 7:06 PM
# Adapted by brunocarvalho: 04 August,2020, 10:32 AM
# Authors' Emails: aqeel.anwar@gatech.edu, b_per@encs.concordia.ca

from tkinter import *
import numpy as np
import math

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


class Board():
	# Board object
	def __init__(self, max_player_turn=True, start_board=np.zeros(shape=(3, 3))):
		self.board = start_board
		self.max_player_turn = max_player_turn

	def make_move(self, logical_position):
		if self.max_player_turn: # True for x and False for o
			self.board[logical_position[0],logical_position[1]] = 1
		else:
			self.board[logical_position[0],logical_position[1]] = -1
		self.max_player_turn = not self.max_player_turn
		# print("Possible moves: ", self.get_possible_moves())
		# print("max_player_turn: ", self.max_player_turn)
		# print("board: ", self.board)
		# print("is_terminal: ", self.is_terminal())
		# print("winner: ", self.get_winner())
		return self.board, self.max_player_turn

	def get_possible_moves(self):
		possible_moves = list()
		set_to = 1 if self.max_player_turn else -1

		for ix, iy in np.ndindex(self.board.shape):
			if self.board[ix, iy] == 0:
				temp = np.copy(self.board)
				temp[ix, iy] = set_to
				possible_moves.append(((ix, iy), temp))
		return possible_moves

	def get_winner(self):
		# Either someone wins or all grid occupied
		# winner = -1 (X winner), winner = 1 (O winner), winner = 0 (draw)
		if self.is_winner(-3):
			return -1
		elif self.is_winner(3):
			return 1
		elif self.is_board_complete():
			return 0
		else:
			return None

	def is_winner(self, player_sum):
		# Three in a row
		if np.any(np.sum(self.board, axis=0) == player_sum): return True
		# Three in a col
		if np.any(np.sum(self.board, axis=1) == player_sum): return True
		# Diagonals
		if np.trace(self.board) == player_sum: return True
		if np.trace(self.board[::-1]) == player_sum: return True
		return False

	def is_board_complete(self):
		x, y = np.where(self.board == 0)
		if len(x) == 0:
			return True
		else:
			return False

	def is_terminal(self):
		return self.get_winner() != None

class Agent():
	# Computer agent to play against user
	def __init__(self, current_board, max_player=True, my_turn=True):
		self.max_player = max_player
		self.my_turn = my_turn
		self.current_board = current_board


	def minimax(self, current_board, max_turn):
		board = Board(max_turn, current_board)
		if board.is_terminal():
			return board.get_winner(), None
		if max_turn: 
			value = -math.inf
			for move, child_board in board.get_possible_moves():
				value = max(value, self.minimax(child_board, False)[0])
			return value, move
		else:
			value = math.inf
			for move, child_board in board.get_possible_moves():
				value = max(value, self.minimax(child_board, True)[0])
			return value, move

	def get_best_move(self):
		_, best_move = self.minimax(self.current_board, self.max_player==self.my_turn)
		return best_move



class TicTacToe():
	# ------------------------------------------------------------------
	# Initialization Functions:
	# ------------------------------------------------------------------
	def __init__(self):
		self.window = Tk()
		self.window.title('Tic-Tac-Toe')
		self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
		self.canvas.pack()
		# Input from user in form of clicks
		self.window.bind('<Button-1>', self.click)

		self.initialize_board()
		self.player_X_turns = True
		self.player_X_starts = True

		self.board = Board(self.player_X_starts)
		self.board_status = self.board.board
		self.reset_board = False
		self.gameover = False
		self.tie = False
		self.X_wins = False
		self.O_wins = False

		self.X_score = 0
		self.O_score = 0
		self.tie_score = 0

	def mainloop(self):
		self.window.mainloop()

	def initialize_board(self):
		for i in range(2):
			self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

		for i in range(2):
			self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

	# ------------------------------------------------------------------
	# Drawing Functions:
	# The modules required to draw required game based object on canvas
	# ------------------------------------------------------------------

	def draw_O(self, logical_position):
		logical_position = np.array(logical_position)
		# logical_position = grid value on the board
		# grid_position = actual pixel values of the center of the grid
		grid_position = self.convert_logical_to_grid_position(logical_position)
		self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
								grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
								outline=symbol_O_color)

	def draw_X(self, logical_position):
		grid_position = self.convert_logical_to_grid_position(logical_position)
		self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
								grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
								fill=symbol_X_color)
		self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
								grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
								fill=symbol_X_color)



	# ------------------------------------------------------------------
	# Logical Functions:
	# The modules required to carry out game logic
	# ------------------------------------------------------------------

	def convert_logical_to_grid_position(self, logical_position):
		logical_position = np.array(logical_position, dtype=int)
		return (size_of_board / 3) * logical_position + size_of_board / 6

	def convert_grid_to_logical_position(self, grid_position):
		grid_position = np.array(grid_position)
		return np.array(grid_position // (size_of_board / 3), dtype=int)

	def is_grid_occupied(self, logical_position):
		if self.board_status[logical_position[0]][logical_position[1]] == 0:
			return False
		else:
			return True

	def click(self, event):
		grid_position = [event.x, event.y]
		logical_position = self.convert_grid_to_logical_position(grid_position)
		# if self.player_X_turns:
		if not self.is_grid_occupied(logical_position):
			self.draw_X(logical_position)
			self.board_status, self.player_X_turns = self.board.make_move(logical_position)

			# Agent turn
			agent = Agent(self.board_status, max_player=True, my_turn=True)
			logical_position = agent.get_best_move()
			self.draw_O(logical_position)
			self.board_status, self.player_X_turns = self.board.make_move(logical_position)

		# else:
		# 	if not self.is_grid_occupied(logical_position):
		# 		self.draw_O(logical_position)
		# 		self.board_status, self.player_X_turns = self.board.make_move(logical_position)





game_instance = TicTacToe()
game_instance.mainloop()