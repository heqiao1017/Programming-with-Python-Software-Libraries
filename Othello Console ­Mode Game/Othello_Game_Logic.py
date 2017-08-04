class GameState:
    '''represents the current game state of the game'''
    
    def __init__(self, row, column, first_player, four_center_cell_arrangment, game_win_rule):
        '''initialize the attributes in the game class including: row, column, first player,
           four center cell arrangement and game win rule........'''
        self.__row=int(row)
        self.__column=int(column)
        self.__turn=first_player
        self.__four_center_cell_arrangment=four_center_cell_arrangment
        self.__win_rule=game_win_rule
        self.__empty_cell_left=int(column)*int(row)-4
        self.__black_dics=0
        self.__white_discs=0

        #constant variables stand for different players
        self.__NONE=0
        self.__BLACK=1 #black disc
        self.__WHITE=2 #white disc
        

        self.__board=self.__new_game_board() #construct a new game board and initializ the board with the four center cells arrangement   
    def get_row(self)->int:
        '''returns the row number of the game board'''
        return self.__row

    def get_column(self)->int:
        '''returns the column number of the game board'''
        return self.__column
    def print_game_board(self):
        for row in range(self.__row):
            for col in range(self.__column):
                cell=self.__board[row][col]
                if cell==self.__NONE:
                    print('.', end=' ')
                elif cell==self.__BLACK:
                    print('B', end=' ')
                else:
                    print('W', end=' ')
            print()

    def print_turn(self):
        print('TURN: '+ self.__turn)


    def shift_turn(self):
        if self.__turn=='B':
            self.__turn='W'
        else:
            self.__turn='B'

    def move(self, input_cell:[]):
        if self.__turn=='B':
            self.__board[input_cell[0]][input_cell[1]]=self.__BLACK
            self.__black_dics+=1
        else:
            self.__board[input_cell[0]][input_cell[1]]=self.__WHITE
            self.__white_discs+=1
        self._shift_cell(input_cell,0,1)
        self._shift_cell(input_cell,1,1)
        self._shift_cell(input_cell,1,0)
        self._shift_cell(input_cell,0,-1)
        self._shift_cell(input_cell,1,-1)
        self._shift_cell(input_cell,-1,0)
        self._shift_cell(input_cell,-1,1)
        self._shift_cell(input_cell,-1,-1)
        self.__empty_cell_left-=1
        
    def get_empty_cell_left(self)->int:
        return self.__empty_cell_left

    def get_available_cell_to_move(self)->[]:
        return self._find_available_cell_to_move()

    
    def counter_discs(self):
        self.__black_dics=0
        self.__white_discs=0
        for row in range(self.__row):
            for col in range(self.__column):
                if self.__board[row][col]==self.__BLACK:
                    self.__black_dics+=1
                elif self.__board[row][col]==self.__WHITE:
                    self.__white_discs+=1


    def get_black_dics(self)->int:
 #       self.__black_dics=0
#        self._counter_discs()
        return self.__black_dics

    def get_white_dics(self)->int:
 #       self.__white_discs=0
