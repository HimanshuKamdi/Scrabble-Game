import sys
from lib.game import Game

class StartGame:
    def __init__(self):
        self.options = {}
        print()
        print('COMMANDLINE SCRABBLE'.center(50))

        self.give_main_options()

    def give_main_options(self):
        print('\n0 => INFO')
        print('1 => Human Vs computer')
        print('2 => Computer Vs computer')
        print('3 => Human Vs human')
        print('9 => Exit')

        action = input('\nChoose an option: ')

        if action == '0':
            self.print_info()
        elif action == '1':
            self.human_against_comp()
        elif action == '2':
            self.comp_against_comp()
        elif action == '3':
            self.human_against_human()
        elif action == '9':
            sys.exit()
        else:
            self.give_main_options()

    def print_info(self):
        info = open('info.txt', 'r').read()
        print(info)
        self.give_main_options()

    def human_against_comp(self):
        # self.options.update(self.give_secondary_options(computer=True))
        self.options['human_comp'] = True
        Game(self.options).enter_game_loop()

    def comp_against_comp(self):
        # self.options.update(self.give_secondary_options(computer=True))
        self.options['comp_comp'] = True
        Game(self.options).enter_game_loop()

    def human_against_human(self):
        self.options['human_human'] = True
        Game(self.options).enter_game_loop()

    def give_secondary_options(self, computer=False):
        print('1 => Start a new game on normal mode')
        # print('2 => Start a new game with time limit')
        print('9 => Go to the previous menu')
        print('0 => Exit')
        action = input('\nPick an action: ')
        if action == '1':
            return {}
        # elif action == '2':
        #     return {'time_limit': input('\nPlease enter the time limit in minutes: ')}
        elif action == '9':
            self.give_main_options()
        elif action == '0':
            sys.exit()

StartGame()