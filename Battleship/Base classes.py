class Board (object):
# class for a battle ship game board for one player
# size and ships are variable

    def __init__(self, n_row, n_col, player_name = ''):
    # Creates a new, empty game board of size n_row 8 n_col for player, name optional
        self. player_name = player_name
        self. n_row = n_row
        self. n_col = n_col
        self. tiles_hit = []
        # all tiles start out not hit (status 'O')
        for i in range(n_row):
            self. tiles_hit. append( ['O'] * n_col)
        # Ships to hit have to be added manually with add_ship
        self. ships = []
        self. n_ships = 0
        self. ships_sunk = 0
        

    def __repr__(self):
    # Print should show the tiles hit with 'O' not hit, 'M' a miss and 'X' a hit
        res = (self. player_name + '\n' +
               '  ' + ' '.join(str(i) for i in range(self. n_col)) + '\n')
        # print indeces for rows and columns to make identification easier
        for i in range(self. n_row):
            res += str(i) + ' '
            for j in range(self. n_col):
                res = res + str(self. tiles_hit[i][j]) + ' '
            res += '\n'
        # print row index and row entries afterwards for all columns
        return res

    def add_ship(self, pos_x, pos_y):
    # Adds a 1 tile ship to the game board, check if ship is valid or duplicated
        if not type(pos_x) == int or not type(pos_y) == int:
            print('Positions are not valid integers!')
        elif 0 > pos_x or pos_x > self. n_row or 0 > pos_y or pos_y > self. n_col:
            print('Positions are not on the board! Use smaller positions!')
        elif (pos_x, pos_y) in self. ships:
            print('This ship already exists, not added!')
        else:
        # if positions are vald coordinates and ship does not exist yet, add ship
            self. ships. append( (pos_x, pos_y) )
            self. n_ships += 1

    def take_shot(self, pos_x, pos_y):
    # Shoots at position (pos_x, pos_y), check if valid or duplicated
        if not type(pos_x) == int or not type(pos_y) == int:
            print('Positions are not valid integers!')
        elif 0 > pos_x or pos_x > self. n_row or 0 > pos_y or pos_y > self. n_col:
            print('Positions are not on the board! Use smaller positions!')
        elif self. tiles_hit[pos_x][pos_y] != 'O':
            print('Shot wasted, you already shot here!')
        elif (pos_x, pos_y) not in self. ships:
            print('You missed!')
            self. tiles_hit[pos_x][pos_y] = 'M'
        else:
            self. tiles_hit[pos_x][pos_y] = 'X'
            self. ships_sunk += 1
            print('It is a hit!')
            


