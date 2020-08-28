#!/usr/bin/env python
# -*- coding: utf-8 vi:noet
# Agent player objects

import numpy as np
import math

from board import Board

class AgentAlphaBetaPruning():
	# ------------------------------------------------------------------
	# Agent to be coded:
	# ------------------------------------------------------------------
	def __init__(self, current_board, max_player=True, my_turn=True):
		self.max_player = max_player
		self.my_turn = my_turn
		self.current_board = current_board

	def alphabeta(self, current_board, max_turn, depth, alpha, beta):
		board = Board(max_turn, current_board)
		if board.is_terminal():
			return board.get_winner(), None
		if max_turn: 
			value = -math.inf
			value_dict = {None: value}
			for move, child_board in board.get_possible_next_states():
				value = max(value, self.alphabeta(child_board, False, depth+1, alpha, beta)[0])
				alpha = max(alpha, value)
				value_dict[move] = value
				if alpha >= beta:
					break
			move = max(value_dict, key=value_dict.get)
			return value_dict[move], move
		else:
			value = math.inf
			value_dict = {None: value}
			for move, child_board in board.get_possible_next_states():
				value = min(value, self.alphabeta(child_board, True, depth+1, alpha, beta)[0])
				beta = min(beta, value)
				value_dict[move] = value
				if beta <= alpha:
					break
			move = min(value_dict, key=value_dict.get)
			return value_dict[move], move

	def get_best_move(self):
		_, best_move = self.alphabeta(self.current_board, True, 0, -math.inf, math.inf)
		return best_move


class AgentMinimax():
	# ------------------------------------------------------------------
	# Agent to be coded:
	# ------------------------------------------------------------------
	def __init__(self, current_board, max_player=True, my_turn=True):
		self.max_player = max_player
		self.my_turn = my_turn
		self.current_board = current_board

	def minimax(self, current_board, max_turn, depth):
		board = Board(max_turn, current_board)
		if board.is_terminal():
			return board.get_winner(), None
		if max_turn: 
			value_dict = {None: -math.inf}
			for move, child_board in board.get_possible_next_states():
				value_dict[move] = self.minimax(child_board, False, depth+1)[0]
			move = max(value_dict, key=value_dict.get)
			return value_dict[move], move
		else:
			value_dict = {None: math.inf}
			for move, child_board in board.get_possible_next_states():
				s = ' ' * depth
				value_dict[move] = self.minimax(child_board, True, depth+1)[0]
			move = min(value_dict, key=value_dict.get)
			return value_dict[move], move

	def get_best_move(self):
		_, best_move = self.minimax(self.current_board, True, 0)
		return best_move

class DummyAgent():
	# ------------------------------------------------------------------
	# Dummy agent
	# ------------------------------------------------------------------
	def __init__(self):
		pass
	def choose_move(self, current_board):
		import random
		_board = Board(True, current_board)
		possible_moves = _board.get_possible_next_states()
		return random.choice(possible_moves)[0]
