import re

class Board:
    def __init__(self):
        self.wild_tiles_on_board = []
        self.initialize_board()
        self.place_bonus()

    def display(self,output):
        t_line = u'\u2550\u2550\u2550\u2566'
        m_line = u'\u2550\u2550\u2550\u256C'
        b_line = u'\u2550\u2550\u2550\u2569'
        hor, ver = u'\u2551', u'\u2550'
        lcu, rcu = u'\u2554', u'\u2557'
        lcm, rcm = u'\u2560', u'\u2563'
        lcd, rcd = u'\u255A', u'\u255D'

        row_number = 15

        print('\n     a   b   c   d   e   f   g   h   i   j   k   l   m   n   o')
        print('   {}'.format(lcu + t_line * 14 + ver * 3 + rcu))

        for row in self.rows:
            if row_number < 10:
                print('{}  '.format(row_number), end='')
            else:
                print('{} '.format(row_number), end='')

            for spot in row:
                if self.board[spot] == 'h8':
                    print('{}\x1b[32m{} \x1b[00m'.format(hor, self.board[spot]), end='')
                elif self.board[spot] == '3w':
                    print('{}\x1b[31m{} \x1b[00m'.format(hor, self.board[spot]), end='')
                elif self.board[spot] == '2w':
                    print('{}\x1b[35m{} \x1b[00m'.format(hor, self.board[spot]), end='')
                elif self.board[spot] == '3l':
                    print('{}\x1b[34m{} \x1b[00m'.format(hor, self.board[spot]), end='')
                elif self.board[spot] == '2l':
                    print('{}\x1b[36m{} \x1b[00m'.format(hor, self.board[spot]), end='')
                else:
                    print('{}\033[1m {} \033[0m'.format(hor, self.board[spot]), end='')

            print('{} {}'.format(hor, row_number))

            row_number -= 1

            if row_number > 0:
                print('   {}'.format(lcm + m_line * 14 + ver * 3 + rcm))
            else:
                print('   {}'.format(lcd + b_line * 14 + ver * 3 + rcd))

        print('     a   b   c   d   e   f   g   h   i   j   k   l   m   n   o')
        return

    def calculate_bonus(self, word_range):
        bonus = {'word': {}, 'letter': {}}
        for square in word_range:
            if self.board[square] == '2w':
                bonus['word'][square] = 2
            elif self.board[square] == '3w':
                bonus['word'][square] = 3
            elif self.board[square] == '2l':
                bonus['letter'][square] = 2
            elif self.board[square] == '3l':
                bonus['letter'][square] = 3
        return bonus

    def valid_range(self, word_range, word, direction):
        for i, s in enumerate(word_range):
            if i == 0:
                if direction == 'd':
                    if self.occupied(s, 'r', self.up_or_left):
                        return False
                else:
                    if self.occupied(s, 'd', self.up_or_left):
                        return False

            if i == len(word_range) - 1:
                if direction == 'd':
                    if self.occupied(s, 'r', self.down_or_right):
                        return False
                else:
                    if self.occupied(s, 'd', self.down_or_right):
                        return False

            if self.board[s] != word[i] and re.fullmatch('[A-Z]', self.board[s]):
                return False
        return True

    def place(self, letters, word_range):
        for l, s in zip(letters, word_range):
            self.board[s] = l

    def up_or_left(self, square, direction):
        if direction == 'r':
            return square[0] + str(int(square[1:]) + 1)
        else:
            return chr(ord(square[0]) - 1) + square[1:]

    def down_or_right(self, square, direction):
        if direction == 'r':
            return square[0] + str(int(square[1:]) - 1)
        else:
            return chr(ord(square[0]) + 1) + square[1:]

    def occupied(self, square, direction, func):
        letter_ascii = ord(self.board.get(func(square, direction), '.')[0])

        return letter_ascii in range(65, 91)

    def square_occupied(self, square, direction):
        flag1 = self.occupied(square, direction, self.down_or_right)
        flag2 = self.occupied(square, direction, self.up_or_left)
        return flag1 or flag2

    def initialize_board(self):
        self.board = {}
        self.rows = []
        for i in range(1, 16):
            row = []
            for l in range(ord('a'), ord('p')):
                self.board[chr(l) + str(i)] = ' '
                row.append(chr(l) + str(i))

            self.rows.append(row)
        self.rows.reverse()

    def place_bonus(self):
        for key in self.board:
            if key =='h8':				
                self.board[key] = '\u2606'
            if key in 'a1 a8 a15 h15 o15 h1 o8 o1'.split():
                self.board[key] = '3w'

            if key in 'b2 c3 d4 e5 b14 c13 d12 e11 n2 m3 l4 k5 n14 m13 l12 k11'.split():
                self.board[key] = '2w'

            if key in 'b6 b10 n6 n10 f2 f6 f10 f14 j2 j6 j10 j14'.split():
                self.board[key] = '3l'

            if key in 'a4 a12 c7 c9 d1 d8 d15 g3 g7 g9 g13 h4 h12 o4 o12 m7 m9 l1 l8 l15 i3 i7 i9 i13'.split():
                self.board[key] = '2l'
