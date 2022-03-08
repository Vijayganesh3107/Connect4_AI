Name:Vijay Ganesh Panchapakesan
Uta_Id:1001861777
Language used:Python

							Assignment-1 Part-2
----------------------------------------------------------------------------------------------------


Command structure:

One-move mode:python maxconnect4.py one-move [input_file] [output_file] [depth]
Interactive mode:python maxconnect4.py interactive [input_file] [computer-next/human-next] [depth]

----------------------------------------------------------------------------------------------------

Folder Structure:

1)maxconnect4.py-Which is the main file to run which uses MaxConnect4Game class and implements interactive mode and 
  one-move mode based on the command given by the user in the command line
2)Input1.txt-It is the sample input given as an input to the maxconnect4.py and based on which gameboard is created
  The operations are done to this Input gameboard.
3)Input2.txt-It is another sample input file for testing.
4)Player1.txt-Each move of the user is being updated in the Player1.txt file for interactive mode
5)Player2.txt-Each move of the Computer is being updated in the Player2.txt file for interactive mode
6)Output.txt-It is the output file after the one move made from the one-move mode.
7)MaxConnect4Game.py-It is a class which has many member functions.This class impleements the heart i.e the
  Depth Limited MinMax Algorithm with alpha-beta pruning.

----------------------------------------------------------------------------------------------------

Main Functions in MaxConnect4Game.py

1)board_eval:This function takes currentboard as an argument this function first checks the number of 2's 3's
 and 4's vertically,horizontally and diagonally(both +ve and -ve diagonal) for both user and the computer.With
 this information an eval function is created by adding the no of consecutive 2's the no of consecutive 3's and
 the no of consecutive 4's.Each has been given a weight i.e for 4's a weight of 20 is given, for 3's a weight
 of 10 is given and for 2's a weight of 5 is given and returning the differnce betwwen the values of the user
 and the computer.This Eval function is used to find the utility values for the teminal nodes.
2)generate_MinValue:This function gets the min value of the Min player i.e the computer by means of a evaluation
 function
3)generate_MaxValue:This function gets the max value of the Max player i.e the user,by means of a evaluation
 function 
----------------------------------------------------------------------------------------------------

How to run the code:

Before Running please install Python 3.X into your sysytem and perfom the below steps.

Keep all the files of AI_Project_Part_2 in the same folder and run the command prompt in the place
where all the files are present and run the command in the followiung format:

For Interactive mode:
python maxconnect4.py interactive [input_file] [computer-next/human-next] [depth]

eg:-python .\maxconnect4.py interactive Input1.txt human-next 4

For One-move mode:
python maxconnect4.py one-move [input_file] [output_file] [depth]
eg:-python .\maxconnect4.py one-move Input1.txt output.txt 8

----------------------------------------------------------------------------------------------------
DEPTH VS RUNTIME :[One-Move mode]

DepthVsRuntime.xlsx excel sheet has the depth and corresponding runtime values. 
Runtime is calculated for the corresponding depth till time reaches 1 minute.

