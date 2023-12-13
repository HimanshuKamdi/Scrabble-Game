import sys, re
from utility import Word

class Player:
	def __init__(self, inp=sys.stdin, outp=sys.stdout, name=None):
		self.input = inp
		self.output = outp
		self.name = None
		self.score = 0
		self.letters = []
		self.wild_tiles = []
		self.is_passing = False
		self.word = None
		self.full_bonus = False

	def draw_letters(self, bag, amount=7):
		for i in range(amount):
			self.letters.append(self.pick_from(bag))
		self.letters = list(re.sub('[^A-Z@]', '', ''.join(self.letters)))

	def update_rack(self, bag):
		aob = len(self.word.aob_list)
		for l in self.word.word:
			self.remove_tile(l)
		if len(self.letters) == 0:
			self.full_bonus = True
		if len(bag.bag) > 0:
			self.draw_letters(bag, min(len(self.word.word) - aob,len(bag.bag)))

	def update_score(self, points):
		self.score += points

	def get_move(self, bag, board, dic):
		self.wild_tiles = []
		self.is_passing = False
		self.full_bonus = False
		print('\nEnter your move :\t')
		player_input = input().lower().split()

		if len(player_input) == 0:
			self.display_message('Void input...')
			self.get_move(bag, board, dic)
		elif len(player_input) < 3 or len(player_input) > 3:
			if player_input[0] == 'pass':
				self.pass_letters(bag, board, dic)
				self.is_passing = True
			
			else:
				self.display_message('Make sure your input is correct (e.g. h8 r money)...')
				self.get_move(bag, board, dic)
		else:
			start, direction, word = player_input
			if  direction == 'h':
				direction = 'r' 
			if direction == 'c' or direction == 'v':
				direction = 'd' 
			if not re.fullmatch('[a-o]1[0-5]|[a-o][1-9]', start):
				self.display_message('Your starting square is not valid...')
				self.get_move(bag, board, dic)
			elif direction not in ['r', 'd']:
					self.display_message('Your direction should be either \'r\' for right or \'d\' for down...')
					self.get_move(bag, board, dic)
			else:
				self.word = Word(start, direction, word.upper(), board, dic)
				if not self.valid_letters():
					self.display_message('One or more letters are not on your rack...')
					self.get_move(bag, board, dic)

	def display_message(self, message):
		print('\n==================================================================\n')
		print(message.center(70))
		print('\n==================================================================\n\n')

	def __str__(self):
		return '{} has got {} points.'.format(self.name, self.score).center(70)

	def pick_from(self, bag):
		if bag:
			return bag.draw()

	def pass_letters(self, bag, board, dic):
		player_input = input('\nEnter the letter(s) you want to pass:').upper()
		passed_letters = list(re.sub('[^A-Z]', '', player_input))

		if len(player_input) == 0:
			self.display_message('Void input...')
			self.get_move(bag, board, dic)
		else:
			if self.valid_letters(passed_letters):
				for l in passed_letters:
					self.letters.remove(l)

				bag.put_back(passed_letters)
				self.draw_letters(bag, len(passed_letters))
			else:
				self.display_message("One or more letters are not on your rack...")
				self.get_move(bag, board, dic)

	def valid_letters(self, word=None):

		for l in (word or self.word.word):
			try:
				if l not in self.word.aob_list:
					if not self.letter_on_rack(word, l):
						return False
			except AttributeError:
				if not self.letter_on_rack(word, l):
					return False

		return True

	def letter_on_rack(self, word, l):
		if l not in self.letters or (word or self.word.word).count(l) > self.letters.count(l):
			return False
		return True

	def remove_tile(self, l):
		if l in self.word.aob_list:
			self.word.aob_list.remove(l)
		elif l not in self.word.aob_list:
			if l in self.letters:
				self.letters.remove(l)