#Yuxin Shen 17937926

import tkinter
import othello
import user_input

DEFAULT_FONT = ('Helvetica', 14)


class OthelloApplication:
    def __init__(self):

        self._root_window = tkinter.Tk()       
        self._display_start_page()

    def run(self):
        self._root_window.mainloop()
        
    def _display_start_page(self):

        '''Button: Game Start'''
        greet_button = tkinter.Button(
            master = self._root_window, text = 'Start Game', font = DEFAULT_FONT,
            command = self._game_start)

        greet_button.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.S)
        
        '''Label: Welcome Label'''
        greeting_label = tkinter.Label(
            master = self._root_window, text = 'Welcome to othello!\nFULL Version',
            font = DEFAULT_FONT)
        
        greeting_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)


    def _game_start(self):
        '''Checks if the input is entered, and displays the canvas to play'''
        self._Game = self._get_input()

        if self._input_entered == True:
            self._display_canvas()


    def _get_input(self) -> 'GameState':
        '''
        Asks users to enter input and returns a GameState
        '''
        self._input_entered = False
        
        settings = user_input.BasicSettings()
        settings.show()
        
        if settings.was_ok_clicked():
            '''If basic settings are entered, displays an empty board'''
            self._rows = settings.get_rows()
            self._columns = settings.get_columns()
            self._turn = settings.get_first_player()
            self._winning_mode = settings.get_winning_mode()

            set_board = user_input.InitialBoard(self._rows, self._columns)
            set_board.show()

            if set_board.was_finished():
                '''If initial board is set, returns a GameState'''
                self._board = set_board.get_initial_board()
                self._input_entered = True
                return othello.GameState(self._rows, self._columns, self._board, self._turn, self._winning_mode)

            elif set_board.was_quit():
                '''If initial board is dismissed, asks for input again'''
                return self._get_input()

        elif settings.was_cancel_clicked():
            '''If basic settings are canceled, starts game again'''
            self._display_start_page()


    def _display_canvas(self):
        '''Canvas: Displays the game board and plays the game'''
        self._board_canvas = tkinter.Canvas(
            master = self._root_window, background = '#006000',
            height = self._rows*50, width = self._columns*50)

        self._board_canvas.grid(
            row = 0, column = 0, rowspan = 3, columnspan = 3,
            sticky = tkinter.W + tkinter.E + tkinter.N + tkinter.S)
       
        self._board_canvas.bind('<Configure>', self._on_canvas_resized)
        self._board_canvas.bind('<Button-1>', self._drop_disc)       


        '''StringVar: Label for Current Score'''
        self._current_score = tkinter.StringVar()
        self._current_score.set('Current Score\nBlack: {}  White: {}'.format(
                            self._Game.count_disc('B'),
                            self._Game.count_disc('W')
                              ))

        current_score_label = tkinter.Label(
            master =self._root_window, textvariable = self._current_score,
            font = DEFAULT_FONT)

        current_score_label.grid(
            row = 0, column = 3, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E + tkinter.S + tkinter.N)

        '''StringVar: Label for Current Turn'''
        self._current_turn = tkinter.StringVar()
        self._current_turn.set('Current Turn\n{}'.format(_full_name(self._Game.current_turn())))

        current_turn_label = tkinter.Label(
            master =self._root_window, textvariable = self._current_turn,
            font = DEFAULT_FONT)

        current_turn_label.grid(
            row = 0, column = 5, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E + tkinter.S + tkinter.N)   

        '''Label: Shows the version of the game and author's name'''
        self._copyright_label = tkinter.Label(
            master = self._root_window,
            text = 'ICS32 Othello\n'+
                    'FULL Version\n'+
                    'Code by: Yuxin Shen\n'+
                    '2017/12/05')

        self._copyright_label.grid(
            row = 2, column = 6,
            sticky = tkinter.E + tkinter.S)

        self._root_window.rowconfigure(0, weight = 2) 
        self._root_window.rowconfigure(1, weight = 2) 
        self._root_window.rowconfigure(2, weight = 2)               
        self._root_window.columnconfigure(0, weight = 2)
        self._root_window.columnconfigure(1, weight = 2)
        self._root_window.columnconfigure(2, weight = 2)
        self._root_window.columnconfigure(3, weight = 1)
        self._root_window.columnconfigure(4, weight = 1)
        self._root_window.columnconfigure(5, weight = 1)
        self._root_window.columnconfigure(6, weight = 1)

             
    def _drop_disc(self, event:tkinter.Event):
        '''
        Drops a disc with current player's color on the click point
        and updates the canvas with player's move
        '''
        click_point= [event.x, event.y]

        rows = self._Game.rows()
        columns = self._Game.columns()
        color = _full_name(self._Game.current_turn())
        
        board_width = self._board_canvas.winfo_width()
        board_height = self._board_canvas.winfo_height()
 
        i = int(click_point[1]//(board_height/rows))
        j = int(click_point[0]//(board_width/columns))

        if self._Game.check_valid(i,j) and self._Game.current_board()[i][j] == '.':       
            top_left_x = j * (board_width/columns)
            top_left_y = i * (board_height/rows)
            bottom_right_x = (j + 1)*(board_width/columns)
            bottom_right_y = (i + 1)*(board_height/rows)
            
            self._board_canvas.create_oval(
                top_left_x, top_left_y,
                bottom_right_x, bottom_right_y,
                fill = color, outline = color)

            location = [i,j]
            try:
                self._Game = self._Game.make_move(location[0],location[1])
                self._update_canvas()
            except:
                pass

    def _update_canvas(self):

        '''
        Updates game info: Current Score, Current Turn, Winner (if exists),
        and Game End Buttons (if winner exists)
        '''
        self._display_game_board()
        self._current_score.set('Current Score\nBlack: {}\nWhite: {}'.format(
                self._Game.count_disc('B'),
                self._Game.count_disc('W')
                  ))
        self._current_turn.set('Current Turn:\n{}'.format(_full_name(self._Game.current_turn())))
    
        if self._Game.winner() != 'Game is not over':
            self._current_turn.set('Game Over!')
            self._display_winner()
            self._display_end_button()


    def _display_winner(self) -> None:
        '''StringVar: Winner'''
        self._winner = tkinter.StringVar()
        self._winner.set('Winner: {}'.format(_full_name(self._Game.winner())))

        winner_label = tkinter.Label(
            master =self._root_window, textvariable = self._winner,
            font = DEFAULT_FONT)

        winner_label.grid(
            row = 1, column = 3, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E + tkinter.S + tkinter.N)   


    def _display_end_button(self) -> None:
        '''Frame: Replay Button and Exit Button'''
        end_frame = tkinter.Frame(master = self._root_window)

        end_frame.grid(
            row = 1, column = 5, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.S + tkinter.E)

        replay_button = tkinter.Button(
            master = end_frame, text = 'Replay', font = DEFAULT_FONT,
            command = self._click_replay_button)
        
        replay_button.grid(row=0, column = 1, padx = 10, pady = 10)

        exit_button = tkinter.Button(
            master = end_frame, text = 'Exit', font = DEFAULT_FONT,
            command = self._click_exit_button)

        exit_button.grid(row = 0, column = 2, padx = 10, pady = 10)

        
    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''
        Redraw the canvas when window is resized
        '''
        self._board_canvas.delete(tkinter.ALL)
        self._display_game_board()


    def _display_game_board(self) -> None:
        '''
        Draw rectangles and ovals to present current gameboard.
        '''
        board = self._Game.current_board()
        rows = self._Game.rows()
        columns = self._Game.columns()
        
        board_width = self._board_canvas.winfo_width()
        board_height = self._board_canvas.winfo_height()
        
        for i in range(rows):
            for j in range(columns):

                self._board_canvas.create_rectangle \
                (j*(board_width/columns), i*(board_height/rows), \
                (j+1)*(board_width/columns), (i+1)*(board_height/rows), \
                 outline = 'black')
                
                top_left_x = j * (board_width/columns)
                top_left_y = i * (board_height/rows)
                bottom_right_x = (j+1) *(board_width/columns)
                bottom_right_y = (i+1) *(board_height/rows)
                
                if board[i][j] == 'B':
                    self._board_canvas.create_oval(
                        top_left_x, top_left_y,
                        bottom_right_x, bottom_right_y,
                        fill = 'black')
                elif board[i][j] == 'W':
                    self._board_canvas.create_oval(
                        top_left_x, top_left_y,
                        bottom_right_x, bottom_right_y,
                        fill = 'white')


    def _click_replay_button(self) -> None:
        '''If replay button clicked, closes current window and
        starts the application again'''
        self._root_window.destroy()
        OthelloApplication().run()

    def _click_exit_button(self) -> None:
        '''If exit button clicked, closes the root window'''
        self._root_window.destroy()



def _full_name (player:str) -> str:
    '''Returns the full name of player'''
    if player == 'B':
        return 'Black'
    elif player == 'W':
        return 'White'
    elif player == 'NONE':
        return 'None'
    else:
        return 'Game is not over'



if __name__ == '__main__':
    OthelloApplication().run()