#        self._counter_discs()
        return self.__white_discs

    def __new_game_board(self)->[[int]]:
        '''return s a new game board'''
        board=[]
        for row in range(self.__row):
            board.append([])
            for column in range(self.__column):
                board[-1].append(self.__NONE)

        top_left_row=int(self.__row/2)-1
        top_left_col=int(self.__column/2)-1

        if self.__four_center_cell_arrangment=='B':
            board[top_left_row][top_left_col]=self.__BLACK
            board[top_left_row+1][top_left_col+1]=self.__BLACK
            board[top_left_row][top_left_col+1]=self.__WHITE
            board[top_left_row+1][top_left_col]=self.__WHITE
        else:
            board[top_left_row][top_left_col]=self.__WHITE
            board[top_left_row+1][top_left_col+1]=self.__WHITE
            board[top_left_row][top_left_col+1]=self.__BLACK
            board[top_left_row+1][top_left_col]=self.__BLACK
        return board
    
    def _find_available_cell_to_move(self)->[]:
        available_cell_to_move=[]
        for row in range(self.__row):
            for col in range(self.__column):
                #when the turn is black, find the white discs
                if self.__turn=='B':
                    if self.__board[row][col]==self.__WHITE:
                        valid_empty_cells=self._find_surrounding_empty_cell([row, col])
                        valid_cell_to_move=self._find_valid_cell_to_move([row,col],valid_empty_cells)
                        #print(valid_cell_to_move)
                        available_cell_to_move+=valid_cell_to_move
                else:
                    if self.__board[row][col]==self.__BLACK:
                        valid_empty_cells=self._find_surrounding_empty_cell([row, col])
                        valid_cell_to_move=self._find_valid_cell_to_move([row,col],valid_empty_cells)
                        #print(valid_cell_to_move)
                        available_cell_to_move+=valid_cell_to_move
        return available_cell_to_move
                    
    def _find_surrounding_empty_cell(self,cell_to_search:[])->[]:
        row=cell_to_search[0]
        col=cell_to_search[1]

        valid_empty_cells=[]

        if self._is_valid_surrounding_cell(row, col, 0,1) and self.__board[row][col+1]==self.__NONE:
            valid_empty_cells.append([row, col+1])
        if self._is_valid_surrounding_cell(row, col, 1,1) and self.__board[row+1][col+1]==self.__NONE:
            valid_empty_cells.append([row+1, col+1])
        if self._is_valid_surrounding_cell(row, col, 1,0) and self.__board[row+1][col]==self.__NONE:
            valid_empty_cells.append([row+1, col])
        if self._is_valid_surrounding_cell(row, col, 1,-1) and self.__board[row+1][col-1]==self.__NONE:
            valid_empty_cells.append([row+1, col-1])
        if self._is_valid_surrounding_cell(row, col, 0,-1) and self.__board[row][col-1]==self.__NONE:
            valid_empty_cells.append([row, col-1])
        if self._is_valid_surrounding_cell(row, col, -1,-1) and self.__board[row-1][col-1]==self.__NONE:
            valid_empty_cells.append([row-1, col-1])
        if self._is_valid_surrounding_cell(row, col, -1,0) and self.__board[row-1][col]==self.__NONE:
            valid_empty_cells.append([row-1, col])
        if self._is_valid_surrounding_cell(row, col, -1,1) and self.__board[row-1][col+1]==self.__NONE:
            valid_empty_cells.append([row-1, col+1])

        return valid_empty_cells
        
    def _is_valid_surrounding_cell(self, row:int , col:int, row_delta:int, col_delta: int)->[]:
        row=row+row_delta
        col=col+col_delta
        if not self._is_valid_row_number(row) or not self._is_valid_column_number(col):
            return False
        return True

    def _is_valid_column_number(self, column_number:int)->bool:
        return 0<=column_number<self.__column

    def _is_valid_row_number(self, row_number:int)->bool:
        return 0<=row_number<self.__row
    
    def _find_valid_cell_to_move(self, center_cell:[], valid_empty_cells:[[]])->[]:
        center_cell_row=center_cell[0]
        center_cell_col=center_cell[1]
        center_cell_row_hold=center_cell_row
        center_cell_col_hold=center_cell_col

        valid_cell_to_move=[]

        for cell in valid_empty_cells:
            row_delta=center_cell_row_hold-cell[0]
            #print("row delta: " +str(row_delta))
            col_delta=center_cell_col_hold-cell[1]
            #print("col delta: " +str(col_delta))
            if self.__turn=='B':              
                while self._is_valid_row_number(center_cell_row+row_delta) and\
                      self._is_valid_column_number(center_cell_col+col_delta):
                    center_cell_row+=row_delta
                    center_cell_col+=col_delta
                    if self.__board[center_cell_row][center_cell_col]==self.__BLACK:
                        valid_cell_to_move.append(cell)
                        break
                    elif self.__board[center_cell_row][center_cell_col]==self.__NONE:
                        break
            else:
                while self._is_valid_row_number(center_cell_row+row_delta) and\
                      self._is_valid_column_number(center_cell_col+col_delta):
                    center_cell_row+=row_delta
                    center_cell_col+=col_delta
                    if self.__board[center_cell_row][center_cell_col]==self.__WHITE:
                        valid_cell_to_move.append(cell)
                        break
                    elif self.__board[center_cell_row][center_cell_col]==self.__NONE:
                        break
            center_cell_row=center_cell_row_hold
            center_cell_col=center_cell_col_hold

        return valid_cell_to_move


    def _shift_cell(self, start_cell:[], row_delta:int, col_delta:int):
        start_cell_row=start_cell[0]
        start_cell_col=start_cell[1]

        temp_list=[]
        
        if self.__turn=='B':
            while self._is_valid_row_number(start_cell_row+row_delta) and\
                  self._is_valid_column_number(start_cell_col+col_delta):
                start_cell_row+=row_delta
                start_cell_col+=col_delta
                if self.__board[start_cell_row][start_cell_col]==self.__WHITE:
                    temp_list.append([start_cell_row,start_cell_col])
                elif self.__board[start_cell_row][start_cell_col]==self.__BLACK:
                    for temp in temp_list:
                        self.__board[temp[0]][temp[1]]=self.__BLACK
                    break
                else:
                    break
        else:
            while self._is_valid_row_number(start_cell_row+row_delta) and\
                  self._is_valid_column_number(start_cell_col+col_delta):
                start_cell_row+=row_delta
                start_cell_col+=col_delta
                if self.__board[start_cell_row][start_cell_col]==self.__BLACK:
                    temp_list.append([start_cell_row,start_cell_col])
                elif self.__board[start_cell_row][start_cell_col]==self.__WHITE:
                    for temp in temp_list:
                        self.__board[temp[0]][temp[1]]=self.__WHITE
                    break
                else:
                    break

    
                
