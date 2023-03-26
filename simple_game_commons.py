#Tic tac toe game helper script - v0.1
#Author: Fernando A. C. de Barros - ECA - UERGS
import colorama

_EMPTY = " "
_X = "X"
_O = "O"

def check_cross_right(specValues):
    return (specValues[0].value == specValues[4].value) and (specValues[4].value == specValues[8].value) and (specValues[0].value != _EMPTY)

def check_cross_left(specValues):
    return (specValues[2].value == specValues[4].value) and (specValues[4].value == specValues[6].value) and (specValues[2].value != _EMPTY)

def check_row(specValues, offset = 0):
    return (specValues[offset].value == specValues[offset + 1].value == specValues[offset + 2].value) and (specValues[offset].value != _EMPTY)

def check_column(specValues, offset = 0):
    return (specValues[offset].value == specValues[offset + 3].value == specValues[offset + 6].value) and (specValues[offset].value != _EMPTY)

def is_valid_position(position):
    return position >= 0 and position < 9

def moveCursor(x, y):
    print("\033[%d;%dH" % (y, x), end="")

def draw_board(positions):
    print("   |   |   ")
    print(f" {positions[0].value} | {positions[1].value} | {positions[2].value} ")
    print("-----------")
    print(f" {positions[3].value} | {positions[4].value} | {positions[5].value} ")
    print("-----------")
    print(f" {positions[6].value} | {positions[7].value} | {positions[8].value} ")
    print("   |   |   ")

def draw_board_on_position(positions, startX, startY):
    moveCursor(startX, startY)
    print("   |   |   ")
    moveCursor(startX, startY + 1)
    print(f" {positions[0].value} | {positions[1].value} | {positions[2].value} ")
    moveCursor(startX, startY + 2)
    print("-----------")
    moveCursor(startX, startY + 3)
    print(f" {positions[3].value} | {positions[4].value} | {positions[5].value} ")
    moveCursor(startX, startY + 4)
    print("-----------")
    moveCursor(startX, startY + 5)
    print(f" {positions[6].value} | {positions[7].value} | {positions[8].value} ")
    moveCursor(startX, startY + 6)
    print("   |   |   ")

def receive_command(values, lastMove):
    cmd = input("Enter your move [Position,Character]: ")
    [pos, char] = cmd.split(",")
    convPos = int(pos)

    if(not is_valid_position(convPos)):
        print("Invalid position received!")
        return
    
    if(values[convPos] != _EMPTY):
        return

    if((lastMove != None) and (char.upper() == lastMove)):
        return
    
    values[convPos] = _X if char.upper() == _X else _O if char.upper() == _O else _EMPTY
    lastMove = values[convPos]

class GameEndException(Exception):
    pass

colorama.init()