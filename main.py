
#Sudoku board
board = [
    [0,0,5,0,0,0,9,8,4],
    [0,0,0,9,6,0,0,0,3],
    [0,9,0,0,7,0,0,1,0],
    [0,8,3,0,5,9,0,3,7],
    [0,0,7,0,2,0,8,0,0],
    [1,3,0,7,6,0,5,4,0],
    [0,2,0,0,8,0,0,7,0],
    [7,0,0,2,0,1,0,0,0],
    [8,4,6,0,0,0,1,0,0]
]


def is_valid(board, num, idx):

    #check row
    if num in board[idx(1)]:
        return False
    
    #check column
    for i in range(len(board)):
        if num == board[[idx(0), i]]:
            return False

    #check box
    box_x = idx(0)//3
    box_y = idx(1)//3 
    for i range(box_x*3, box_x*3 + 3):
        for j range(box_y*3, box_y*3 + 3):
            if num == board[i, j]:
                return False

    return True 

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return (i, j)

    return None                
