from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
from functools import cmp_to_key

class MyBoard(Board):
    def __init__(self,col,row,k,g):
        Board.__init__(self,col,row,k,g)

    def make_my_move(self,col,row,player):
        self.board[row][col] = player

    def revert_my_move(self,col,row):
        self.board[row][col] = 0

    def show_my_board(self):
        print("#####")
        for i in range(0, self.row): 
            print(self.board[i])
        print("#####")

    def get_my_board_val(self, col, row):
        return self.board[row][col]

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():
    col = 0
    row = 0
    k = 0
    g = 0
    possibleMoves = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]
    
    def __init__(self,col,row,k,g):
        self.g = g
        self.col = col
        self.row = row
        self.k = k
        self.objB = MyBoard(col,row,k,g)

        self.possibleMovesForGravity = []
        for c in range(0, self.col):
            self.possibleMovesForGravity.insert(c, row-1)

        self.adj_to_opponent_move = set()

    def check_next_win(self, tempCol, tempRow, player):        
        # if the move is invalid then check next possible position
        if(not self.objB.is_valid_move(tempCol, tempRow, True)):
            return False

        # if the move is possible temporarily make the move
        self.objB.make_my_move(tempCol, tempRow, player)

        # check if the player wins by this move then we move to that position
        if(self.objB.is_win() == player):
            self.objB.revert_my_move(tempCol, tempRow)
            return True

        # we remove the temporary move from the board
        self.objB.revert_my_move(tempCol, tempRow)
        return False

    def get_heuristic_moves(self):
        heuristic_val = []

        for c in range(0,self.col):
            heuristic_val.insert(c, 0)
            r = self.possibleMovesForGravity[c]
            if(r<0):
                continue
            #print(c, r)
            # Calculate left and right of this position and if they are valid
            left = self.objB.is_valid_move(c-1, r, False)
            right = self.objB.is_valid_move(c+1, r, False)
            #print(left, right)

            if(left and right):
                if(self.objB.get_my_board_val(c-1, r)==2 and self.objB.get_my_board_val(c+1, r)==2):
                    heuristic_val[c] += 2

                if(self.objB.get_my_board_val(c-1, r)==1 and self.objB.get_my_board_val(c+1, r)==1):
                    heuristic_val[c] += 4
                    


            if(left and c>=(self.k-1) ):
                #print("l1")
                #print(self.objB.get_my_board_val(c-1, r))
                if(self.objB.get_my_board_val(c-1, r) == 2):
                    #print("l2")
                    heuristic_val[c] += 1

                if(self.objB.get_my_board_val(c-1, r) == 1):
                    #print("l2")
                    heuristic_val[c] += 3

            if(right and ((self.col-c)>=self.k) ):
                #print("r1")
                #print(self.objB.get_my_board_val(c+1, r))
                if(self.objB.get_my_board_val(c+1, r) == 2):
                    #print("r2")
                    heuristic_val[c] += 1

                if(self.objB.get_my_board_val(c+1, r) == 1):
                    #print("r2")
                    heuristic_val[c] += 3

            # Left-Cell-Right
            # Calculate top-left and bottom-right of this position and if they are valid
            top_left = False
            bottom_right = False

            if(r+self.col-c>=self.k):
                top_left = self.objB.is_valid_move(c-1, r-1, False)

                if(top_left and self.objB.get_my_board_val(c-1, r-1) == 2):
                    heuristic_val[c] += 2

                if(top_left and self.objB.get_my_board_val(c-1, r-1) == 1):
                    heuristic_val[c] += 4

                bottom_right = self.objB.is_valid_move(c+1, r+1, False)

                if(bottom_right and self.objB.get_my_board_val(c+1, r+1) == 2):
                    heuristic_val[c] += 2

                if(bottom_right and self.objB.get_my_board_val(c+1, r+1) == 1):
                    heuristic_val[c] += 4

            # Both
            if(top_left and bottom_right):
                if(self.objB.get_my_board_val(c-1, r-1)==2 and self.objB.get_my_board_val(c+1, r+1)==2):
                    heuristic_val[c] += 3

                if(self.objB.get_my_board_val(c-1, r-1)==1 and self.objB.get_my_board_val(c+1, r+1)==1):
                    heuristic_val[c] += 5


            # Calculate top-right and bottom-left of this position and if they are valid
            top_right = False
            bottom_left = False

            if(c+r >= self.k-1):
                top_right = self.objB.is_valid_move(c+1, r-1, False)

                if(top_right and self.objB.get_my_board_val(c+1, r-1) == 2):
                    heuristic_val[c] += 2

                if(top_right and self.objB.get_my_board_val(c+1, r-1) == 1):
                    heuristic_val[c] += 4

                bottom_left = self.objB.is_valid_move(c-1, r+1, False)

                if(bottom_left and self.objB.get_my_board_val(c-1, r+1) == 2):
                    heuristic_val[c] += 2

                if(bottom_left and self.objB.get_my_board_val(c-1, r+1) == 1):
                    heuristic_val[c] += 4

            if(top_right and bottom_left):
                if(self.objB.get_my_board_val(c+1, r-1)==2 and self.objB.get_my_board_val(c-1, r+1)==2):
                    heuristic_val[c] += 3

                if(self.objB.get_my_board_val(c+1, r-1)==1 and self.objB.get_my_board_val(c-1, r+1)==1):
                    heuristic_val[c] += 5

        

        list_return = []
        for i in range(0, self.col):
            list_return.insert(i, (i,heuristic_val[i]) )

        #print(list_return)
        return list_return

    def get_heuristic_moves_gravity_off(self):
        max_col = 0
        max_row = 0
        max_score = 0

        for c in range(0,self.col):
            for r in range(0,self.row):
                curr_score = 0
                
                if(not self.objB.is_valid_move(c, r, True)):
                    continue

                # print("c: ", c, ", r:", r)
                # Calculate left and right of this position and if they are valid
                left = self.objB.is_valid_move(c-1, r, False)
                right = self.objB.is_valid_move(c+1, r, False)
                # print(left, right)

                if(left and right):
                    if(self.objB.get_my_board_val(c-1, r)==2 and self.objB.get_my_board_val(c+1, r)==2):
                        curr_score += 4
                        # print("left-right-1")
                    if(self.objB.get_my_board_val(c-1, r)==1 and self.objB.get_my_board_val(c+1, r)==1):
                        curr_score += 2
                        # print("left-right-2")
                    
                if(left):
                    #print("l1")
                    #print(self.objB.get_my_board_val(c-1, r))
                    if(self.objB.get_my_board_val(c-1, r) == 2):
                        #print("l2")
                        curr_score += 3
                        # print("left-right-3")

                    if(self.objB.get_my_board_val(c-1, r) == 1):
                        #print("l2")
                        curr_score += 1
                        # print("left-right-4")

                if(right):
                    #print("r1")
                    #print(self.objB.get_my_board_val(c+1, r))
                    if(self.objB.get_my_board_val(c+1, r) == 2):
                        #print("r2")
                        curr_score += 3
                        # print("left-right-5")

                    if(self.objB.get_my_board_val(c+1, r) == 1):
                        #print("r2")
                        curr_score += 1
                        # print("left-right-6")

                top = self.objB.is_valid_move(c, r-1, False)
                bottom = self.objB.is_valid_move(c, r+1, False)
                if(top and bottom):
                    # print("tb")
                    if(self.objB.get_my_board_val(c, r-1)==2 and self.objB.get_my_board_val(c, r+1)==2):
                        curr_score += 4
                        # print("top-bottom-1")

                    if(self.objB.get_my_board_val(c, r-1)==1 and self.objB.get_my_board_val(c, r+1)==1):
                        curr_score += 2
                        # print("top-bottom-2")


                if(bottom):
                    # print("bottom")
                    #print(self.objB.get_my_board_val(c-1, r))
                    if(self.objB.get_my_board_val(c, r+1) == 2):
                        #print("l2")
                        curr_score += 3
                        # print("top-bottom-3")

                    if(self.objB.get_my_board_val(c, r+1) == 1):
                        #print("l2")
                        curr_score += 1
                        # print("top-bottom-4")
                
                if(top):
                    #print("r1")
                    #print(self.objB.get_my_board_val(c+1, r))
                    if(self.objB.get_my_board_val(c, r-1) == 2):
                        #print("r2")
                        curr_score += 3
                        # print("top-bottom-5")

                    if(self.objB.get_my_board_val(c, r-1) == 1):
                        #print("r2")
                        curr_score += 1
                        # print("top-bottom-6")

                # Left-Cell-Right
                # Calculate top-left and bottom-right of this position and if they are valid
                top_left = False
                bottom_right = False

                if(r+self.col-c>=self.k):
                    top_left = self.objB.is_valid_move(c-1, r-1, False)

                    if(top_left and self.objB.get_my_board_val(c-1, r-1) == 2):
                        curr_score += 3
                        # print("topleft-bottomright-1")

                    if(top_left and self.objB.get_my_board_val(c-1, r-1) == 1):
                        curr_score += 1
                        # print("topleft-bottomright-2")

                    bottom_right = self.objB.is_valid_move(c+1, r+1, False)

                    if(bottom_right and self.objB.get_my_board_val(c+1, r+1) == 2):
                        curr_score += 3
                        # print("topleft-bottomright-3")

                    if(bottom_right and self.objB.get_my_board_val(c+1, r+1) == 1):
                        curr_score += 1
                        # print("topleft-bottomright-4")

                # Both
                if(top_left and bottom_right):
                    if(self.objB.get_my_board_val(c-1, r-1)==2 and self.objB.get_my_board_val(c+1, r+1)==2):
                        curr_score += 4
                        # print("topleft-bottomright-5")

                    if(self.objB.get_my_board_val(c-1, r-1)==1 and self.objB.get_my_board_val(c+1, r+1)==1):
                        curr_score += 2
                        # print("topleft-bottomright-6")


                # Calculate top-right and bottom-left of this position and if they are valid
                top_right = False
                bottom_left = False

                if(c+r >= self.k-1):
                    top_right = self.objB.is_valid_move(c+1, r-1, False)

                    if(top_right and self.objB.get_my_board_val(c+1, r-1) == 2):
                        curr_score += 3
                        # print("topright-bottomleft-1")

                    if(top_right and self.objB.get_my_board_val(c+1, r-1) == 1):
                        curr_score += 1
                        # print("topright-bottomleft-2")

                    bottom_left = self.objB.is_valid_move(c-1, r+1, False)

                    if(bottom_left and self.objB.get_my_board_val(c-1, r+1) == 2):
                        curr_score += 3
                        # print("topright-bottomleft-3")

                    if(bottom_left and self.objB.get_my_board_val(c-1, r+1) == 1):
                        curr_score += 1
                        # print("topright-bottomleft-4")

                if(top_right and bottom_left):
                    if(self.objB.get_my_board_val(c+1, r-1)==2 and self.objB.get_my_board_val(c-1, r+1)==2):
                        curr_score += 4
                        # print("topright-bottomleft-5")

                    if(self.objB.get_my_board_val(c+1, r-1)==1 and self.objB.get_my_board_val(c-1, r+1)==1):
                         curr_score += 2
                        #  print("topright-bottomleft-6")

                # print("current score: ", curr_score)
                if(curr_score > max_score):
                    max_score = curr_score
                    max_col = c
                    max_row = r

            #print(list_return)
        return max_col, max_row

    def add_adj_cells(self, move):
        max_score = 0
        max_score_row = 0
        max_score_col = 0
        # check all the cells
        for row in range(0, self.row):
            for col in range(0, self.col):
                if(not self.objB.is_valid_move(col, row, True)):     
                    continue

                # calculate the heuristic of how good is this place based on 
                # h(c) = number of adjecent cells with 1 + number of adjecent cells with 2
                score = 0
                for adj in self.possibleMoves:
                    tmpCol = col + adj[0]
                    tmpRow = row + adj[1]
                    if(not self.objB.is_valid_move(tmpCol, tmpRow, False)):     
                        continue

                    if(self.objB.get_my_board_val(tmpCol, tmpRow) == 1):
                        score += 2

                    if(self.objB.get_my_board_val(tmpCol, tmpRow) == 2):
                        score += 1

                if(score > max_score):
                    max_score = score
                    max_score_row = row
                    max_score_col = col

        return max_score_col, max_score_row

    def get_move(self,move):
        if self.g == 0:
            # we move first
            if(move.col == -1 and move.row == -1):
                # take middle element so that increases connect on many sides
                newCol = math.ceil((self.col-1)/2)
                newRow = math.ceil((self.row-1)/2)
            
            # subsequent moves
            else:
                #set recent move of player 2 on board
                self.objB.make_my_move(move.col, move.row, 2)

                # add all adjecent cells which are empty to possible moves to choose from
                # newCol, newRow = self.add_adj_cells(move)

                newCol, newRow = self.get_heuristic_moves_gravity_off()
                print("newCol: ", newCol, ", newRow: ", newRow)
                #self.objB.my_show_board();        
            
                # check around this move if it makes it win for 2
                for r in range(0, self.row):
                    for c in range(0, self.col):

                        # if this move makes player2 to win then move to that position
                        if(self.check_next_win(c, r, 2) | self.check_next_win(c, r, 1)):
                            self.objB.make_my_move(c, r, 1)
                            return Move(c,r)

                # # else if no such move makes player2 to win then make a random move
                # newCol = randint(0,self.col-1)
                # newRow = randint(0,self.row-1)

                # while(not self.objB.is_valid_move(newCol, newRow, True)):
                #     newCol = randint(0,self.col-1)
                #     newRow = randint(0,self.row-1)
            
            self.objB.make_my_move(newCol, newRow, 1)
            
            return Move(newCol,newRow)

        elif self.g == 1:
            if(move.col == -1 and move.row == -1):
                # take middle element so that increases connect on many sides
                newCol = math.ceil((self.col-1)/2)
                self.objB.make_my_move(newCol, self.possibleMovesForGravity[newCol], 1)
                self.possibleMovesForGravity[newCol] -= 1
                return Move(newCol, self.possibleMovesForGravity[newCol] + 1)

            else:
                #print("Opponent Move: ", move.col, self.possibleMovesForGravity[move.col])
                # print("Opponent Move: ", move.col, move.row)

                self.objB.make_my_move(move.col, self.possibleMovesForGravity[move.col], 2)
                #print("Make Opponent Move")
                self.possibleMovesForGravity[move.col] -= 1
                # print(move.col, self.possibleMovesForGravity[move.col])
                
                # print(self.possibleMovesForGravity)
                for c in range(0, self.col):
                    if(self.possibleMovesForGravity[c] < 0):
                        continue
                    
                    #print(c, self.possibleMovesForGravity[c])
                    #print(self.check_opponent_win(c, self.possibleMovesForGravity[c]))

                    if(self.check_next_win(c, self.possibleMovesForGravity[c], 2) | self.check_next_win(c, self.possibleMovesForGravity[c], 1)):
                        self.objB.make_my_move(c, self.possibleMovesForGravity[c], 1)
                        self.possibleMovesForGravity[c] -= 1
                        #print("My Move: ", c, self.possibleMovesForGravity[c]+1)
                        #print("Poss Move: ", self.possibleMovesForGravity)
                        return Move(c, self.possibleMovesForGravity[c]+1)
                
                # sort by the evaluation result
                evalList = self.get_heuristic_moves()
                evalList.sort(key = lambda evalList: -evalList[1])

                for i in range(0, len(evalList)):
                    c = evalList[i][0]
                    if(self.possibleMovesForGravity[c] < 0):
                        continue

                    #print("c: ", c)
                    #print("Befroe Poss Move: ", self.possibleMovesForGravity)
                    self.objB.make_my_move(c, self.possibleMovesForGravity[c], 1)
                    self.possibleMovesForGravity[c] -= 1
                    #print("After Poss Move: ", self.possibleMovesForGravity)

                    if(self.check_next_win(c, self.possibleMovesForGravity[c], 2)):
                        #print("Here", c)
                        self.possibleMovesForGravity[c] += 1
                        self.objB.revert_my_move(c, self.possibleMovesForGravity[c])
                        continue

                    #print("My Move: ", c, self.possibleMovesForGravity[c]+1)
                    #print("Poss Move: ", self.possibleMovesForGravity)
                    return Move(c, self.possibleMovesForGravity[c]+1)

                # when got out of loop
                c = randint(0,self.col-1)
                while(not self.objB.is_valid_move(c, self.possibleMovesForGravity[c])):
                    c = randint(0,self.col-1)

                self.objB.make_my_move(c, self.possibleMovesForGravity[c], 1)
                self.possibleMovesForGravity[c] -= 1

                return Move(c, self.possibleMovesForGravity[c]+1)

                
