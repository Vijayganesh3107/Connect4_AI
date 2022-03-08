#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
import time
from MaxConnect4Game import *

def oneMoveGame(currentGame):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print('BOARD FULL\n\nGame Over!\n')
        sys.exit(0)

    currentGame.aiPlay() # Make a move (only random is implemented)

    print('Game state after move:')
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()


def interactiveGame(currentGame,player):
    currentGame.printGameBoard()
    if(player.lower()=="human-next"):
        currentGame.checkPieceCount()
        while(currentGame.pieceCount!=42):
            col=int(input("Enter the column you want to put your coin in:"))
            
            if(col>7 or col<=0):
                print("Please enter a valid column from 1-7")
                continue
            if(currentGame.playPiece(col-1)):
                # print("Player: Moved a red coin to the column"+str(col))
                currentGame.printGameBoard()
                currentGame.gameFile=open("Player1.txt","w")
                currentGame.printGameBoardToFile()
                currentGame.gameFile.close()
                currentGame.checkPieceCount()
                if(currentGame.pieceCount==42):
                    print("Sorry Game over no more moves left")
                    currentGame.countScore()
                    print("Player1: "+str(currentGame.player1Score)+" Player2: "+str(currentGame.player2Score))
                    break
                else:
                    currentGame.currentTurn=currentGame.currentTurn+1 if currentGame.currentTurn==1 else currentGame.currentTurn-1 ;
                    currentGame.aiPlay()
                    currentGame.countScore()
                    print("Player1: "+str(currentGame.player1Score)+" Player2: "+str(currentGame.player2Score))
                    currentGame.printGameBoard()
                    currentGame.gameFile=open("Player2.txt","w")
                    currentGame.printGameBoardToFile()
                    currentGame.gameFile.close()
            else:
                print("No such move possible as column"+str(col)+" is filled")
                currentGame.checkPieceCount()
                continue
    else:
        currentGame.aiPlay()
        currentGame.countScore()
        currentGame.printGameBoard()
        print("Player1: "+str(currentGame.player1Score)+" Player2: "+str(currentGame.player2Score))
        currentGame.gameFile=open("Player2.txt","w")
        currentGame.printGameBoardToFile()
        currentGame.gameFile.close()
        interactiveGame(currentGame,"Human-next")
    currentGame.checkPieceCount()
    
    currentGame.countScore()
    print("Player1: "+str(currentGame.player1Score)+" Player2: "+str(currentGame.player2Score))
    print((f'Player1 Won the game with a score {currentGame.player1Score}',f"Player2 Won the game with {currentGame.player2Score}")[currentGame.player2Score>currentGame.player1Score])
    
            
            
        
    #sys.exit('Interactive mode is currently not implemented')


def main(argv):
    # argv=argv[1].split(","); For testing purpose
    # print(argv)
    # Make sure we have enough command-line arguments
    if len(sys.argv) != 5:
        print('Four command-line arguments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % sys.argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % sys.argv[0])
        sys.exit(2)

    game_mode,inFile=sys.argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game
    

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    print(currentGame.gameBoard)
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print ('\nMaxConnect-4 game\n')
    print ('Game state before move:')
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    currentGame.depth=4
    if game_mode == 'interactive':
        interactiveGame(currentGame,sys.argv[3].lower()) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        start=time.time();
        currentGame.depth=int(sys.argv[4])
        outFile = sys.argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        
        
        oneMoveGame(currentGame) # Be sure to pass any other arguments from the command line you might need.
        endtime=time.time()
        print(f"Time = {endtime-start}s")

if __name__ == '__main__':
    main(sys.argv)



