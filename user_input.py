#Yuxin Shen 17937926
import tkinter

DEFAULT_FONT = ('Helvetica', 14)


class InitialBoard:
    def __init__(self, row_number:int, column_number:int):
        
        self._initial_board_window = tkinter.Toplevel()

        self._rows = row_number
        self._columns = column_number

        '''Canvas: Displays the game board and take the inital board input'''
        self._board_canvas = tkinter.Canvas(
            master = self._initial_board_window, background = '#006000',
            height = row_number*50, width = column_number*50)

        self._board_canvas.grid(
            row = 0, column = 0, rowspan = 3, columnspan = 3,
            sticky = tkinter.W + tkinter.E + tkinter.N + tkinter.S)
        
        self._board_canvas.bind('<Configure>', self._on_canvas_resized)


        '''Instructions'''
        self._instruction_text = tkinter.StringVar()
        self._instruction_text.set('Set up the initial board:\n'+\
                                   'Click buttons to drop discs on board\n'+\
                                   'Click again to remove disc (same color only)')

        instruction_label = tkinter.Label(
            master = self._initial_board_window, textvariable = self._instruction_text,
            font = DEFAULT_FONT)
        
        instruction_label.grid(
            row = 0, column = 3, padx = 10, pady = 10,
            sticky = tkinter.W)


        '''Black Button and White Button'''
        disc_color_frame = tkinter.Frame(master = self._initial_board_window)

        disc_color_frame.grid(
            row = 1, column = 3, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E)

        black_button = tkinter.Button(
            master = disc_color_frame, text = 'Black', font = DEFAULT_FONT,
            command = self._black_disc_button)
        
        black_button.grid(row=0, column = 1, padx = 10, pady = 10)

        white_button = tkinter.Button(
            master = disc_color_frame, text = 'White', font = DEFAULT_FONT,
            command = self._white_disc_button)

        white_button.grid(row = 0, column = 2, padx = 10, pady = 10)
        
        
        '''Ok Button and Cancel Button'''
        button_frame = tkinter.Frame(master = self._initial_board_window)

        button_frame.grid(
            row = 2, column = 3, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.S + tkinter.E)

        ok_button = tkinter.Button(
            master = button_frame, text = 'Start', font = DEFAULT_FONT,
            command = self._click_ok_button)
        
        ok_button.grid(row=0, column = 1, padx = 10, pady = 10)

        cancel_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
            command = self._click_cancel_button)

        cancel_button.grid(row = 0, column = 2, padx = 10, pady = 10)


        self._initial_board_window.rowconfigure(0, weight = 1)
        self._initial_board_window.rowconfigure(1, weight = 1)
        self._initial_board_window.rowconfigure(2, weight = 1)        
        self._initial_board_window.columnconfigure(0, weight = 1)
        self._initial_board_window.columnconfigure(1, weight = 1)
        self._initial_board_window.columnconfigure(2, weight = 1)
        self._initial_board_window.columnconfigure(3, weight = 1)

        self._ok_clicked = False
        self._cancel_clicked  = False
        self._black_disc_selected = False
        self._white_disc_selected = False

        self._board_input = []
        self._disc_lists = []


    def show(self) -> None:
        '''Shows dialog box'''
        self._initial_board_window.grab_set()
        self._initial_board_window.wait_window()
            
    def was_finished(self) -> bool:
        '''Checks if input is finished'''
        return self._ok_clicked

    def was_quit (self) -> bool:
        '''Checks if input is canceled'''
        return self._cancel_clicked

    def get_initial_board(self) -> [[str]]:
        '''Returns the initial board in a 2D list'''
        return self._board_input

    def _draw_board(self) -> [[str]]:
        '''Displays board by drawing rectangles on the canvas'''
        board_width = self._board_canvas.winfo_width()
        board_height = self._board_canvas.winfo_height()
        
        for i in range(self._rows):
            self._board_input.append([])
            for j in range(self._columns):               
                self._board_canvas.create_rectangle \
                (j*(board_width/self._columns), i*(board_height/self._rows), \
                (j+1)*(board_width/self._columns), (i+1)*(board_height/self._rows), \
                 outline = 'black')
                self._board_input[i].append('.')
              
        return self._board_input

    def _draw_disc(self, event: tkinter.Event, color:str) -> [[str]]:
        '''
        Draws discs on the board and saves each disc in the disclists.
        Deletes disc if a same color disc has already existed.
        '''
        
        board_width = self._board_canvas.winfo_width()
        board_height = self._board_canvas.winfo_height()


        click_point= [event.x, event.y]
        i = int(click_point[1]//(board_height/self._rows))
        j = int(click_point[0]//(board_width/self._columns))
        
        top_left_x = j * (board_width/self._columns)
        top_left_y = i * (board_height/self._rows)
        bottom_right_x = (j + 1)*(board_width/self._columns)
        bottom_right_y = (i + 1)*(board_height/self._rows)

       
        if self._board_input[i][j] == '.':
            
            self._board_input[i][j] = color[0].upper()
            
            disc_id = self._board_canvas.create_oval(
            top_left_x, top_left_y,
            bottom_right_x, bottom_right_y,
            fill = color, outline = color)
            
            self._disc_lists.append(([i,j],disc_id))
            
            return self._board_input

       
        elif self._board_input[i][j] == color[0].upper():
            for existed_disc in self._disc_lists:
                if existed_disc[0] == [i,j]:
                    self._board_canvas.delete(existed_disc[1])
                    self._board_input[i][j] = '.'
                    return self._board_input                   


    def _black_disc_button(self) -> bool:
        '''Returns if black disc button is clicked'''
        self._black_disc_selected = True
        self._board_canvas.bind('<Button-1>', self._black_disc_clicked)
        return self._black_disc_selected

    def _white_disc_button(self) -> bool:
        '''Returns if white disc button is clicked'''
        self._white_disc_selected = True
        self._board_canvas.bind('<Button-1>', self._white_disc_clicked)
        return self._white_disc_selected

    def _black_disc_clicked (self, event:tkinter.Event) -> None:
        '''Draws black disc'''
        self._draw_disc(event, 'black')

    def _white_disc_clicked (self, event:tkinter.Event) -> None:
        '''Draws white disc'''
        self._draw_disc(event, 'white')

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''Deletes and redraws the board if canvas is resized'''
        self._board_canvas.delete(tkinter.ALL)
        self._draw_board()

        board_width = self._board_canvas.winfo_width()
        board_height = self._board_canvas.winfo_height()
        
        for i in range(self._rows):
            for j in range(self._columns):
                
                top_left_x = j * (board_width/self._columns)
                top_left_y = i * (board_height/self._rows)
                bottom_right_x = (j+1) *(board_width/self._columns)
                bottom_right_y = (i+1) *(board_height/self._rows)
                
                if self._board_input[i][j] == 'B':
                    self._board_canvas.create_oval(
                        top_left_x, top_left_y,
                        bottom_right_x, bottom_right_y,
                        fill = 'black')
                elif self._board_input[i][j] == 'W':
                    self._board_canvas.create_oval(
                        top_left_x, top_left_y,
                        bottom_right_x, bottom_right_y,
                        fill = 'white')
                    

    def _click_ok_button(self) -> None:
        '''
        If both disc colors are selected, returns TRUE on 'ok' button
        and closes dialog window
        '''
        if self._black_disc_selected == True and self._white_disc_selected == True:
            self._ok_clicked = True
            self._initial_board_window.destroy()
        else:
            self._ok_clicked = False
            self._disc_error_message()
            

    def _click_cancel_button(self) -> None:
        '''Returns True on 'Cancel' button and closes dialog window'''
        self._cancel_clicked = True
        self._initial_board_window.destroy()

    def _disc_error_message(self) -> None:
        '''Displays error message if only one disc color is clicked'''
        self._disc_error = tkinter.StringVar()
        self._disc_error.set('Please display both color discs on the board')

        invalid_input_label = tkinter.Label(
            master = self._initial_board_window, textvariable = self._disc_error,
            font = DEFAULT_FONT, fg='red')
        
        invalid_input_label.grid(
            row = 3, column = 3, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.S + tkinter.E)




class BasicSettings:
    def __init__(self):

        '''A home page that asks user to set up the game'''
        self._home_window = tkinter.Toplevel()

        '''First line: Settings'''
        settings_label = tkinter.Label(
            master = self._home_window, text = 'Settings:',
            font = DEFAULT_FONT)

        settings_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        '''Second line: Asks for number of rows ([4 16]) and returns self._rows_entry'''
        rows_label = tkinter.Label(
            master = self._home_window, text = 'Number of rows (Even integer between 4 and 16 inclusive): ',
            font = DEFAULT_FONT)
        
        rows_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._rows_entry = tkinter.Entry(
            master = self._home_window, width = 20, font = DEFAULT_FONT)

        self._rows_entry.grid(
            row = 1, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        '''Third line: Asks for number of columns ([4 16]) and retusn self._columns_entry'''
        columns_label = tkinter.Label(
            master = self._home_window, text = 'Number of columns (Even integer between 4 and 16 inclusive): ',
            font = DEFAULT_FONT)
        
        columns_label.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._columns_entry = tkinter.Entry(
            master = self._home_window, width = 20, font = DEFAULT_FONT)

        self._columns_entry.grid(
            row = 2, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        '''Fourth Line: Asks for which player moves first, returns self._first_player_entry'''
        first_player_label = tkinter.Label(
            master = self._home_window, text = 'Player who will move first (Black / White): ',
            font = DEFAULT_FONT)
        
        first_player_label.grid(
            row = 3, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._first_player_entry = tkinter.Entry(
            master = self._home_window, width = 20, font = DEFAULT_FONT)

        self._first_player_entry.grid(
            row = 3, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        '''Fifth line: Asks for winning mode, returns self._winning_mode_entry'''
        winning_mode_label = tkinter.Label(
            master = self._home_window, text = 'Game won by the player with more discs or fewer discs (More / Fewer): ',
            font = DEFAULT_FONT)
        
        winning_mode_label.grid(
            row = 4, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._winning_mode_entry = tkinter.Entry(
            master = self._home_window, width = 20, font = DEFAULT_FONT)

        self._winning_mode_entry.grid(
            row = 4, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        '''Ok Button and Cancel Button'''
        button_frame = tkinter.Frame(master = self._home_window)

        button_frame.grid(
            row = 6, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.S + tkinter.E)

        ok_button = tkinter.Button(
            master = button_frame, text = 'Ok', font = DEFAULT_FONT,
            command = self._click_ok_button)
        
        ok_button.grid(row=0, column = 0, padx = 10, pady = 10)

        cancel_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
            command = self._click_cancel_button)

        cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)


        '''Label: Error Message'''
        self._error_message = tkinter.StringVar()
        self._error_message.set('')

        invalid_input_label = tkinter.Label(
            master = self._home_window, textvariable = self._error_message,
            font = DEFAULT_FONT, fg='red')
        
        invalid_input_label.grid(
            row = 5, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.S + tkinter.E)

        self._home_window.rowconfigure(6, weight = 1)
        self._home_window.columnconfigure(1, weight = 1)

        self._ok_clicked = False
        self._cancel_clicked = False
        self._rows = ''
        self._columns = ''
        self._first_player = ''
        self._winning_mode = ''

    def show(self) -> None:
        self._home_window.grab_set()
        self._home_window.wait_window()

    def was_ok_clicked(self) -> bool:
        return self._ok_clicked
    
    def was_cancel_clicked (self) -> bool:
        return self._cancel_clicked

    def get_rows(self) -> int:
        return self._rows

    def get_columns(self) -> int:
        return self._columns

    def get_first_player(self) -> str:
        return self._first_player[0]

    def get_winning_mode(self) -> str:
        return self._winning_mode

    def _click_ok_button(self) -> None:
        '''
        Returns True on 'ok' button if entries are valid,
        and closes dialog window
        '''
        if self._valid_entry():           
            self._ok_clicked = True
            self._home_window.destroy()               
        else:
            self._ok_clicked = False
    
    def _click_cancel_button(self) -> None:
        '''
        Returns True on 'cancel' button and closes dialog window
        '''
        self._cancel_clicked = True
        self._home_window.destroy()

    def _valid_entry(self) -> bool:
        '''Returns True if all entries are valid'''
        if self._valid_rows() and self._valid_columns() and self._valid_first_player() and self._valid_winning_mode():
            return True

    def _valid_rows (self) -> bool:
        '''Checks if rows entry is valid'''
        try:
            self._rows = int(self._rows_entry.get())
            if 2 <= self._rows <= 16 and self._rows %2 == 0:
                return True
            else:
                self._error_message.set('Number of rows must be an even number between 4 and 16')
        except:
            self._error_message.set('Invalid number of rows input, must be a number')

    def _valid_columns (self) -> bool:
        '''Checks if columns entry is valid'''
        try:
            self._columns = int(self._columns_entry.get())
            if 2 <= self._columns <= 16 and self._columns %2 == 0:
                return True
            else:
                self._error_message.set('Number of columns must be an even number between 4 and 16')
        except:
            self._error_message.set('Invalid number of columns input, must be a number')


    def _valid_first_player (self) -> bool:
        '''Checks if first player entry is valid'''
        self._first_player = self._first_player_entry.get()
        if self._first_player == 'Black' or self._first_player == 'White':
            return True
        else:
            self._error_message.set('Invalid first player input, must be \'Black\' or \'White\'')             
        
    def _valid_winning_mode (self) -> bool:
        '''Checks if winning mode entry is valid'''
        self._winning_mode = self._winning_mode_entry.get()
        
        if self._winning_mode == 'More':
            self._winning_mode = '>'
            return True
        elif self._winning_mode == 'Fewer':
            self._winning_mode = '<'
            return True
        else:
            self._error_message.set('Invalid winning mode input, must be \'More\' or \'Fewer\'')                                      
