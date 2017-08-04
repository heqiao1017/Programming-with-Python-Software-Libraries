import Othello_Game_Logic

def print_rule():
    print('FULL')

def read_input()->str or int:
    user_input=input()
    return user_input

def print_discs_number(game_state: Othello_Game_Logic.GameState):
    game_state.counter_discs()
    black_dics=game_state.get_black_dics()
    white_dics=game_state.get_white_dics()

    print('B: '+str(black_dics)+' W: ' + str(white_dics))

def get_input_position(available_move:[])->[]:
    while True:
        position=read_input()
        move_postion=[int(position[0]), int(position[2])]
        if move_postion in available_move:
            print('VALID')
            break
        print('INVALID')
    return move_postion

def print_winner(win_rule:str, game_state:Othello_Game_Logic.GameState):
    black_dics=game_state.get_black_dics()
    white_dics=game_state.get_white_dics()
    if black_dics==white_dics:
        print('WINNER: NONE')
    elif black_dics>white_dics:
        if win_rule=='>':
            print('WINNER: B')
        else:
            print('WINNER: W')
    else:
        if win_rule=='>':
            print('WINNER: W')
        else:
            print('WINNER: B')
        

def _run_user_interface()->None:
    print_rule()
    #get user input
    row=read_input()
    column=read_input()
    first_player=read_input()
    arrangement=read_input()
    win_rule=read_input()

    game_state=Othello_Game_Logic.GameState(row, column, first_player,
                                            arrangement, win_rule)
    no_valid_move_counter=0
    while True:
        if no_valid_move_counter>1:
            #end the game
            break
        print_discs_number(game_state)
        game_state.print_game_board()
        game_state.print_turn()
        
        available_move=game_state.get_available_cell_to_move()
        
        if len(available_move)==0:
            print('NO VALID MOVES AVAILABLE')
            game_state.shift_turn()
            no_valid_move_counter+=1
            continue
        else:
            if no_valid_move_counter>0:
                no_valid_move_counter-=1
            move_postion=get_input_position(available_move)
            game_state.move(move_postion)
            game_state.shift_turn()

        if game_state.get_empty_cell_left()==0:
            #game over
            break
    print_winner(win_rule,game_state)
   

if __name__=='__main__':
    _run_user_interface()
