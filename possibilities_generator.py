#Tic tac toe possibilities generator script - v0.1
#Author: Fernando A. C. de Barros - ECA - UERGS

import simple_game_commons as sp
from simple_game_commons import GameEndException

_BOARD_HEIGHT = 8
_BOARD_WIDTH = 11
_TREE_HEIGHT = _BOARD_HEIGHT + 4 + _BOARD_HEIGHT + 1 + 1

class Position:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.index = id

class Possibility:
    def __init__(self, id, lastMove, currentPositions = None):
        self.id = id
        self.lastMove = lastMove
        self.positions = Possibility.initializePositionsArray() if currentPositions == None else currentPositions
        self.nextPossibilities = self.generateNextPossibilities()

    def initializePositionsArray():
        return [Position(i, sp._EMPTY) for i in range(9)]

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
        if self.lastMove == sp._O or self.lastMove == sp._EMPTY:
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
            if i.value == sp._EMPTY:
                emptyPos.append(i)

        return emptyPos
    
    def draw_current(self):
        print(f"Drawing current positions of id {self.id}:")
        sp.draw_board(self.positions)
    
    def draw_possibilities(self):
        print("Drawing next possibilities:")
        cnt = 0
        for i in self.nextPossibilities:
            print(f"{cnt}:")
            sp.draw_board(i.positions)
            cnt += 1
    
    def draw_tree(self, startPositionY):
        sp.moveCursor(1, startPositionY)
        print("Possibility tree:")
        cnt = 1
        print(f"Current board {cnt} - ")
        sp.draw_board(self.positions)
        print("Next moves:")
        nextCnt = 0
        for pos in self.nextPossibilities:
            sp.draw_board_on_position(pos.positions, 1 + (nextCnt * (_BOARD_WIDTH + 2 + 1 + 2)), startPositionY + _BOARD_HEIGHT + 4)
            sp.moveCursor(1 + (nextCnt * ((_BOARD_WIDTH + 2 + 1 + 2))) + _BOARD_WIDTH + 2, startPositionY + _BOARD_HEIGHT + 3 + (_BOARD_HEIGHT / 2))
            print("-",  end="")
            nextCnt += 1
        
        sp.moveCursor(1, startPositionY + _BOARD_HEIGHT + 4 + _BOARD_HEIGHT + 1)
    
    def draw_horizontally(self, initialX, initialY, possibilities):
        for i in possibilities:
            sp.draw_board(i.positions)
            sp.moveCursor(initialX + _BOARD_WIDTH + 1, initialY)

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
        sp.moveCursor(1, startY + h)
        for i in range((_BOARD_WIDTH + 5) * 9):
            print(" ", end="")

print("Generating possibilities...")
possib = Possibility(0, sp._EMPTY)
print(f"Generated -> {check_possibility_quantity(possib)} game possibilities")
possib.draw_tree(4)

run_simulation = True
currentPossib = possib
offset = 0
while run_simulation:
    try:
        if(len(currentPossib.nextPossibilities) == 0):
            raise GameEndException("We have a winner!" if currentPossib.isGameFinished() else "No more positions available. Game finished...")
        
        #User can choose the next move by inserting a number from 0 to n-1, where n is the number of possible next moves shown in the console
        control = input("Choose a path [0-n]: ") 
        desiredPoss = int(control)
        currentPossib = currentPossib.nextPossibilities[desiredPoss]
        clear_tree(4)
        currentPossib.draw_tree(4)
    except KeyboardInterrupt:
        print("Simulation ended...")
        run_simulation = False
    except ValueError:
        print("Invalid value")
        offset += 2
    except GameEndException as e:
        print(str(e))
        shouldRestart = input("Do you want to restart [y/n]? ")
        if(shouldRestart.upper() == "Y"):
            currentPossib = possib
            clear_tree(5)
            currentPossib.draw_tree(4)
        else:
            print("Closing simulation...")
            run_simulation = False