#mean old woman playground test 1

_EMPTY = " "
_X = "X"
_O = "O"

values = [_EMPTY for i in range(0, 3)] * 3
last_move = None

def draw_board():
    print("   |   |   ")
    print(f" {values[0]} | {values[1]} | {values[2]} ")
    print("-----------")
    print(f" {values[3]} | {values[4]} | {values[5]} ")
    print("-----------")
    print(f" {values[6]} | {values[7]} | {values[8]} ")
    print("   |   |   ")

def end_game():
    print("Game ended!")
    exit()

def check_cross_right(specValues):
    return (specValues[0].value == specValues[4].value) and (specValues[4].value == specValues[8].value) and (specValues[0].value != _EMPTY)

def check_cross_left(specValues):
    return (specValues[2].value == specValues[4].value) and (specValues[4].value == specValues[6].value) and (specValues[2].value != _EMPTY)

def check_row(specValues, offset = 0):
    return (specValues[offset].value == specValues[offset + 1].value == specValues[offset + 2].value) and (specValues[offset].value != _EMPTY)

def check_column(specValues, offset = 0):
    return (specValues[offset].value == specValues[offset + 3].value == specValues[offset + 6].value) and (specValues[offset].value != _EMPTY)

def check_game_end(operation, argValues, argOffset = None):
    if(operation(argValues, argOffset) if argOffset != None else operation(argValues)):
        end_game()


def check_winner():
    for i in range(0, 3):
        check_game_end(check_row, values, i * 3)
        check_game_end(check_column, values, i)
    check_game_end(check_cross_right, values)
    check_game_end(check_cross_left, values)

def is_valid_position(position):
    return position >= 0 and position < 9

def receive_command():
    global last_move
    cmd = input("Enter your move [Position,Character]: ")
    [pos, char] = cmd.split(",")
    convPos = int(pos)

    if(not is_valid_position(convPos)):
        print("Invalid position received!")
        return
    
    if(values[convPos] != _EMPTY):
        return

    if((last_move != None) and (char.upper() == last_move)):
        return
    
    values[convPos] = _X if char.upper() == _X else _O if char.upper() == _O else _EMPTY
    last_move = values[convPos]

def run_game():
    run_game = True
    draw_board()

    while run_game:
        try:
            receive_command()
            draw_board()
            check_winner()
        except KeyboardInterrupt:
            print("\nGame cancelled...")
            run_game = False