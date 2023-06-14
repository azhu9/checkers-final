import pygame, sys
from pygame.locals import *

pygame.font.init()

##COLORS##
#             R    G    B 
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
SKYBLUE  = (123, 211, 247)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)
GOLD     = (255, 215,   0)
HIGH     = (160, 190, 255)

##DIRECTIONS##
NW = "northwest"
NE = "northeast"
SW = "southwest"
SE = "southeast"

class Game:
	#Initializes variables for Game Class
	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()
		
		self.gameState = "start"
		self.turn = BLUE
		self.selected_piece = None # a board location. 
		self.hop = False
		self.selected_legal_moves = []

		self.red_score = 0
		self.blue_score = 0

	#Call Setup window
	def setup(self):
		self.graphics.setup_window()

	#Game Event Loop
	def event_loop(self):
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos()) # what square is the mouse in?
		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)

		for event in pygame.event.get():

			if event.type == QUIT:
				self.terminate_game()
			
			if event.type == MOUSEBUTTONDOWN:
				if self.hop == False:
					if self.board.location(self.mouse_pos).occupant != None and self.board.location(self.mouse_pos).occupant.color == self.turn:
						self.selected_piece = self.mouse_pos

					elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece):

						self.board.move_piece(self.selected_piece, self.mouse_pos)
					
						if self.mouse_pos not in self.board.adjacent(self.selected_piece):
							self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))
						
							self.hop = True
							self.selected_piece = self.mouse_pos

						else:
							self.end_turn()

				if self.hop == True:					
					if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
						self.board.move_piece(self.selected_piece, self.mouse_pos)
						self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))

					if self.board.legal_moves(self.mouse_pos, self.hop) == []:
							self.end_turn()

					else:
						self.selected_piece = self.mouse_pos

	#Start Screen Event Loop
	def start_screen_loop(self):

		for event in pygame.event.get():
					
			if event.type == QUIT:
				self.terminate_game()
			
			# Changes board type
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.graphics.boardNumber = self.graphics.boardNumber + 1
					if self.graphics.boardNumber == 3:
						self.graphics.boardNumber = 0
					self.graphics.background = pygame.image.load(f'resources/{self.graphics.boards[self.graphics.boardNumber]}')
					print(self.graphics.boardNumber)
					print(self.graphics.boards[self.graphics.boardNumber])
			
			#checks if a mouse is clicked
			if event.type == MOUSEBUTTONDOWN:
				print("CLICKED")
				self.gameState = "play"

	#Update Display function
	def update(self):
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

	#Quit game 
	def terminate_game(self):	
		pygame.quit()
		sys.exit

	#Main function with game loop
	def main(self):
		self.setup()

		while True: # main game loop
			if self.gameState == "start":
				self.start_screen_loop()
				self.graphics.draw_start_menu()
			elif self.gameState == "play":
				self.event_loop()
				self.update()

	#Turn end function
	def end_turn(self):
		if self.turn == BLUE:
			self.turn = RED
		else:
			self.turn = BLUE

		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False

		if self.check_for_endgame():
			if self.turn == BLUE:
				self.red_score += 1
				self.graphics.draw_message("RED WINS!")
			else:
				self.blue_score += 1
				self.graphics.draw_message("BLUE WINS!")

	#Endgame function
	def check_for_endgame(self):
		for x in range(8):
			for y in range(8):
				if self.board.location((x,y)).color == BLACK and self.board.location((x,y)).occupant != None and self.board.location((x,y)).occupant.color == self.turn:
					if self.board.legal_moves((x,y)) != []:
						return False

		return True

class Graphics:
	#Initialize variables for Graphics class
	def __init__(self):
		self.caption = "Checkers"
  
		##BOARDS##
		self.boards = ["board.png","WienerBoard.jpg","ColoredWienerBoard.jpg"]
		self.boardsNAMES = ["Normal","Dr. Wiener","Red/Blue Dr. Wiener"]
		self.boardNumber = 0

		self.fps = 60
		self.clock = pygame.time.Clock()

		self.window_size = 600
		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.background = pygame.image.load(f'resources/{self.boards[self.boardNumber]}')

		self.square_size = self.window_size >> 3
		self.piece_size = self.square_size >> 1

		self.message = False

	#Setup window for graphics
	def setup_window(self):
		pygame.init()
		pygame.display.set_caption(self.caption)

	#Draw start menu function
	def draw_start_menu(self):
		self.screen.fill(SKYBLUE)
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.title = self.font_obj.render('CHECKERS', True, WHITE)
		self.font_obj = pygame.font.Font('freesansbold.ttf', 25)
		self.start_button = self.font_obj.render('CLICK ANYWHERE TO START', True, WHITE)
		self.start_button2 = self.font_obj.render('PRESS SPACE TO CHANGE BOARD', True, WHITE)
		self.font_obj = pygame.font.Font('freesansbold.ttf', 20)
		self.boardName = self.font_obj.render(f'{self.boardsNAMES[self.boardNumber]}', True, WHITE)
		self.screen.blit(self.title, (300 - self.title.get_width()/2, 250 - self.title.get_height()/2))
		self.screen.blit(self.start_button, (300 - self.start_button.get_width()/2, 305 + self.start_button.get_height()/2))
		self.screen.blit(self.start_button2, (300 - self.start_button2.get_width()/2, 340 + self.start_button2.get_height()/2))
		self.screen.blit(self.boardName, (300 - self.boardName.get_width()/2, 400 + self.boardName.get_height()/2))
		pygame.display.update()

	#Update display during game loop
	def update_display(self, board, legal_moves, selected_piece):
		self.screen.blit(self.background, (0,0))
		
		self.highlight_squares(legal_moves, selected_piece)
		self.draw_board_pieces(board)

		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		pygame.display.update()
		self.clock.tick(self.fps)

	#Draw board in game
	def draw_board_squares(self, board):
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )
	
	#Draw pieces in game
	def draw_board_pieces(self, board):
		for x in range(8):
			for y in range(8):
				if board.matrix[x][y].occupant != None:
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, self.pixel_coords((x,y)), self.piece_size) 

					if board.location((x,y)).occupant.king == True:
						pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x,y)), int (self.piece_size / 1.7), self.piece_size >> 2)

	#Store coordinates of pieces 
	def pixel_coords(self, board_coords):
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

	#Store coordinates of board
	def board_coords(self, pixel):
		return (pixel[0] // self.square_size, pixel[1] // self.square_size)

	#Show highlights when hovering piece
	def highlight_squares(self, squares, origin):
		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))	

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

	#Draw message on screen
	def draw_message(self, message):
		self.message = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size >> 1, self.window_size >> 1)

