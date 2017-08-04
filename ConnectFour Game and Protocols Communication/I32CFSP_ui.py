#Qiao He: 16765414
#Aman Saini: 51853123
#This module allows users to interact with I32CFSP server to play connectfour game

import I32CFSP
import connectfour
import game_board

def _show_welcome_banner()->None:
    '''welcome the user to intearct with I32CFSP server'''
    print("Welcome to the I32CFSP client!")

def _get_column()->int:
    '''get the valid column number from the user'''
    return game_board.get_user_input_column_number()

def _get_command()->str:
    '''get the valid command from the user'''
    return game_board.get_user_command_drop_or_pop()

def _print_turn(game_state:connectfour.GameState)->None:
    '''Indicate who is the player each turn'''
    if game_state.turn==1:
        print('Now it is your turn!')
    else:
        print("Now it is server's turn")

def _print_game_board(board:[[int]])->None:
    '''print the game board state'''
    game_board.print_board_current_state(board)

def _get_game_state()->connectfour.GameState:
    '''return the namedtuple game state object'''
    return game_board.create_new_game()

def _read_host()->str:
    '''get the host IP addresss'''
    while True:
        host=input('Host: ').strip()

        if host=='':
            print('Please specify a host (either a name or an IP address)')
        else:
            return host


def _read_port()->int:
    '''get the port number to access the server'''
    while True:
        try:
            port=int(input('Port: ').strip())
            if port>=0 and port<=65535:
                return port
        except:
            pass
        print("Ports must be an integer between 0 and 65535")

        
def _say_hello(connection: I32CFSP.I32CFSP_connection, username:str)->bool:
    '''sying hello to the server and reveive the welcome from the server'''
    try:
        response=I32CFSP.hello(connection, username)
        if response==I32CFSP.WELCOME:
            print('WELCOME '+username)
        return True
    except:
        print('The conversation fails, might be the wrong connection!')
        print("Closing the connection.........")
        I32CFSP.close(connection)
        print('Connection Closed!')
        return False

        
def _start_game(connection:I32CFSP.I32CFSP_connection, connection_success: bool)->bool:
    '''starting the game by requesting game from the client side and show welcom banner'''
    if connection_success:
        try:
            response=I32CFSP.request_game(connection)
            if response==I32CFSP.READY:
                game_board.welcome_banner()
            return True
        except:
            print('The conversation fails, might be the wrong connection!')
            print("Closing the connection.........")
            I32CFSP.close(connection)
            print('Connection Closed!')
            return False
               

def _ask_username()->str:
    '''ask the user name which cannot be empty and space inside the name'''
    while True:
        username=input("Username: ").strip()
        if username=='':
            print("Username cannot be empty! Try again")
        elif ' ' in username:
            print("No space in the username! Try again")
        else:
            return username
        

def _connect_server()->I32CFSP.I32CFSP_connection:
    '''connect the server with the host address and port number'''
    while True:
        host=_read_host()
        port=_read_port()
        try:
            connection=I32CFSP.connect(host, port)
            return connection
        except:
            print("Connection failed, please try again!")    

def _receive_execute_server_move(connection:I32CFSP.I32CFSP_connection, game_state: connectfour.GameState)->connectfour.GameState:
    '''receive server's response and uadate the game board by executing the command from the server, then return the new game state'''
    server_move=I32CFSP.recieve_server_command_and_number(connection)
    command=server_move.command
    column=server_move.column
    GameState=_execute_command(game_state,command,column)
    return GameState       

def _execute_command(game_state: connectfour.GameState,command:str, column:int)->connectfour.GameState:
    '''execute the command either be drop or pop'''
    if command=='DROP':
        return connectfour.drop(game_state,column-1)
    else:
        return connectfour.pop(game_state,column-1)


def _send_command_column_to_server(connection:I32CFSP.I32CFSP_connection, game_state: connectfour.GameState,command:str,column:int)->None:
    '''sending command request to the server, waiting for the response from the server. If the server says OKAY: then the move is valid,
    then it becomes server's turn. After server finished its turn, it will say READY to shift to client's turn. If the server says INVALID,
    client needs to keep enter command and column until the move is valid. After each turn, the server will check if there is a winner, if
    response showing there is a winner, then announce the winner and end the game. '''
    while True:
        try:
            #Receiving response from the server when the user is sending something
            response=I32CFSP.send_command_and_column_number(connection,command,column)
            if response==I32CFSP.OKAY:
                #Update the board
                GameState=_execute_command(game_state,command,column)
                #Print the board
                print()
                _print_game_board(GameState.board)
                print()
                #Now is the server's turn
                _print_turn(GameState)
                print()
                #Recieve server's command and column number and update the board
                GameState=_receive_execute_server_move(connection,GameState)
                #Print board
                print()
                _print_game_board(GameState.board)
                print()
                
                #After computer's move, either READY, WINNER_RED, WINNER_YELLOW will be received from the server
                response=I32CFSP.check_server_last_response(connection)
                if response==I32CFSP.WINNER_RED:
                    print('You WIN, congratulations!')
                    print('GAME OVER, GOODBYE!')
                    I32CFSP.close(connection)
                    break
                elif response==I32CFSP.WINNER_YELLOW:
                    print('You LOST, sorry!')
                    print('GAME OVER, GOODBYE!')
                    I32CFSP.close(connection)
                    break
                elif response==I32CFSP.READY:
                    _print_turn(GameState)
                    print()
                    column=_get_column()
                    command=_get_command()
                    game_state=GameState#unpdate the game board state
                        
            elif response==I32CFSP.INVALID:
                print()
                print('Invalid move, try again!')
                print()
                #waiting for READY
                response=I32CFSP.check_server_last_response(connection)
                if response==I32CFSP.READY:
                    column=_get_column()
                    command=_get_command()
                    
            elif response==I32CFSP.WINNER_RED or response==I32CFSP.WINNER_YELLOW:
                #update the board
                GameState=_execute_command(game_state,command,column)
                #print the board
                print()
                _print_game_board(GameState.board)
                print()
                #announce the winner
                if response==I32CFSP.WINNER_RED:
                    print('You WIN, congratulations!')
                else:
                    print('You LOST, sorry!')
                print('GAME OVER, GOODBYE!')
                I32CFSP.close(connection)
                break
        except:
            print('The server is sending something invalid and unrecognized!')
            print("Closing the connection.........")
            I32CFSP.close(connection)
            print('Connection Closed!')
            break

def _run_user_interface()->None:
    '''process the game'''
    #show welcome to the server
    _show_welcome_banner()
    #connect to the server
    connection=_connect_server()
    #get username
    username=_ask_username()
    #flag that check if conneciton is success
    connection_success=True
    #saying hello to the server
    connection_success=_say_hello(connection,username)#checking if connection closed
    #request the human versus computer game
    connection_success=_start_game(connection,connection_success )#checking if connection closed
    #if the connection is still a success, then start the connectfour game
    if connection_success==True:
        Gamestate=_get_game_state()
        _print_game_board(Gamestate.board)
        _print_turn(Gamestate)
        column=_get_column()
        command=_get_command()
        _send_command_column_to_server(connection,Gamestate,command,column)


if __name__=='__main__':
    _run_user_interface()
