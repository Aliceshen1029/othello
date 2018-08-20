#Yuxin Shen 17937926

class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass


class GameOverError(Exception):
    '''
    Raised whenever an attempt is made to make a move after the game is
    already over
    '''
    pass


class GameState:
    def __init__(self, row_numbers: int, column_numbers: int, board:[[str]], turn:str, winning_mode: str):
        self._rows = row_numbers
        self._columns = column_numbers
        self._board = board
        self._turn = turn
        self._winning_mode = winning_mode

    def current_turn(self) -> str:
        'Returns current player'
        return self._turn

    def current_board(self) -> [[str]]:
        'Returns current board'
        return self._board
    
    def rows(self) -> int:
        'Returns number of rows on board'
        return self._rows

    def columns(self) -> int:
        'Returns number of columns on board'
        return self._columns

    def count_disc(self,color:str) -> int:
        'Takes a color and returns the number of disc with that color on the board'
        count = 0
        for col in range(self._rows):
            for disc_color in self._board[col]:
                if disc_color == color:
                    count += 1
        return count

    def check_valid (self, row:int, col:int) -> bool:
        '''
        Takes a row and column number that represents a cell location.
        Returns True if a direction could make move valid in any of the eight possible directions;
        Returns False otherwise.
        '''
        return self._valid_direction(row, col, 0, 1) \
            or self._valid_direction(row, col,  1, 1) \
            or self._valid_direction(row, col, 1, 0) \
            or self._valid_direction(row, col,  1, -1) \
            or self._valid_direction(row, col,  0, -1) \
            or self._valid_direction(row, col,  -1, -1) \
            or self._valid_direction(row, col,  -1, 0) \
            or self._valid_direction(row, col,  -1, 1)


    def make_move(self,row:int, col:int) -> 'GameState':
        '''
        Given a row and a column number to represent a cell location, returns
        the game state that results when the current player (whose turn it is) makes
        a move on the board. If the cell location is valid, a ValueError is raised.
        If the game is over, a GameOverError is raised. If a move cannot be made in the
        given cell location because it is not valid to the current player,
        and InvalidMoveError is raised.
        '''
        self._require_valid_cell_location(row, col)
        self._require_game_is_not_over()

        if self.check_valid(row, col):
            for rowdelta in range(-1,2):
                for coldelta in range(-1,2):
                    if self._valid_direction(row, col, rowdelta, coldelta):
                       self._update_direction(row, col, rowdelta, coldelta)
            self._opposite_turn()
            return self
            
        else:
            raise InvalidMoveError()
        
        
    def winner(self) -> str:
        '''
        Determines if the game is over in the current game state.
        If either player has a move available on the board,
        a string that indicates the game is not over is returned.
        If no player has a move available, winner is returned.
        '''
        if self._move_available() == True:
            return 'Game is not over'
        else:
            self._opposite_turn()
            if self._move_available() == True:
                return 'Game is not over'
            else:
                return self._result()


    def _opposite_turn(self) -> str:
        '''Returns the opposite player in the current game state'''
        if self._turn == 'B':
            self._turn = 'W'
            return self._turn
        else:
            self._turn = 'B'
            return self._turn


    def _result(self) -> str:
        '''
        Checks the winning mode that is pre-defined for this game state,
        returns the winner by comparing the number of disc on the board.
        '''
        if self._winning_mode == '>':
            if self.count_disc('B') > self.count_disc('W'):
                return 'B'
            elif self.count_disc('W') > self.count_disc('B'):
                return 'W'
            elif self.count_disc('B') == self.count_disc('W'):
                return 'NONE'
        else:
            if self.count_disc('B') < self.count_disc('W'):
                return 'B'
            elif self.count_disc('W') < self.count_disc('B'):
                return 'W'
            elif self.count_disc('B') == self.count_disc('W'):
                return 'NONE'


    def _move_available (self) -> bool:
        '''
        Checks all of the empty cells on the board.
        Returns True if there is a valid cell for the current player;
        Returns False otherwise
        '''
        available_move = 0
        for i in range(self._rows):
            for j in range(self._columns):
                if self._board[i][j] == '.' and self.check_valid(i,j) == True:
                    available_move += 1
        return available_move != 0


    def _valid_direction (self, row: int, col: int, rowdelta: int, coldelta: int) -> bool:
        '''
        Returns True if the next cell of the given cell (represented by given row and column number)
        in the direction specified by the coldelta and rowdelta is not empty, doesn't have the same color,
        and there is cell with the same color exists somewhere in this direction on the board;
        Returns False otherwise.
        '''
        if self._check_disc(row+rowdelta,col+coldelta) != self._turn \
            and self._check_disc(row+rowdelta,col+coldelta) != '.' \
                and self._same_disc_location (row, col, rowdelta, coldelta) != 'NONE':
            return True
 
        else:
            return False

       
    def _update_direction(self, row: int, col: int, rowdelta: int, coldelta: int) -> [[str]]:
        '''
        Finds the cell location in the direction specified by the coldelta and rowdelta
        that has the same color with the current player on the board.
        Turns all disc between the found cell location and the current cell location
        (specified by given row and column number) into the same color.
        '''
        end_location = self._same_disc_location(row,col,rowdelta,coldelta)
        for i in range(0,max(abs(end_location[0]-row)+1,abs(end_location[1]-col)+1)):
            self._board[row+rowdelta*i][col+coldelta*i] = self._turn

        
    def _same_disc_location(self, row: int, col: int, rowdelta: int, coldelta: int) -> [] or 'NONE':
        '''
        Returns the cell location in the direction specified by the coldelta and rowdelta that
        has the same color with the current player with contagious pieces between the current cell location
        (specified by given row and column number) and the first empty cell/the edge of the board.
        Returns NONE if no same color disc is found.
        '''
        for i in range(1, max(self._rows,self._columns)):
            if self._check_disc(row+rowdelta*i,col+coldelta*i)=='.':
                empty_cell=[row+rowdelta*i,col+coldelta*i]
                for j in range(1, max(abs(empty_cell[0]-row),abs(empty_cell[1]-col))):
                    if self._check_disc(row+rowdelta*j, col+coldelta*j) == self._turn:
                        return [row+rowdelta*j,col+coldelta*j]
                return 'NONE'
                        
            else:
                if self._check_disc(row+rowdelta*i, col+coldelta*i) == self._turn:
                    return [row+rowdelta*i,col+coldelta*i]
                
        return 'NONE'

    def _check_disc(self,row:int,col:int) -> str:
        '''
        Takes a row number and a column number that represetns a cell location.
        Returns the color if the cell location is valid (within the board).
        '''
        if self._is_valid_column_number (col)\
           and self._is_valid_row_number (row):
            return self._board[row][col]


    def _require_game_is_not_over (self) -> None:
        '''
        Raises a GameOverError if the current game state represents a situation
        where the game is over (i.e., there is a winning player)
        '''
        if self.winner() != 'Game is not over':
            raise GameOverError()

    def _require_valid_cell_location (self, row_number: int, column_number: int) -> bool:
        '''Raises a ValueError if its parameter is not a valid cell location'''
        if type(row_number) != int\
            or type(column_number) != int \
                or not self._is_valid_row_number(row_number) \
                    or not self._is_valid_column_number(column_number) \
                        or self._check_disc(row_number, column_number) != '.':
            raise ValueError('Invalid Cell Location')

    def _is_valid_column_number (self, column_number: int) -> bool:
        '''Returns True if the given column number is valid; Returns False otherwise'''
        return 0 <= column_number < self._columns

    def _is_valid_row_number (self, row_number: int) -> bool:
        '''Returns True if the given row number is valid; Returns False otherwise'''
        return 0 <= row_number < self._rows


