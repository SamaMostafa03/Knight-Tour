initX, initY = 0 , 0
boardSize = 8 #5->30
dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]
grid =[ [0 for i in range(boardSize)]for j in range(boardSize)]
def isValid(x,y):
    return x>=0 and y>=0 and x<boardSize and y<boardSize and grid[x][y] == 0
def dfs(x,y,step):
    grid[x][y] = step
    if step == boardSize*boardSize:
        return 1
    availableMoves = []
    for i in range(8):
        xi , yi = x + dx[i] , y + dy[i]
        if isValid(xi,yi) :
            counter = 0
            for j in range(8):
                xj , yj = xi + dx[j] , yi + dy[j]
                if isValid(xj,yj) :
                    counter+=1
            availableMoves.append( (counter,xi,yi) )
    availableMoves.sort()
    for it in availableMoves:
        if dfs(it[1],it[2],step+1):
            return 1
    grid[x][y] = 0
    return 0
if __name__ == "__main__":  
    if dfs(initX,initY,1):
        for i in range(boardSize):
            for j in range(boardSize):
                print(grid[i][j] , end=" ")
            print()     