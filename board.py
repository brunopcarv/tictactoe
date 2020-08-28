#!/usr/bin/env python
# -*- coding: utf-8 vi:noet
# Board object

import numpy as np
import math

class Board():
	# Board object
	def __init__(self, max_player_turn=False, start_board=np.zeros(shape=(3, 3))):
		self.board = start_board
		self.max_player_turn = max_player_turn
		self.first_turn = True

	def make_move(self, logical_position):
		if not self.max_player_turn: # True for X and False for O
			self.board[logical_position[0],logical_position[1]] = -1
		else:
			self.board[logical_position[0],logical_position[1]] = 1
		if self.max_player_turn:
			self.first_turn = False
		self.max_player_turn = not self.max_player_turn
		return self.board, self.max_player_turn

	def get_possible_next_states(self):
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