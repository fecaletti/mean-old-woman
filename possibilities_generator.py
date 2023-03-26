import numpy as np
import colorama
import simple_game as sp

_O = "O"
_X = "X"
_EMPTY = " "

_BOARD_HEIGHT = 8
_BOARD_WIDTH = 11

colorama.init()

def moveCursor(x, y):
    print("\033[%d;%dH" % (y, x), end="")

def initializePositionsArray():
    return [Position(i, sp._EMPTY) for i in range(9)]

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

class Position:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.index = id

class Possibility:
    def __init__(self, id, lastMove, currentPositions = None):
        self.id = id
        self.lastMove = lastMove
        self.positions = initializePositionsArray() if currentPositions == None else currentPositions
        self.nextPossibilities = self.generateNextPossibilities()

    #For the first version, we will consider that our possibility will be the 'X'
    def generateNextPossibilities(self):
        nextPossibilities = []
        emptyPositions = self.calculateEmptyPositions()
        nextMove = self.getNextMove()
        for i in emptyPositions:
            newPossibilityPositions = [Position(pos.id, pos.value) for pos in self.positions]
            newPossibilityPositions[i.id].value = nextMove
            newPossibility = Possibility(0, nextMove, newPossibilityPositions)
            nextPossibilities.append(newPossibility)
        return nextPossibilities

    def getNextMove(self):
        if self.lastMove == _O or self.lastMove == _EMPTY:
            return sp._X
        else:
            return sp._O
        
    def check_game_end(self, operation, argValues, argsOffset = None):
        if(operation(argValues, argsOffset) if argsOffset != None else operation(argValues)):
            raise Exception("This game is finished")
    
    def isGameFinished(self):
        try:
            for i in range(0, 3):
                self.check_game_end(sp.check_row, self.positions, i * 3)
                self.check_game_end(sp.check_column, self.positions, i)
            self.check_game_end(sp.check_cross_right, self.positions)
            self.check_game_end(sp.check_cross_left, self.positions)

            return False
        except Exception:
            return True

    def calculateEmptyPositions(self):
        emptyPos = []
        if self.isGameFinished():
            return emptyPos
        
        for i in self.positions:
            if i.value == _EMPTY:
                emptyPos.append(i)

        return emptyPos
    
    def draw_current(self):
        print(f"Drawing current positions of id {self.id}:")
        draw_board(self.positions)
    
    def draw_possibilities(self):
        print("Drawing next possibilities:")
        cnt = 0
        for i in self.nextPossibilities:
            print(f"{cnt}:")
            draw_board(i.positions)
            cnt += 1
    
    def draw_tree(self, startPositionY):
        moveCursor(1, startPositionY)
        print("Possibility tree:") #STart + 1
        cnt = 1
        print(f"Current board {cnt} - ") #Start + 2
        draw_board(self.positions) #Start + BOARD_HEIGHT + 3
        print("Next moves:") #Start + BOARD_HEIGHT + 4
        nextCnt = 0
        for pos in self.nextPossibilities:
            draw_board_on_position(pos.positions, 1 + (nextCnt * (_BOARD_WIDTH + 2 + 1 + 2)), startPositionY + _BOARD_HEIGHT + 4)
            moveCursor(1 + (nextCnt * ((_BOARD_WIDTH + 2 + 1 + 2))) + _BOARD_WIDTH + 2, startPositionY + _BOARD_HEIGHT + 3 + (_BOARD_HEIGHT / 2))
            print("-",  end="")
            # moveCursor(_BOARD_WIDTH + 2, initialY - (_BOARD_HEIGHT / 2))
            # print(" --> ")
            # initialX = _BOARD_WIDTH + 7
            # initialY = (3 + _BOARD_HEIGHT) + ((_BOARD_HEIGHT * nextCnt) / 2)
            # moveCursor(initialX, initialY)
            # self.draw_horizontally(initialX, initialY, pos.nextPossibilities)
            nextCnt += 1
        
        moveCursor(1, startPositionY + _BOARD_HEIGHT + 4 + _BOARD_HEIGHT + 1)
    
    def draw_horizontally(self, initialX, initialY, possibilities):
        for i in possibilities:
            draw_board(i.positions)
            moveCursor(initialX + _BOARD_WIDTH + 1, initialY)

class GameEndException(Exception):
    pass


# def calculateAllPossibilities(start):

def check_possibility_quantity(poss):
    possCnt = 0
    specNextPossibilities = len(poss.nextPossibilities)
    if(specNextPossibilities > 0):
        possCnt += specNextPossibilities
        for nposs in poss.nextPossibilities:
            possCnt += check_possibility_quantity(nposs)

    return possCnt

def recursive_print(poss):
    poss.draw_current()
    if(len(poss.nextPossibilities) == 0):
        return
    
    recursive_print(poss.nextPossibilities[0])

def clear_tree(startY):
    for h in range(_TREE_HEIGHT):
        moveCursor(1, startY + h)
        for i in range((_BOARD_WIDTH + 5) * 9):
            print(" ", end="")

# initialValues = np.array([5, 4, 5, 6])
# possib = Possibility(0, _EMPTY)
# possib.draw_current()
# possib.draw_possibilities()

# possib.draw_tree()

# erasedPos = initializePositionsArray()
# draw_board_on_position(erasedPos, 1, 2)
# moveCursor(_BOARD_WIDTH + 3, (_BOARD_HEIGHT / 2) + 1)
# print(" ---> ")
# draw_board_on_position(erasedPos, _BOARD_WIDTH + 3 + 6 + 3, 2)
print("Generating possibilities...")
possib = Possibility(0, _EMPTY)
# print("Possibilities generated!")
print(f"Generated -> {check_possibility_quantity(possib)}")
possib.draw_tree(3)
# recursive_print(possib)

_TREE_HEIGHT = _BOARD_HEIGHT + 4 + _BOARD_HEIGHT + 1 + 1

run_simulation = True
currentPossib = possib
offset = 0
while run_simulation:
    try:
        stateCount = 1

        if(len(currentPossib.nextPossibilities) == 0):
            raise GameEndException("Happy end!")
        
        control = input("Choose a path: ")
        desiredPoss = int(control)
        currentPossib = currentPossib.nextPossibilities[desiredPoss]
        # currentPossib.draw_tree((stateCount * (_TREE_HEIGHT + 3)) + offset)
        clear_tree(3)
        currentPossib.draw_tree(3)
        stateCount += 1
    except KeyboardInterrupt:
        print("Simulation ended...")
        run_simulation = False
    except ValueError:
        print("Invalid value")
        offset += 2
    except GameEndException as e:
        print(str(e))
        run_simulation = False