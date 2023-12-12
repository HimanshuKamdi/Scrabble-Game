import sys
from lib.game import Game

class StartGame:
    def __init__(self):
        self.options = {}
        print()
        print('SCRABBLE AI'.center(75))

        self.give_main_options()

    def give_main_options(self):
        # print('\n0 => INFO')
        print('1 => Human Vs computer')
        print('2 => Computer Vs computer')
        print('3 => Human Vs human')
        print('9 => Exit')

        action = input('\nChoose an option: ')

        # if action == '0':
        #     self.print_info()
        if action == '1':
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
        self.select_level()
        self.options['human_comp'] = True
        Game(self.options).enter_game_loop()

    def comp_against_comp(self):
        # self.options.update(self.give_secondary_options(computer=True))
        self.options['comp_comp'] = True
        Game(self.options).enter_game_loop()

    def human_against_human(self):
        self.options['human_human'] = True
        Game(self.options).enter_game_loop()

    def select_level(self):
        print("Select the mode")
        print('1 => Easy')
        print('2 => Medium')
        print('3 => Hard')
        print('9 => Previous Menu')
        print('0 => Exit')
        action = input('\nPick an action: ')
        if action == '1':
            self.options['level']='easy'
        elif action == '3':
            self.options['level']='hard'        
        elif action == '9':
            self.give_main_options()
        elif action == '0':
            sys.exit()
StartGame()