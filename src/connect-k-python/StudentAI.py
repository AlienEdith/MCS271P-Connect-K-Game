from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():
    col = 0
    row = 0
    k = 0
    g = 0
    possibleMoves = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]
    adj_to_opponent_move = set()

    def __init__(self,col,row,k,g):
        self.g = g
        self.col = col
        self.row = row
        self.k = k
        self.objB = Board(col,row,k,g)

    def check_opponent_win(self, tempCol, tempRow):
        # if the move is invalid then check next possible position
        if(not self.objB.is_valid_move(tempCol, tempRow, True)):
            return False;

        # if the move is possible temporarily make the move
        self.objB.make_my_move(tempCol, tempRow, 2)

        # check if 2 wins by this move then we move to that position
        if(self.objB.is_win() == 2):
            self.objB.revert_my_move(tempCol, tempRow)
            return True

        # we remove the temporary move from the board
        self.objB.revert_my_move(tempCol, tempRow)
        return False

    def add_adj_cells(self, move):
        # check all the adjecent cells of the move
        for pm in possibleMoves:

            # if cell is valid i.e. empty then add it to list

            # also calculate the heuristic of how good is this place based on 
            # h(c) = number of adjecent cells with 1 + number of adjecent cells with 2

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
                self.add_adj_cells(move)
            
                #self.objB.my_show_board();        
            
                # check around this move if it makes it win for 2
                for r in range(0, self.row):
                    for c in range(0, self.col):

                        # if this move makes player2 to win then move to that position
                        if(self.check_opponent_win(c, r)):
                            self.objB.make_my_move(c, r, 1)
                            return Move(c,r)

                # else if no such move makes player2 to win then make a random move
                newCol = randint(0,self.col-1)
                newRow = randint(0,self.row-1)

                while(not self.objB.is_valid_move(newCol, newRow, True)):
                    newCol = randint(0,self.col-1)
                    newRow = randint(0,self.row-1)
            
            self.objB.make_my_move(newCol, newRow, 1)
            
            return Move(newCol,newRow)
        else:
            return Move(randint(0,self.col-1),0)
