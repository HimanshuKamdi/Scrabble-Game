import itertools, random
from lib.word import Word
from lib.player import Player
class AI_Player(Player):
  def get_move(self, bag, board, dic, opp_rack=[]):
    self.full_bonus = False
    self.is_passing = False

    words = []
    word_set = set()

    for n in range(2, len(self.letters) + 1):
      word_set = word_set.union(self.permute(n, dic))

    for word in word_set:
      for key in board.board.keys():
        word_d = Word(key, 'd', word, board, dic)
        word_r = Word(key, 'r', word, board, dic)

        if word_d.validate():
          words.append(word_d)

        if word_r.validate():
          words.append(word_r)

    if len(words) == 0:
      self.is_passing = True
      self.pass_letters(bag)
    else:
        best_move = words[0]
        best_points = best_move.calculate_total_points()
        opponent_potential_moves = []

        for word in words:
            move_points = word.calculate_total_points()            

            if len(opp_rack)>0 and set(word.word.split()).issubset(set(opp_rack)):
                move_points -= min(len(word.tiles),5) 

            if move_points  > best_points:
                best_move = word
                move_points = word.calculate_total_points()

        self.word = best_move

  def permute(self, n, dic):
    words = set()
    perms = itertools.permutations(self.letters, n)

    for perm in perms:
      if dic.valid_word(''.join(perm)):
        words.add(''.join(perm))

    return words

  def pass_letters(self, bag):
    if len(bag.bag)>0:
      passed_letters = random.sample(self.letters, min(3,len(bag.bag)))

      for l in passed_letters:
        if l in self.letters:
          self.letters.remove(l)  

        bag.put_back(passed_letters)
      self.draw_letters(bag, len(passed_letters))



