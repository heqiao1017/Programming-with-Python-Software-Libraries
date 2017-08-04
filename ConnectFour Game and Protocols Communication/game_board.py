#Qiao He: 16765414
#Aman Saini: 51853123


import connectfour

def welcome_banner()->None:
    ''''show welcome banner when the connectfour game start'''
    print('Welcome to the ConnectFour Game!')

def create_new_game()->connectfour.GameState:
    '''create a new game with board and turn'''
    return connectfour.new_game()

def print_board_current_state(board:[[int]]):
    '''print the first line and the grid to show the actual game board'''
    #print the first line which indicates the column number
    _print_column_number(connectfour.BOARD_COLUMNS)    
    #print the game board
    _print_game_board(board)
    
def get_user_input_column_number()->int:
    '''get user column number'''
    while True:
        column_input=input('Please enter column number: ')
        if _check_column_input_validity(column_input):
            column_number=int(column_input)
            return column_number
        else:
            print('Valid number must be an int and in the range of 1 to {}'.format(connectfour.BOARD_COLUMNS))

def get_user_command_drop_or_pop()->str:
    '''get user command: drop or pop'''
    while True:
        action=input('Please choose an action: drop (DROP) or Pop (POP): ')
        if action=='DROP' or action =='POP':
            return action
        else:
            print('Valid input must be "DROP" or "POP"')

#########################################################################################    
def _print_column_number(column_number: int):
    '''print the first line of column number indicate the columns'''
    for number in range(column_number):
        print(number+1, end=' ')
    print()


def _print_game_board(board: [[int]]):
    '''print the game board as the grid'''
    for row in range(connectfour.BOARD_ROWS):
        for col in range(connectfour.BOARD_COLUMNS):
            cell=board[col][row]
            if cell==0:
                print(".",end=' ')
            elif cell==1:
                print("R",end=' ')
            else:
                print("Y",end=' ')
        print()

def _check_column_input_validity(column_input: str)->bool:
    '''check if input column number is an integer in the range of 1 to BOARD_COLUMNS'''
    try:
        column_number=int(column_input)
        if 0<column_number<=connectfour.BOARD_COLUMNS:           
            return True
    except:
        return False
