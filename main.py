
#Sudoku board
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]


def solve(board):
    #check if index is empty
    indx = is_empty(board)

    #board is filled out and program exits
    if not indx:
        return True

    row = indx[0]
    col = indx[1]

    #check for valid values to fill in for the position (index)
    for i in range (1,10):
        if is_valid(board, i, indx):
            board[row][col] = i

            if solve(board):
                return True      
            
            board[row][col] = 0


    return False

def is_valid(board, num, idx):

    row = idx[0]
    col = idx[1]

    #check row
    if num in board[row]:
        return False
    
    #check column
    for i in range(len(board)):
        if num == board[i][col]:
            return False

    #check box
    box_x = row//3
    box_y = col//3 
    for i in range(box_x*3, box_x*3 + 3):
        for j in range(box_y*3, box_y*3 + 3):
            if num == board[i][j]:
                return False

    return True 

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return [i, j]

    return None                


solve(board)

for i in board:
    print(i)