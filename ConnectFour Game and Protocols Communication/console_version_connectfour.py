#Qiao He: 16765414
#Aman Saini: 51853123


import connectfour
import game_board

def show_current_turn(game_state: connectfour.GameState):
    '''show the current turn of the player'''
    if game_state.turn==1:
        print('Now it is the RED turn!')
    else:
        print('Now it is the YELLOW turn!')
    
def prompt_and_execute_column_number_and_command(game_state: connectfour.GameState):
    '''after getting the command and column number, then start to execute the action and return a new game state'''
    while True:
        column_number = game_board.get_user_input_column_number()
        action = game_board.get_user_command_drop_or_pop()
        if action=='DROP':
            try:
                game_state=connectfour.drop(game_state, column_number-1)
                return game_state
            except connectfour.InvalidMoveError:
                print('Invalid move, cannot drop here, try again!')
        else:
            try:
                game_state=connectfour.pop(game_state, column_number-1)
                return game_state
            except connectfour.InvalidMoveError:
                print('Invalid move, cannot pop here, try again!')
    
    
def announce_winner(winner: int):
    '''when there is a winner, announce it according to the winner value'''
    if winner==1:
        print('The winner is RED')
    else:
        print('The winner is YELLOW')
    
    

if __name__ == '__main__':
    game_board.welcome_banner()

    #create a new game
    GameState=game_board.create_new_game()
    board=GameState.board
    
    #print the new board
    game_board.print_board_current_state(board)

    while connectfour.winner(GameState)==connectfour.NONE:
        #print who is the turn
        show_current_turn(GameState)           
        #prompt the user input and take acion
        GameState=prompt_and_execute_column_number_and_command(GameState)
        #show the current board status to the user
        game_board.print_board_current_state(GameState.board)

    the_winner=connectfour.winner(GameState)
    announce_winner(the_winner)
