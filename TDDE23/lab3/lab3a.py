def new_board():
    #crates a new board
    return {}

def is_free(board,x,y):
    #checks if space on cordinates x,y is free
    return not (x,y) in board.keys()

def place_piece(board,x,y,player):
    #places a piece on cordinates x,y
    free = is_free(board,x,y)
    if free:
        board[(x,y)] = player
    return free

def get_piece(board,x,y):
    #return piece on a specific cordinate
    piece_exists = not is_free(board,x,y)
    if piece_exists:
        return board[(x,y)]
    return piece_exists

def remove_piece(board,x,y):
    #removes a piece from specific cordinate
    piece_exists = not is_free(board,x,y)
    if piece_exists:
        del board [(x,y)]
    return piece_exists

def move_piece(board,x,y,newx,newy):
    #moves a piece from specific cordinate to specific cordinate
    if is_free(board,newx,newy) == False:
        return False

    if not is_free(board, x, y):
        player = get_piece(board,x,y)
        remove_piece(board,x,y)
        place_piece(board,newx,newy,player)
        return True
    return False 





def count(board,RoC,amount,player):
    #checks every key in keys on their respective x and y values depending on
    #if it is searching in a row or column, then returns the number of players
    #in the row or column
    count = 0
    for key in board.keys():
        row = 0
        if RoC == "row":
            row = 1
        if key[row] == amount and get_piece(board,key[0],key[1]) == player:
            count += 1
    return count

def nearest_piece(board,x,y):
    #finds nearest piece for cordinates x,y
    #checks if cord is free, if not free returns same x,y cordinates
    #if free checks distance to every piece and the retuns the closest piece
    min_dist = 0
    n_player = False
    if not is_free(board,x,y):
        return(x,y)
    for key in board.keys():
        dist = (x-key[0]) **2 + (y-key[1]) **2
        if min_dist==0:
            min_dist= dist
        if dist <= min_dist:
            min_dist = dist
            n_player = key
    return n_player