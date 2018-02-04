class GameBoard (object):
# class for a battle ship game board for one player
# size and ships are variable

    def __init__(self, n_row, n_col, player_name = ''):
    # Creates a new, empty game board of size n_row * n_col for player, name optional
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
    # Output: Number of ships on the board
        if not type(pos_x) == int or not type(pos_y) == int:
            print('Positions are not valid integers!')
        elif 0 > pos_x or pos_x > self. n_row or 0 > pos_y or pos_y > self. n_col:
            print('Positions are not on the board! Use smaller positions!')
        elif (pos_x, pos_y) in self. ships:
            print('This ship already exists, not added!')
        else:
        # if positions are vald coordinates and ship does not exist yet, add ship
            self. ships. append( (pos_x, pos_y) )
            self. n_ships = len(self. ships)
        return self. n_ships

    def take_shot(self, pos_x, pos_y):
    # Shoots at position (pos_x, pos_y), check if valid or duplicated
    # Output: 0 invalid shot, 1 Hit, 2 Miss or Duplicate
        if not type(pos_x) == int or not type(pos_y) == int:
            print('Positions are not valid integers!')
            return 0
        elif 0 > pos_x or pos_x > self. n_row or 0 > pos_y or pos_y > self. n_col:
            print('Positions are not on the board! Use smaller positions!')
            return 0
        elif self. tiles_hit[pos_x][pos_y] != 'O':
            print('Shot wasted, you already shot here!')
            return 2
        elif (pos_x, pos_y) not in self. ships:
            print('You missed!')
            self. tiles_hit[pos_x][pos_y] = 'M'
            return 2
        else:
            self. tiles_hit[pos_x][pos_y] = 'X'
            self. ships_sunk += 1
            print('It is a hit!')
            return 1

    def clear_board(self, print_result = True):
    # Resets the board to no ships and no hits or misses, size stays the same
    # print_result is a boolean specifying if the result before the reset should be printed
        if print_result:
            print('You sank %s of %s ships this time!'%
                  (self. ships_sunk, self. n_ships))
        self. n_ships = 0
        self. ships_sunk = 0
        self. ships = []
        self. tiles_hit = []
        # all tiles start out not hit (status 'O')
        for i in range(self. n_row):
            self. tiles_hit. append( ['O'] * self. n_col)

    def all_ships_hit(self):
    # A function to check whether there are still ships hidden on the board
    # Output: a boolean that is true if all ships were sunk
        return self. ships_sunk == self. n_ships

test = GameBoard(4,4)
print(test)
test.add_ship(2,2)
test.take_shot(1,1)
test.take_shot(2,2)
print(test)
test. clear_board()
print(test)
