import random, re
from pygtrie import StringTrie

class Bag:
	def __init__(self):
		self.bag = []
		self.fill_bag()

	def fill_bag(self):
		self.bag.extend(['Q','Z','J','X','K'])

		for i in range(2):
			self.bag.extend(['F','H','V','W','Y','B','C','M','P'])

		for i in range(3):
			self.bag.extend(['G'])

		for i in range(4):
			self.bag.extend(['D','U','S','L'])

		for i in range(6):
			self.bag.extend(['T','R','N'])

		for i in range(8):
			self.bag.extend(['O'])

		for i in range(9):
			self.bag.extend(['I','A'])

		for i in range(12):
			self.bag.extend(['E'])

	def draw(self):
		random.shuffle(self.bag)
		try:
			return self.bag.pop()
		except :
			return 

	def put_back(self, letters):
		self.bag.extend(letters)
		

class Word:
  def __init__(self, start, direction, word, board, dic):
    self.start = start
    self.dict = dic
    self.direction = direction
    self.word = word
    self.board = board

    self.valid = False
    self.wild_tiles = []
    self.extra_words = []
    self.invalid_word = False

    self.range = self.set_range()
    self.aob_list = self.set_aob_list()
    self.letter_points = self.set_letter_points()

  def process_extra_words(self):
    check_list = []
    aob_list = self.aob_list.copy()

    for i, square in enumerate(self.range):
      extra_word = [[self.word[i]], [square]]

      if self.board.board[square] in aob_list and self.board.square_occupied(square, self.direction):
        del aob_list[aob_list.index(self.board.board[square])]
        check_list.append(True)

      elif not(self.board.square_occupied(square, self.direction)):
        check_list.append(True)

      else:
        self.extra_words.append(self.set_extra_word(square, extra_word))

        if self.dict.valid_word(self.extra_words[-1][0]):
          check_list.append(True)
        else:
          self.invalid_word = self.extra_words[-1][0]
          self.extra_words = []
          check_list.append(False)

    return not (False in check_list)

  def calculate_total_points(self):
    if not self.range:
      return 0

    bonus = self.board.calculate_bonus(self.range)
    self.word_bonus = bonus.get('word', None)
    self.letter_bonus = bonus.get('letter', None)

    points = self.calculate_word_points(self.word, self.range)

    for word, w_range in self.extra_words:
      points += self.calculate_word_points(word, w_range)

    return points

  def reset(self):
    self.extra_words = []
    self.word = None

  def valid_move(self):
    if not self.range:
      return False

    for square in self.range:
      if self.aob_list:
        return True
      elif self.board.square_occupied(square, self.direction):
        return True

    if self.start == 'h8':
      return True

    return False

  def validate(self):
    if self.valid:
      return True
    else:
      if all(i in self.aob_list for i in self.word):
        self.error_message = 'Move was illegal...'
        self.invalid_word = True
        return False
      
      if not self.valid_move():
        self.error_message = 'Move was illegal...'
        return False

      if not self.dict.valid_word(self.word):
        self.error_message = 'Word {} is not in dictionary...'.format(self.word)
        self.invalid_word = True
        return False

      if not self.process_extra_words():
        self.error_message = 'Extra word {} is not in the dictionary...'.format(self.invalid_word)
        self.invalid_word = True
        return False
      
      self.valid = True
      return True

  def set_range(self):
    if self.direction == "r":
      squares = self.set_range_to_right()
    else:
      squares = self.set_range_to_down()

    for s in squares:
      if not re.fullmatch('[a-o]1[0-5]|[a-o][1-9]', s):
        return False

    if not self.board.valid_range(squares, self.word, self.direction):
      return False

    return squares

  def set_range_to_right(self):
    last = chr((ord(self.start[0]) + len(self.word)))
    letter_range = list(range(ord(self.start[0]), ord(last)))
    return list(map(lambda x: chr(x) + self.start[1:], letter_range))

  def set_range_to_down(self):
    last = int(self.start[1:]) - len(self.word)
    number_range = list(range(int(self.start[1:]), last, -1))
    return list(map(lambda x: self.start[0] + str(x), number_range))

  def set_aob_list(self):
    aob_list = []
    if self.range:
      for i, spot in enumerate(self.range):
        if self.board.board[spot] == self.word[i]:
          aob_list.append(self.word[i])
        else:
          self.valid = False
    return aob_list

  def set_up_or_left_extra_word(self, square, extra_word):
    while self.board.occupied(square, self.direction, self.board.up_or_left):
      square = self.board.up_or_left(square, self.direction)
      extra_word[0].insert(0, self.board.board[square])
      extra_word[1].insert(0, square)

  def set_down_or_right_extra_word(self, square, extra_word):
    while self.board.occupied(square, self.direction, self.board.down_or_right):
      square = self.board.down_or_right(square, self.direction)
      extra_word[0].append(self.board.board[square])
      extra_word[1].append(square)

  def set_extra_word(self, square, extra_word):
    self.set_up_or_left_extra_word(square, extra_word)
    self.set_down_or_right_extra_word(square, extra_word)
    extra_word[0] = ''.join(extra_word[0])

    return extra_word

  def set_letter_points(self):
    points = {}

    for letter in list('AEILNORSTU'):
      points[letter] = 1

    for letter in list('DG'):
      points[letter] = 2

    for letter in list('BCMP'):
      points[letter] = 3

    for letter in list('FHVWY'):
      points[letter] = 4

    for letter in list('JX'):
      points[letter] = 8

    for letter in list('QZ'):
      points[letter] = 10

    points['K'] = 5

    return points

  def calculate_word_points(self, word, w_range):
    word_points = 0
    for l, s in zip(word, w_range):
      if self.letter_bonus:
        word_points += self.letter_bonus.get(s, 1) * self.letter_points[l]
      else:
        word_points += self.letter_points[l]

    if self.word_bonus:
      for s in w_range:
        if not self.aob_list: 
          word_points *= self.word_bonus.get(s, 1)

    return word_points
		

class Dict:
    def __init__(self, dic):
        self.trie = self.create_trie(dic)

    def create_trie(self, dic):
        trie = StringTrie()
        with open(dic, 'r') as file:
            for line in file:
                word = line.strip().upper()
                trie[word] = True
        return trie

    def valid_word(self, word):
        return word in self.trie


