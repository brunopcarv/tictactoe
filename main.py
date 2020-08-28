#!/usr/bin/env python
# -*- coding: utf-8 vi:noet
# Authors: aqeelanwar and brunocarvalho
# Created by aqeelanwar: 12 March,2020, 7:06 PM
# Adapted by brunocarvalho: 28 August,2020, 10:32 AM
# Authors' Emails: aqeel.anwar@gatech.edu, b_per@encs.concordia.ca

from tkinter import *
import numpy as np
import math

from board import Board

from agents import DummyAgent, AgentAlphaBetaPruning

BOARD_SIZE = 600
SYMBOL_SIZE = (BOARD_SIZE / 3 - BOARD_SIZE / 8) / 2
SYMBOL_THICKNESS = 50
SYMBOL_X_COLOR = '#EE4035'
SYMBOL_O_COLOR = '#0492CF'
GREEN_COLOR = '#7BC043'
BACKGROUND_COLOR = '#FFFFFF'

class TicTacToe():
	# ------------------------------------------------------------------
	# Initialization Functions:
	# ------------------------------------------------------------------
	def __init__(self):
		self.window = Tk()
		self.window.title('Tic-Tac-Toe')
		self.canvas = Canvas(self.window,
		 width=BOARD_SIZE,
		 height=BOARD_SIZE,
		 bg=BACKGROUND_COLOR)
		self.canvas.pack()
		# Input from user in form of clicks
		self.window.bind('<Button-1>', self.click)

		self.initialize_board()
		self.player_X_turns = True
		self.player_X_starts = True

		self.board = Board(max_player_turn=not self.player_X_starts)
		self.board_status = self.board.board
		self.reset_board = False

		self.X_score = 0
		self.O_score = 0
		self.tie_score = 0

	def mainloop(self):
		self.window.mainloop()

	def initialize_board(self):
		for i in range(2):
			self.canvas.create_line((i + 1) * BOARD_SIZE / 3, 0, (i + 1) * BOARD_SIZE / 3, BOARD_SIZE)

		for i in range(2):
			self.canvas.create_line(0, (i + 1) * BOARD_SIZE / 3, BOARD_SIZE, (i + 1) * BOARD_SIZE / 3)

	def play_again(self):
		self.initialize_board()
		self.player_X_starts = not self.player_X_starts
		self.board = Board(max_player_turn=not self.player_X_starts, start_board=np.zeros(shape=(3, 3)))
		self.board_status = self.board.board
		self.reset_board = False
		if not self.player_X_starts:
			self.agent_play_dummy()

	def agent_play_dummy(self):
		if not self.board.is_terminal():
			# Agent turn
			agent = DummyAgent()
			agent_move = agent.choose_move(self.board_status)
			if not agent_move == None:
				self.draw_O(agent_move)
				self.board_status, self.player_X_turns = self.board.make_move(agent_move)
				self.canvas.update()

	def agent_play(self):
		if not self.board.is_terminal():
			# Agent turn
			if False:
				self.agent_play_dummy()
			else: #Smart play
				agent = AgentAlphaBetaPruning(self.board_status, max_player=True, my_turn=True)
				logical_position = agent.get_best_move()
				self.draw_O(logical_position)
				self.canvas.update()
				self.board_status, self.player_X_turns = self.board.make_move(logical_position)



	# ------------------------------------------------------------------
	# Drawing Functions:
	# ------------------------------------------------------------------

	def draw_O(self, logical_position):
		logical_position = np.array(logical_position)
		# logical_position = grid value on the board
		# grid_position = actual pixel values of the center of the grid
		grid_position = self.convert_logical_to_grid_position(logical_position)
		self.canvas.create_oval(grid_position[0] - SYMBOL_SIZE, grid_position[1] - SYMBOL_SIZE,
								grid_position[0] + SYMBOL_SIZE, grid_position[1] + SYMBOL_SIZE, width=SYMBOL_THICKNESS,
								outline=SYMBOL_O_COLOR)

	def draw_X(self, logical_position):
		grid_position = self.convert_logical_to_grid_position(logical_position)
		self.canvas.create_line(grid_position[0] - SYMBOL_SIZE, grid_position[1] - SYMBOL_SIZE,
								grid_position[0] + SYMBOL_SIZE, grid_position[1] + SYMBOL_SIZE, width=SYMBOL_THICKNESS,
								fill=SYMBOL_X_COLOR)
		self.canvas.create_line(grid_position[0] - SYMBOL_SIZE, grid_position[1] + SYMBOL_SIZE,
								grid_position[0] + SYMBOL_SIZE, grid_position[1] - SYMBOL_SIZE, width=SYMBOL_THICKNESS,
								fill=SYMBOL_X_COLOR)


	def display_gameover(self):

		if self.board.get_winner() == -1:
			self.X_score += 1
			text = 'You win!'
			color = SYMBOL_X_COLOR
		elif self.board.get_winner() == 1:
			self.O_score += 1
			text = 'Computer wins'
			color = SYMBOL_O_COLOR
		else:
			self.tie_score += 1
			text = 'Its a tie'
			color = 'gray'

		self.canvas.delete("all")
		self.canvas.create_text(BOARD_SIZE / 2, BOARD_SIZE / 3, font="cmr 40 bold", fill=color, text=text)

		score_text = 'Scores \n'
		self.canvas.create_text(BOARD_SIZE / 2, 5 * BOARD_SIZE / 8, font="cmr 30 bold", fill=GREEN_COLOR,
								text=score_text)

		score_text = 'You:           ' + str(self.X_score) + '\n'
		score_text += 'Computer: ' + str(self.O_score) + '\n'
		score_text += 'Tie:             ' + str(self.tie_score)
		self.canvas.create_text(BOARD_SIZE / 2, 3 * BOARD_SIZE / 4, font="cmr 20 bold", fill=GREEN_COLOR,
								text=score_text)
		self.reset_board = True

		score_text = 'Click to play again \n'
		self.canvas.create_text(BOARD_SIZE / 2, 15 * BOARD_SIZE / 16, font="cmr 16 bold", fill="gray",
								text=score_text)


	# ------------------------------------------------------------------
	# Logical Functions:
	# The modules required to carry out game logic
	# ------------------------------------------------------------------

	def convert_logical_to_grid_position(self, logical_position):
		logical_position = np.array(logical_position, dtype=int)
		return (BOARD_SIZE / 3) * logical_position + BOARD_SIZE / 6

	def convert_grid_to_logical_position(self, grid_position):
		grid_position = np.array(grid_position)
		return np.array(grid_position // (BOARD_SIZE / 3), dtype=int)

	def is_grid_occupied(self, logical_position):
		if self.board_status[logical_position[0]][logical_position[1]] == 0:
			return False
		else:
			return True

	# Mouse click event handler
	def click(self, event):
		grid_position = [event.x, event.y]
		logical_position = self.convert_grid_to_logical_position(grid_position)

		if not self.reset_board:
			if not self.is_grid_occupied(logical_position):

				# User turn
				self.draw_X(logical_position)
				self.canvas.update()
				self.board_status, self.player_X_turns = self.board.make_move(logical_position)

				# Agent turn
				self.agent_play()

			# Check if game is concluded
			if self.board.is_terminal():
				self.display_gameover()

		else:  # Play Again
			self.canvas.delete("all")
			self.play_again()



game_instance = TicTacToe()
game_instance.mainloop()