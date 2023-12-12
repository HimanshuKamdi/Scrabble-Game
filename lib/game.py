import random, time, sys

from lib.bag import Bag
from lib.board import Board
from lib.player import Player
from lib.dic import Dict
from lib.ai import AI_Player

class Game:
	def __init__(self, options={}):
		# print("INIT RAN")
		self.board = Board()
		self.bag = Bag()
		self.dict = Dict('./dics/sowpods.txt')
		self.turns = 0
		self.passes = 0
		self.points = 0
		self.words = []
		self.word = None
		self.human = None
		self.words_list = set()
		self.players_list = []
		self.players = 2
		# self.time_limit = options.get('time_limit', False)
		# self.end_time = time.time() + int(self.time_limit) * 60
		self.human_comp = options.get('human_comp', False)
		self.comp_comp = options.get('comp_comp', False)
		self.human_human = options.get('human_human', False)
		self.level = options.get('level','medium')
		self.comp_dict = Dict(f'./dics/easy.txt')
		self.chances=0

	def initialize_game(self):
		# print("initialize_game RAN")

		if self.human_comp:
			self.players_list.extend([ Player(), AI_Player()])
			self.players_list[0].name = input('\nWhat is your name?: ').upper()
			self.players_list[1].name = 'COMP'

			for p in self.players_list:
				p.draw_letters(self.bag)

			random.shuffle(self.players_list)
			self.current_player = self.players_list[0]
			self.prev_player = self.players_list[-1]

		elif self.comp_comp:
			self.players_list.extend([AI_Player(), AI_Player()])
			self.players_list[0].name = 'COMP1'
			self.players_list[1].name = 'COMP2'

			for p in self.players_list:
				p.draw_letters(self.bag)

			random.shuffle(self.players_list)
			self.current_player = self.players_list[0]
			self.prev_player = self.players_list[-1]

		elif self.human_human:
			self.human1 = Player()
			self.human2 = Player()
			self.players_list.extend([self.human1,self.human2])
			self.players_list[0].name = input('\nWhat is your name?: ').upper()
			self.players_list[1].name = input('\nWhat is your name?: ').upper()

			for p in self.players_list:
				p.draw_letters(self.bag)

			random.shuffle(self.players_list)
			self.current_player = self.players_list[0]
			self.prev_player = self.players_list[-1]

		else:
			print("Init else")

	def initialize_turn(self):
		# print("initialize_turn RAN")
		self.words = []
		if self.word:
			self.words.append(self.word.word)
			self.words.extend(list(map(lambda x: x[0], self.word.extra_words)))
			self.words_list = self.words_list.union(set(self.words))


		self.prev_player = self.current_player		
		
		self.current_player = self.players_list[self.turns % self.players]
		# if self.current_player is self.human or not self.human_comp:
		if self.turns==0:
			self.board.display(self.current_player.output)
			self.intial_display()
			self.display_turn_info(self.current_player)
		else:	
			if self.word:
				print("\nWords Played: {}".format(self.word.word))
				print("Words Formed: {}\t| Points:\t{}\n".format(self.words,self.points))
			else:
				if self.passes>0:
					print("Turn Passed")
					print("Passes",self.passes)
			print('\n==================================================================\n\n')
			self.board.display(self.current_player.output)
			self.display_turn_info(self.current_player)
		self.turns += 1

	def intial_display(self):
		# self.current_player = self.players_list[self.turns % self.players]
		# print("Initial display RAN")
		print('\n==================================================================\n')
		print("Players INFO")
		for p in self.players_list:
			print("\nPlayer:{}\t|\tTotal Points:{}\t|\tLetters Left in Bag: {} \n".format(p.name, p.score,len(self.bag.bag)))
			print("Letters On Rack:\t\u2551 {} \u2551\n".format(' - '.join(p.letters)))
		print('\n==================================================================\n')
		print("Input Instructions\n")
		print("1.Enter input in format \"intial_position\" \"direction\" \"word\"\n\tE.g h8 r start ")
		print("2.Valid Directions:\n\t\"r/h\" For rowise or horizontal\n\t\"c/v\" For column or vertical")
		print("3.Enter \"pass\" for passing the turn")


	def display_turn_info(self, p):
		# print("display_turn_info")
		print('\n==================================================================\n\n')
		print(f"{p.name}'s Turn")
		print("\nPlayer:{}\t|\tTotal Points:{}\t|\tLetters Left in Bag: {} \n\n".format(p.name, p.score,len(self.bag.bag)))
		print("Letters On Rack:\t\u2551 {} \u2551\n".format(' - '.join(p.letters)))
		# p.output.write(
		# 	"Letters Left in Bag: {}  | Words: {} for {} pts by {}\n\n".format(
		# 		len(self.bag.bag), self.words, self.points, self.prev_player.name
		# 	)
		# )
		# p.output.write("Time left: {} minutes\n".format(int((self.end_time - time.time()) / 60)))
		# print("\u2551 {} \u2551\n".format(' - '.join(p.letters)).center(70))

	def play_turn(self):
		# print("play_turn RAN")
		# print("Chances",self.chances)
		# self.chances+=1
		if self.human_comp and self.level == 'easy' and self.current_player.name == 'COMP':
			self.current_player.get_move(self.bag, self.board, self.comp_dict)
		elif self.human_comp and self.level == 'hard' and self.current_player.name == 'COMP':
			self.current_player.get_move(self.bag, self.board, self.dict, self.prev_player.letters)
		# elif self.comp_comp:
		# 	self.current_player.get_move(self.bag, self.board, self.dict,self.prev_player.letters)
		else:
			self.current_player.get_move(self.bag, self.board, self.dict)

		self.word = self.current_player.word

		if self.current_player.is_passing:
			self.passes += 1
			self.word = None
			self.words = []
			self.points = 0
		elif self.move_acceptable() and self.word.validate():
			if self.word.wild_tiles:
				self.board.wild_tiles_on_board.extend(self.word.wild_tiles)

			self.points = self.word.calculate_total_points()

			if self.turns == 1:
				self.points *= 2

			self.board.place(self.word.word, self.word.range)
			self.current_player.update_rack(self.bag)

			if self.current_player.full_bonus and len(self.bag.bag) > 0:
				self.points += 50

			self.current_player.update_score(self.points)
			self.passes = 0
		else:
				self.current_player.display_message(self.word.error_message)
				# if self.word.invalid_word:
				# 	self.handle_invalid_word()
				# else:
				self.play_turn()
		

	def racks_not_empty(self):
		# print("racks_not_empty RAN")
		for p in self.players_list:
			if len(p.letters) == 0:
				return False

		return True

	def move_acceptable(self):
		# if self.time_limit and self.time_over():
		# 	self.end_game()
		# 	return False

		return True

	def handle_invalid_word(self):
		# print("handle_invalid_word RAN")
		self.current_player.return_wild_tile()

		# if not self.challenge_mode:
		# 	self.play_turn()
		# else:
		self.passes += 1
		self.points = 0
		self.word.reset()

	# def set_time_limit(self):
	# 	try:
	# 		start_time = time.time()
	# 		self.end_time = start_time + int(self.time_limit) * 60
	# 	except ValueError:
	# 		print('\nTime limit should be a whole number (1, 2, etc)...')
	# 		self.time_limit = input('Please enter the time limit in minutes: ')
	# 		self.set_time_limit()

	# def time_over(self):
	# 	return time.time() >= self.end_time

	def decide_winner(self):
		# print("decide_winner RAN")
		bonus_getter = None
		bonus = 0

		for p in self.players_list:
			if len(p.letters) == 0:
				bonus_getter = p
			else:
				subt = 0

				try:
					for l in p.letters:
						subt += self.word.letter_points[l]

					self.player.update_score(-subt)
				except AttributeError:
					pass

				bonus += subt

		if bonus_getter:
			bonus_getter.update_score(bonus)

		scores = [player.score for player in self.players_list]
		points = max(scores)
		winner = self.players_list[scores.index(points)]

		return winner


	def end_game(self):
		# print("end_game RAN")
		self.remove_points()

		winner = self.decide_winner()

		for p in [self.current_player]:
			# if self.time_limit and self.time_over():
			# 	# p.output.write('\n==================================================================\n\n')
			# 	# p.output.write('TIME IS UP!\n'.center(70))
			# 	pass
			# else:
			print('\n==================================================================\n\n')
			print('GAME IS OVER!\n'.center(70))

			print('\n')

			for pl in self.players_list:
				print((str(pl) + '\n').center(70))
			print('\n')
			print('The winner is \033[1m{}\033[0m with \033[1m{}\033[0m points!\n'.format(winner.name, winner.score).center(85))
			print('\n==================================================================\n')
		sys.exit()

	def remove_points(self):
		for p in self.players_list:
			while p.letters:
				for l in p.letters:
					p.letters.remove(l)
					# p.update_score(-(self.prev_player.word.letter_points[l]))
					try:
						p.update_score(-(self.prev_player.word.letter_points[l]))
					except:
						pass

	def enter_game_loop(self):
		# try:
			self.initialize_game()
			while (self.racks_not_empty() and self.passes != 2 * self.players) :
				try:
					self.initialize_turn()
					self.play_turn()					
				except KeyboardInterrupt:
					answer = input('\nDo you want to end the game (y/n) ?: ').upper().strip()

					if answer.startswith('Y'):
						self.end_game()
						sys.exit()
					else:
						self.turns -= 1
			if self.passes == 2 * self.players:
				print("Turn Passed")
				print("Passes",self.passes)
			self.end_game()
			exit()
		# except Exception as e:
		# 	print(e)


