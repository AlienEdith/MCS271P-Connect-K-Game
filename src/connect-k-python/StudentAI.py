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
    possibleMovesForGravity = []

    def __init__(self,col,row,k,g):
        self.g = g
        self.col = col
        self.row = row
        self.k = k
        self.objB = Board(col,row,k,g)
        for c in range(0, self.col):
            self.possibleMovesForGravity.insert(c, row-1)

    def check_opponent_win(self, tempCol, tempRow):        
        # if the move is invalid then check next possible position
        if(not self.objB.is_valid_move(tempCol, tempRow, True)):
            return False

        # if the move is possible temporarily make the move
        self.objB.make_my_move(tempCol, tempRow, 2)

        # check if 2 wins by this move then we move to that position
        if(self.objB.is_win() == 2):
            self.objB.revert_my_move(tempCol, tempRow)
            return True

        # we remove the temporary move from the board
        self.objB.revert_my_move(tempCol, tempRow)
        return False

    def get_move(self,move):
        if self.g == 0:
            if(move.col == -1 and move.row == -1):
                # take middle element so that increases connect on many sides
                newCol = math.ceil((self.col-1)/2)
                newRow = math.ceil((self.row-1)/2)
            
            else:
                #set recent move of player 2 on board
                self.objB.make_my_move(move.col, move.row, 2)
            
                #self.objB.my_show_board();        
                newCol = -1
                newRow = -1

                # check around this move if it makes it win for 2
                for r in range(0, self.row):
                    for c in range(0, self.col):

                        if(self.check_opponent_win(c, r)):
                            self.objB.make_my_move(c, r, 1)
                            return Move(c,r)

                # else make a random move
                newCol = randint(0,self.col-1)
                newRow = randint(0,self.row-1)

                while(not self.objB.is_valid_move(newCol, newRow, True)):
                    newCol = randint(0,self.col-1)
                    newRow = randint(0,self.row-1)
               
            self.objB.make_my_move(newCol, newRow, 1)
            
            return Move(newCol,newRow)

        elif self.g == 1:
            if(move.col == -1 and move.row == -1):
                # take middle element so that increases connect on many sides
                newCol = math.ceil((self.col-1)/2)
            else:
                print("Opponent Move: ", move.col, self.possibleMovesForGravity[move.col])
                print("Opponent Move: ", move.col, move.row)

                self.objB.make_my_move(move.col, self.possibleMovesForGravity[move.col], 2)
                print("Make Opponent Move")
                self.possibleMovesForGravity[move.col] -= 1
                print(move.col, self.possibleMovesForGravity[move.col])
                
                newCol = -1

                for c in range(0, self.col):
                    if(self.possibleMovesForGravity[c] < 0):
                        continue
                    
                    print(c, self.possibleMovesForGravity[c])
                    print(self.check_opponent_win(c, self.possibleMovesForGravity[c]))

                    if(self.check_opponent_win(c, self.possibleMovesForGravity[c])):
                        self.objB.make_my_move(c, self.possibleMovesForGravity[c], 1)
                        self.possibleMovesForGravity[c] -= 1
                        print("My Move: ", c, self.possibleMovesForGravity[c]+1)
                        return Move(c, self.possibleMovesForGravity[c]+1)
                
                newCol = randint(0,self.col-1)
                while(not self.objB.is_valid_move(newCol, self.possibleMovesForGravity[newCol], True)):
                    newCol = randint(0,self.col-1)

            self.objB.make_my_move(newCol, self.possibleMovesForGravity[newCol], 1)
            self.possibleMovesForGravity[newCol] -= 1
            print("My Move: ", newCol, self.possibleMovesForGravity[newCol]+1)
            return Move(newCol, self.possibleMovesForGravity[newCol]+1)
                
        return Move(randint(0,self.col-1),0)