class Board:
	#Initializes matrix for board
	def __init__(self):
		self.matrix = self.new_board()

	#Creates new matrix and sets the board 
	def new_board(self):

		matrix = [[None] * 8 for i in range(8)]

		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0): 
					matrix[y][x] = Square(BLACK)

		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(RED)
			for y in range(5, 8):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(BLUE)

		return matrix

	def board_string(self, board):
		board_string = [[None] * 8] * 8 

		for x in range(8):
			for y in range(8):
				if board[x][y].color == WHITE:
					board_string[x][y] = "WHITE"
				else:
					board_string[x][y] = "BLACK"

		return board_string
	
		#Checks directionally for available moves
	def rel(self, dir, pixel):
		x = pixel[0]
		y = pixel[1]
		if dir == NW:
			return (x - 1, y - 1)
		elif dir == NE:
			return (x + 1, y - 1)
		elif dir == SW:
			return (x - 1, y + 1)
		elif dir == SE:
			return (x + 1, y + 1)
		else:
			return 0

	def adjacent(self, pixel):
		x = pixel[0]
		y = pixel[1]

		return [self.rel(NW, (x,y)), self.rel(NE, (x,y)),self.rel(SW, (x,y)),self.rel(SE, (x,y))]

	def location(self, pixel):
		x = pixel[0]
		y = pixel[1]

		return self.matrix[x][y]

	#All moves function
	def blind_legal_moves(self, pixel):
		x = pixel[0]
		y = pixel[1]
		if self.matrix[x][y].occupant != None:
			
			if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == BLUE:
				blind_legal_moves = [self.rel(NW, (x,y)), self.rel(NE, (x,y))]
				
			elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == RED:
				blind_legal_moves = [self.rel(SW, (x,y)), self.rel(SE, (x,y))]

			else:
				blind_legal_moves = [self.rel(NW, (x,y)), self.rel(NE, (x,y)), self.rel(SW, (x,y)), self.rel(SE, (x,y))]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	#Legal moves function
	def legal_moves(self, pixel, hop = False):
		x = pixel[0]
		y = pixel[1]
		blind_legal_moves = self.blind_legal_moves((x,y)) 
		legal_moves = []

		if hop == False:
			for move in blind_legal_moves:
				if hop == False:
					if self.on_board(move):
						if self.location(move).occupant == None:
							legal_moves.append(move)

						elif self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
							legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		else: # hop == True
			for move in blind_legal_moves:
				if self.on_board(move) and self.location(move).occupant != None:
					if self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
						legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		return legal_moves
	
	#Capture function
	def remove_piece(self, pixel):
		x = pixel[0]
		y = pixel[1]
		self.matrix[x][y].occupant = None

	#Move function
	def move_piece(self, pixel_start, pixel_end):
		start_x = pixel_start[0]
		start_y = pixel_start[1]
		end_x = pixel_end[0]
		end_y = pixel_end[1]

		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.remove_piece((start_x, start_y))

		self.king((end_x, end_y))

	#Checks if piece is at the edge of the board
	def is_end_square(self, coords):
		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False

	#Checks if piece is not on edge of the board
	def on_board(self, pixel):
		x = pixel[0]
		y = pixel[1]
		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True

	#Converts piece to king
	def king(self, pixel):
		x = pixel[0]
		y = pixel[1]
		if self.location((x,y)).occupant != None:
			if (self.location((x,y)).occupant.color == BLUE and y == 0) or (self.location((x,y)).occupant.color == RED and y == 7):
				self.location((x,y)).occupant.king = True 

class Piece:
	#Initializes attributes for pieces
	def __init__(self, color, king = False):
		self.color = color
		self.king = king

class Square:
	#Defines attributes for board color
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Square object

#Main function
def main():
	game = Game()
	game.main()

if __name__ == "__main__":
	main()