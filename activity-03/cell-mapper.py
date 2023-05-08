#Universidade Estadual do Rio Grande do Sul - UERGS
#Curso: Engenharia de Controle e Automação - Disciplina: Inteligência Artificial
#Aluno: Fernando Augusto Caletti de Barros
#Ano: 2023

import numpy as np

START_CELL_TC = 1
TARGET_CELL_TC = 2

class Cell:
    #Construtor: Recebe como argumentos os parametros especificados no array de dados de coordenadas da atividade.
    def __init__(self, R = 0, C = 0, CN = 0, CL = 0, CS = 0, CO = 0, TC = 0):
        self.id = 0
        self.data = [R, C, CN, CL, CS, CO, TC]
    
    def toStr(self):
        #return f'|R:{self.getRow()},C:{self.getColumn()}|'
        return f'|{self.id}|'

    def print(self):
        print(self.toStr())

    def getRow(self):
        return self.data[0]

    def getColumn(self):
        return self.data[1]

    #Above connection
    def getCn(self):
        return self.data[2]

    #Right connection
    def getCl(self):
        return self.data[3]

    #Below connection
    def getCs(self):
        return self.data[4]

    #Left connection
    def getCo(self):
        return self.data[5]

    #0 = Empty, 1 = Initial position, 2 = Final position
    def getTc(self):
        return self.data[6]

    def getNextPossibilities(self, organizedMap, previousCellId):
        possibilities = []
        if self.getCn() == 1:
            possibilities.append(organizedMap[self.getRow() - 1][self.getColumn()])
        if self.getCl() == 1:
            possibilities.append(organizedMap[self.getRow()][self.getColumn() + 1])
        if self.getCs() == 1:
            possibilities.append(organizedMap[self.getRow() + 1][self.getColumn()])
        if self.getCo() == 1:
            possibilities.append(organizedMap[self.getRow()][self.getColumn() - 1])
        
        for poss in possibilities:
            if poss.id == previousCellId:
                possibilities.remove(poss)
                break

        result = {"previousId": previousCellId, "nextPoss": possibilities}
        return result

class TreeNode:
    def __init__(self, cell, previousCellId):
        self.cell = cell
        self.previousCellId = previousCellId

class TreeRow:
    def __init__(self, index = 0, nodes = None):
        self.nodes = nodes if nodes != None else []
        self.index = index

    def drawRow(self):
        currentPrevId = self.nodes[0].previousCellId
        cpltList = []
        minList = []
        for data in self.nodes:
            if data.previousCellId == currentPrevId:
                minList.append(data)
            else:
                currentPrevId = data.previousCellId
                cpltList.append(minList.copy())
                minList = [data]
        
        cpltList.append(minList.copy())
        strList = []
        for specList in cpltList:
            specStr = [data.cell.toStr() for data in specList]
            composedStr = '-'.join(specStr)
            previd = specList[0].previousCellId
            strList.append(f'{previd if previd != None else "S"}:[{composedStr}]')

        finalComposedStr = ' '.join(strList)

        print(finalComposedStr)
        return finalComposedStr

def buildOrganizedMap(targetMap, maxRow, maxCol):
    resultMap = [np.empty(maxCol + 1, dtype=Cell) for i in range(maxRow + 1)]
    for cell in targetMap:
        resultMap[cell.getRow()][cell.getColumn()] = cell
    
    return resultMap

def buildRecursiveTree(index, currentTreeRow, organizedMap):
    tree = []
    if index == 0:
        tree.append(currentTreeRow)
        tree.extend(buildRecursiveTree(index + 1, currentTreeRow, organizedMap))
    else:
        nextNodes = []
        for node in currentTreeRow.nodes:
            nextCells = node.cell.getNextPossibilities(organizedMap, node.previousCellId)
            nextNodes.extend([TreeNode(cell, node.cell.id) for cell in nextCells["nextPoss"]])

        if len(nextNodes) == 0:
            return tree

        nextRow = TreeRow(index + 1, nextNodes)
        tree.append(nextRow)
        tree.extend(buildRecursiveTree(index + 1, nextRow, organizedMap))
    
    return tree

def buildPossibilityTree(targetMap):
    state = 0
    resultTree = []
    startCell = None
    targetCell = None
    maxRow = 0
    maxCol = 0
    
    for i in range(len(targetMap)):
        cell = targetMap[i]
        cell.id = i
        if state == 0 and cell.getTc() == START_CELL_TC:
            state = 1
            startCell = cell

        if cell.getTc() == TARGET_CELL_TC:
            targetCell = cell

        if cell.getColumn() > maxCol:
            maxCol = cell.getColumn()
        
        if cell.getRow() > maxRow:
            maxRow = cell.getRow()

    organizedMap = buildOrganizedMap(targetMap, maxRow, maxCol)
    resultTree = buildRecursiveTree(0, TreeRow(0, [TreeNode(startCell, None)]), organizedMap)

    return resultTree, startCell, targetCell

def findRouteToTarget(tree, start, target, state = 0):
    targetNode = None
    targetRowIndex = None
    positionCounter = 0
    for row in tree:
        for node in row.nodes:
            if node.cell.id == target.id:
                targetNode = node
                break
        
        if targetNode != None:
            targetRowIndex = row.index - 1
            break

    recursiveRoute = recursiveRouteBuilder(targetNode, start.id, tree, targetRowIndex)
    return recursiveRoute[::-1]

    
def recursiveRouteBuilder(currentNode, startCellId, tree, index, state = 0):
    result = []
    if currentNode.cell.id == startCellId:
        return [startCellId]

    result.append(currentNode.cell.id)
    result.extend(recursiveRouteBuilder(findNodeByCellIdInRow(tree, index - 1, currentNode.previousCellId), startCellId, tree, index - 1, 1))

    return result

def findNodeByCellIdInRow(tree, index, cellId):
    targetRow = tree[index]
    if len(targetRow.nodes) == 0:
        return None

    for node in targetRow.nodes:
        if node.cell.id == cellId:
            return node
    
    return None

def run(map):
    resultTree, startCell, targetCell = buildPossibilityTree(globalMap)
    for row in resultTree:
        row.drawRow()

    route = findRouteToTarget(resultTree, startCell, targetCell)
    print("Result route ->")
    print(route)

#Constrói array principal para o mapa.
globalMap = [
    Cell(0, 0, 0, 1, 0, 0, 1),
    Cell(0, 1, 0, 1, 1, 1, 0),
    Cell(0, 2, 0, 0, 0, 1, 0),
    Cell(1, 0, 0, 1, 1, 0, 0),
    Cell(1, 1, 1, 1, 1, 1, 0),
    Cell(1, 2, 0, 0, 0, 1, 0),
    Cell(2, 0, 1, 0, 0, 0, 0),
    Cell(2, 1, 1, 1, 0, 0, 0),
    Cell(2, 2, 0, 0, 0, 1, 2)
]

#Roda construção da árvore.
run(globalMap)