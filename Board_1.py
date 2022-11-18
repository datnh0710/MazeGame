from Constants import NUM_ROWS, CELL_VALUES, TERMINAL_CELLS, WALL_VALUES

class Board(object):
    cellValues = {} # Maps cell (x, y) to reward r

    def __init__(self, numRows = NUM_ROWS):
        self.numRows = numRows
        self.initCellRewards()

    def initCellRewards(self):
        initial_value = 1000
        queue = []
        queue.append(TERMINAL_CELLS[0])
        x = [1,0,-1,0]
        y = [0,1,0,-1]
        visited = [False] * (NUM_ROWS*NUM_ROWS)
        visited[TERMINAL_CELLS[0][0] + TERMINAL_CELLS[0][1]*NUM_ROWS] = True
        while len(queue) >0:
            size = len(queue)
            while size >0:
                size-=1
                cell = queue.pop(0)
                self.cellValues[cell] = initial_value
                for i in range(0,4):
                    new_cell = (cell[0]+x[i],cell[1]+y[i])
                    if new_cell[0] >=0 and new_cell[0] < NUM_ROWS and new_cell[1] >=0 and new_cell[1] < NUM_ROWS and visited[new_cell[0] + new_cell[1]*NUM_ROWS] == False and new_cell not in WALL_VALUES:
                        queue.append(new_cell)
                        visited[new_cell[0] + new_cell[1]*NUM_ROWS] = True

            initial_value-=1

        print("doneeee")


        # for xPos in range(NUM_ROWS):
        #     for yPos in range(NUM_ROWS):
        #         print(self.cellValues[(xPos, yPos)])

    def createPenaltyCells(self):
        for cell, val in CELL_VALUES:
            self.cellValues[cell[0], cell[1]] = val

    def isTerminalCell(self, coord):
        return coord in TERMINAL_CELLS

    def isValidCell(self, coord, action):
        xCoord, yCoord = self.getCellAfterAction(coord, action)
        #if(0 <= xCoord < NUM_ROWS  and 0 <= yCoord < NUM_ROWS):
            #if(xCoord,yCoord) not in self.cellValues:
            #    return True
            #return True
        #return False
        return(0 <= xCoord < NUM_ROWS  and 0 <= yCoord < NUM_ROWS and (xCoord,yCoord) not in WALL_VALUES)
        # return (0 <= xCoord < NUM_ROWS  and 0 <= yCoord < NUM_ROWS )

    def getCellAfterAction(self, coord, action):
        xCoord, yCoord = coord
        if action == 'left':
            xCoord-=1
        elif action == 'right':
            xCoord+=1
        elif action == 'up':
            yCoord+=1
        elif action == 'down':
            yCoord-=1
        
        return (xCoord, yCoord)

    def getCellValue(self, coord):
        if(coord in CELL_VALUES):
            return 1
        return self.cellValues[coord]

    def getCells(self):
        return self.cellValues.keys()

    def getCellMap(self):
        return self.cellValues

    def getRewardCellsMap(self):
        return {cell: val for cell, val in self.cellValues.items() if val > 0}

    def getPenaltyCellsMap(self):
        return {cell: val for cell, val in self.cellValues.items() if val < 0}
