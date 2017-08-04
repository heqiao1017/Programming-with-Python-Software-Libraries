#communicate with the I32CFSP server

#Qiao He: 16765414
#Aman Saini: 51853123

import socket
from collections import namedtuple

I32CFSP_connection=namedtuple('I32CFSP_connection', ['socket', 'input', 'output'])
I32CFSP_move=namedtuple('I32CFSP_move', ['command','column'])

WELCOME=0
NO_USER=1
AI_GAME=2
READY=3
DROP=4
POP=5
OKAY=6
INVALID=7
WINNER_RED=8
WINNER_YELLOW=9

class I32CFSPProtocolError(Exception):
    '''when server sending something invalid or bad things happen, throw this error'''
    pass 

def connect(host: str, port: int)->I32CFSP_connection:
    '''
    Connects to the I32CFSP server running on the given host and listening on the given port,
    returning a I32CFSP_connection object describing that connection if successful, or raisin
    an exception if the attempt to connect fails
    '''
    
    I32CFSP_socket=socket.socket()
    I32CFSP_socket.connect((host, port))
    I32CFSP_input=I32CFSP_socket.makefile('r')
    I32CFSP_output=I32CFSP_socket.makefile('w')

    return I32CFSP_connection(
        socket=I32CFSP_socket,
        input=I32CFSP_input,
        output=I32CFSP_output)

def hello(connection: I32CFSP_connection, username: str)->WELCOME:
    '''sending message HELLO to the server with the username and receiving WELCOME from the server'''
    _write_line(connection, 'I32CFSP_HELLO ' + username)

    response = _read_line(connection)

    if response == 'WELCOME ' + username:
        return WELCOME
    else:
        raise I32CFSPProtocolError()

def request_game(connection:I32CFSP_connection)->READY:
    '''request game by sending AI_GAME to the server to be able to start playing the game'''
    _write_line(connection, 'AI_GAME')
    response=_read_line(connection)

    if response == 'READY':
        return READY
    else:
        raise I32CFSPProtocolError()

def send_command_and_column_number(connection: I32CFSP_connection, command: str, column_number: int)->OKAY or INVALID or WINNER_RED or WINNER_YELLOW:
    '''sending command of column protocal to the server and get the response: OKAY, or INVALID, or WINNER_RED or WINNER_YELLOW'''
    line=command+' '+str(column_number)
    _write_line(connection, line)
    response=_read_line(connection)
    
    if response=='OKAY':
        return OKAY
    elif response=='INVALID':
        return INVALID
    elif response=='WINNER_RED':
        return WINNER_RED
    elif response=='WINNER_YELLOW':
        return WINNER_YELLOW
    else:
        raise I32CFSPProtocolError()

def recieve_server_command_and_number(connection:I32CFSP_connection)->I32CFSP_move:
    '''Waiting for the messages from the server'''
    response=_read_line(connection)
    print('Server\'s move: '+response)
    print()
    count_words=response.split()
    if len(count_words)!=2 or (count_words[0]!='DROP' and count_words[0]!='POP'):
        raise I32CFSPProtocolError()
    try:
        column_number=int(count_words[1])
    except ValueError:
        raise I32CFSPProtocolError()

    command=count_words[0]
    column=column_number

    return I32CFSP_move(command,column)

def check_server_last_response(connection:I32CFSP_connection)-> WINNER_RED or WINNER_YELLOW or READY :
    '''checking the last protocal sending from the server in order to deicied the next move'''
    response=_read_line(connection)

    if response=='WINNER_RED':
        return WINNER_RED
    elif response=='WINNER_YELLOW':
        return WINNER_YELLOW
    elif response=='READY':
        return READY
    else:
        raise I32CFSPProtocolError()

def close(connection: I32CFSP_connection)->None:
    '''closing the connection with the server'''
    connection.socket.close()
    connection.input.close()
    connection.output.close()

#################################################################################
    
def _write_line(connection: I32CFSP_connection, line:str)->None:
    '''send the messsage to the server with the new line character'''
    connection.output.write(line+'\r\n')
    connection.output.flush()

def _read_line(connection:I32CFSP_connection)->str:
    '''read the message from the server without the new line character'''
    line=connection.input.readline()[:-1]
    return line

