#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

#Updated by Vijay Ganesh Panchapakesan 
#UTA_ID:1001861777

from copy import deepcopy as deepcopy
import random
import math

Infinity=(math.inf)
Negative_Infinity=-Infinity
nodeUtilityValue={}

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1 #1 for player and 2 for computer
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.depth=0
        random.seed()

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print(' ------------------------')
        for i in range(6):
           print(' |')
           for j in range(7):
               print('%d '%int(self.gameBoard[i][j])),
           print('| ')
        print(' ------------------------')

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1
                
    def ifPiecePresent(self, column,nextmove):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = nextmove
                    self.pieceCount += 1
                    return 1

    # The AI section. Currently plays randomly.
    def aiPlay(self):
        randColumn = self.minmax(int(self.depth))
        print(randColumn)# implement Minimax algorithm here
        result = self.playPiece(randColumn)
        if not result:
            print("Not able to play")
        else:
            print('\n\nmove %d: Player %d, column %d\n' % (self.pieceCount, self.currentTurn, randColumn+1))
            if self.currentTurn == 1:
                self.currentTurn = 2
            elif self.currentTurn == 2:
                self.currentTurn = 1
    #This function is the heart of aiPlay function as it returns the next
    #column to be played            
    def minmax(self,depth):
        current_gameboard=deepcopy(self.gameBoard)
        listofvals=[]
        for i in range(7):
            if(self.playPiece(i)!=None):
                if(self.checkPieceCount()==42 and self.depth==0):#Copy the Currentstate and return i
                    self.gameboard=deepcopy(current_gameboard)
                    return i
                else:
                    value=self.generate_MinValue(self.gameBoard,Negative_Infinity,Infinity,depth-1)
                    nodeUtilityValue[i]=value
                    self.gameBoard=deepcopy(current_gameboard)
        for utilitykey in nodeUtilityValue:
            listofvals.append(nodeUtilityValue[utilitykey])
        max_value=max(listofvals)
                
        #To find the col in which max value is present and ret that column
        for i in range(7):
            if( i in nodeUtilityValue):
                if(nodeUtilityValue[i]==max_value):
                    return i
    
    #This function gets the min value of the Min player i.e the computer
    #by means of a evaluation function
    def generate_MinValue(self,currentGameBoard,alpha,beta,depth):
        #We would get the deep copy of the current gameboard to get the deepest node
        children=[]
        value=Infinity#For min player the value should be assigned to maximum
        parentNode=deepcopy(currentGameBoard)
        if(self.currentTurn==1):
            nextTurn=self.currentTurn+1;
        elif(self.currentTurn==2):
            nextTurn=self.currentTurn-1
        
        for i in range(7):
            currentNode=self.ifPiecePresent(i,nextTurn)
            if(currentNode!=None):
                children.append(self.gameBoard)
                self.gameBoard=deepcopy(parentNode)
        if(len(children)>0 and depth>0):
            for child in children:
                self.gameBoard=deepcopy(child)
                #it is the min value of its value max value of the previous max subtree
                value=min(value,self.generate_MaxValue(child,alpha,beta,depth-1))
                
                if value<=alpha:
                    return value
                else:
                    beta=min(value,beta)
            return value
        else:
            self.countScore()
            return self.board_eval(self.gameBoard)
        
        
        
        
    #This function gets the max value of the Max player i.e the User
    #by means of a evaluation function
    def generate_MaxValue(self,currentGameBoard,alpha,beta,depth):
        #We would get the deep copy of the current gameboard to get the deepest node
        children=[]
        value=Negative_Infinity#For min player the value should be assigned to maximum
        parentNode=deepcopy(currentGameBoard)
        
        for i in range(7):
            currentNode=self.playPiece(i)
            if(currentNode!=None):
                children.append(self.gameBoard)
                self.gameBoard=deepcopy(parentNode)
        if(len(children)>0 and depth>0):
            for child in children:
                self.gameBoard=deepcopy(child)
                #it is the max value of its value max value of the previous min subtree
                value=max(value,self.generate_MinValue(child,alpha,beta,depth-1))
                
                if value>=beta:
                    return value
                else:
                    alpha=max(value,alpha)
            return value           
        else:
            self.countScore()
            return self.board_eval(self.gameBoard)
        
    #As in chess we are finding the number of 2's(vertically,hoziontally and diagonaly)
    #Likewise we are finding for number of 3's and number of 4's
    #which ever is greater and depending upon it returning the utility value
    def board_eval(self,state):
        if(self.currentTurn==1):
            nextTurn=self.currentTurn+1;
        elif(self.currentTurn==2):
            nextTurn=self.currentTurn-1
        
        player_twos=self.Twostreak(self.gameBoard,self.currentTurn)
        player_threes=self.Threestreak(self.gameBoard,self.currentTurn)
        player_fours=self.Fourstreak(self.gameBoard,self.currentTurn)
        opponent_twos=self.Twostreak(self.gameBoard,nextTurn)
        opponent_threes=self.Threestreak(self.gameBoard,nextTurn)
        opponent_fours=self.Fourstreak(self.gameBoard,nextTurn)
        
        #I am giving 20 points for each 4's and 10pts for each 3's and 5pt for each 2's
        return ((player_fours*20 + player_threes*10+player_twos*5)
                -(opponent_fours*20 + opponent_threes*10+opponent_twos*5))
    
    #Checks how many conscecutive 2's are there vertically,
    #horizontally and dioganally
    def Twostreak(self,state,currentturn):
        count=0;
        for i in range(6):
            for j in range(7):
                if(state[i][j]==currentturn):
                    count+=self.TwoHorizontalStreak(i,j,currentturn,state)
                    count+=self.TwoVerticalStreak(i,j,currentturn,state)
                    count+=self.TwoDiagonalStreak(i,j,currentturn,state)
        return count
    
    #Checks how many conscecutive 3's are there vertically,
    #horizontally and dioganally
    def Threestreak(self,state,currentturn):
        count=0;
        for i in range(6):
            for j in range(7):
                if(state[i][j]==currentturn):
                    count+=self.ThreeHorizontalStreak(i,j,currentturn,state)
                    count+=self.ThreeVerticalStreak(i,j,currentturn,state)
                    count+=self.ThreeDiagonalStreak(i,j,currentturn,state)
        return count
    
    #Checks how many conscecutive 4's are there vertically,
    #horizontally and dioganally
    def Fourstreak(self,state,currentturn):
        count=0;
        for i in range(6):
            for j in range(7):
                if(state[i][j]==currentturn):
                    count+=self.FourHorizontalStreak(i,j,currentturn,state)
                    count+=self.FourVerticalStreak(i,j,currentturn,state)
                    count+=self.FourDiagonalStreak(i,j,currentturn,state)
        return count
    
    #Checks how many conscecutive 2's are there hORIZONTALLY
    def TwoHorizontalStreak(self,rowno,colno,turn,state):
        sum=2
        count=0
        for j in range(colno,7):
            if(state[rowno][j]==turn):
                count+=1
            else:
                break
        if(count>=sum):
            return 1
        else:
            return 0
        
    
    #Checks how many conscecutive 3's are there hORIZONTALLY    
    def ThreeHorizontalStreak(self,rowno,colno,turn,state):
        sum=3
        count=0
        for j in range(colno,7):
            if(state[rowno][j]==turn):
                count+=1
            else:
                break
        if(count>=sum):
            return 1
        else:
            return 0
    
    #Checks how many conscecutive 4's are there hORIZONTALLY
    def FourHorizontalStreak(self,rowno,colno,turn,state):
        sum=4
        count=0
        for j in range(colno,7):
            if(state[rowno][j]==turn):
                count+=1
            else:
                break
        if(count>=sum):
            return 1
        else:
            return 0
    
    #Checks how many conscecutive 2's are there Vertically
    def TwoVerticalStreak(self,rowno,colno,turn,state):
        sum=2
        count=0
        for i in range(rowno,6):
            if(state[i][colno]==turn):
                count+=1
            else:
                break
        if(count>=sum):
            return 1
        else:
            return 0
    #Checks how many conscecutive 3's are there Vertically
    def ThreeVerticalStreak(self,rowno,colno,turn,state):
        sum=3
        count=0
        for i in range(rowno,6):
            if(state[i][colno]==turn):
                count+=1
            else:
                break
        if(count>=sum):
            return 1
        else:
            return 0
    
    #Checks how many conscecutive 4's are there Vertically
    def FourVerticalStreak(self,rowno,colno,turn,state):
        sum=4
        count=0
        for i in range(rowno,6):
            if(state[i][colno]==turn):
                count+=1
            else:
                break
        if(count>=sum):
            return 1
        else:
            return 0
    
    #counts the no of consecutive 2' or 3's or 4's in the negative diagonal
    def FindNegativeDiagonal(self,rowno,colno,turn,state,sum):
        count=0    
        for i in range(rowno,-1,-1):
            if colno>6:
                break
            elif(state[i][colno]==turn):
                count+=1
            else:
                break
        if count>=sum:
            return 1
        else:
            return 0
    
    #counts the no of consecutive 2' or 3's or 4's in the both +ve and
    #-ve diagonals
    def TwoDiagonalStreak(self,rowno,colno,turn,state):
        sum=2
        count=0
        j=colno
        final=0
        for i in range(rowno,6):
            if j>6:
                break
            elif(state[i][j]==turn):
                count+=1
            else:
                break
        if count>=sum:
            final+=1
        final=final+self.FindNegativeDiagonal(rowno,j+1,turn,state,sum)
        return final
    
    def ThreeDiagonalStreak(self,rowno,colno,turn,state):
        sum=3
        count=0
        j=colno
        final=0
        for i in range(rowno,6):
            if j>6:
                break
            elif(state[i][j]==turn):
                count+=1
            else:
                break
        if count>=sum:
            final+=1
        final+=self.FindNegativeDiagonal(rowno,j+1,turn,state,sum)
        return final
    
    def FourDiagonalStreak(self,rowno,colno,turn,state):
        sum=4
        count=0
        j=colno
        final=0
        for i in range(rowno,6):
            if j>6:
                break
            elif(state[i][j]==turn):
                count+=1
            else:
                break
        if count>=sum:
            final+=1
        final+=self.FindNegativeDiagonal(rowno,j+1,turn,state,sum)
        return final
    
    

        
    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1

