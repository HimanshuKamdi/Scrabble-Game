# class Dict:
#   def __init__(self, dic):
#     self.dict = open(dic).read().splitlines()

#   def valid_word(self, word):
#     return word in self.dict
  
from pygtrie import StringTrie

class Dict:
    def __init__(self, dic):
        self.trie = self._create_trie(dic)

    def _create_trie(self, dic):
        trie = StringTrie()
        with open(dic, 'r') as file:
            for line in file:
                word = line.strip().upper()
                trie[word] = True
        return trie

    def valid_word(self, word):
        return word in self.trie

