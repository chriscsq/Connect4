############################################
############################################
############################################
########### GROUP 66 - CONNECT 4 ###########
### Chris, Jaskaran, Gary, Pratik, David ###
############################################
############################################
############################################

#The objective of the game is for player or computer to try to get 4 in a row
#You can get win by achieving 4 colors in a row horizontally, vertically, or diagonally
#There will be a tie if the grid is filled and nobody wins.
#Win or lose, press space to start a new game
#Good luck!


#Calls main, main calls the introduction screen then makes a new screen which will make the grid.
#After the grid is done it will chose who will go first, either A.I. or User then the real game beings.
#The grid will listen to when the User clicks then it will go to the clickmove method and first it will check
#if the User clicked within the grid, after the User click it will have coordinates and that will be the parameters
#for the clickmove method. The process after that will convert the coordinates from 1 to 7 then after that it will
#call a new method that will slice the gameList in that certain index and will replace the E with a P.

############################################
############### INSTRUCTIONS ###############
############################################

#PLAYER COLOR IS IN USER_COLOR
#COMPUTER COLOR IS IN COMP_COLORB
#Randomly generates who goes first
#If CPU goes first, most optimal move will always be middle column
#From there on, player will click on the grid to make their turn
#After that, the computer will make their turn on the grid
#Each turn will result in an updated gameList
#Connect 4 in a row horizontally, diagonally, or vertically to win
#If you're looking to save the game, press 's' any time to save the gameList
#To load, press 'l' and click on the screen once to load the game
#When user or computer wins, a message will show up on the screen
#To exit the game, click on screen or press space bar.

###############################################
############### DOCUMENTED BUGS ###############
###############################################

#Computer prioritizes blocking 3 over winning 4
#If player spam clicks very fast on the screen, proper dots wont show up
#Computer does a very good job at blocking vertical 3's

import turtle
import random
import time

################################################
############### GLOBAL CONSTANTS ###############
################################################

#This will control the color of the computers and users dots, respectively.
COMP_COLOR = 'lightblue'
USER_COLOR = 'red'
#This will control the color in which the computers dot will flash.
FLASH_COLOR = 'black'
#Controls the background color of the introduction screen.
INTRODUCTION_COLOR = 'lightblue'
#controls the background color of the grid.
GRID_COLOR = 'lightpink'
#Size of each token/dot.
DOT_SIZE = 60
#Global constants that control the time certain in game messages show up for.
HALF_SEC_TIMER = 0.5
ONE_SEC_TIMER = 1
ONE_HALF_SEC_TIMER = 1.5

#General constants to do with the dimensions of the board.
ROW = 6
COLUMN = 7
#Number of total cells in the board.
NUM_CELLS = 42
#This will make the computer's dot flash for a certain length of time,
#corrisponding to the number of flash_alternations.
FLASH_ALTERNATIONS = 25
#The X coordinate for the center of each cell.
#Not dynamic because it needs to be in a list
CELL_CENTER = {'1': -210, '2': -140, '3': -70, '4': 0, '5': 70, '6': 140, '7': 210}
#Cell size.
CELL = 70
#Y coordinate of the center of the bottom row.
BOTTOM_ROW_CENTER = -160
#The number of tokens that need to be connected in order to win.
WIN_DOT = 4
#Constants or if you have two or three in a row respectively.
TWO_IN_ROW = 2
THREE_IN_ROW = 3
#Best possible first move if comp goes first.
OPTIMAL_FIRST_MOVE = 4
#heuristic values we assigned for how many dots we have in a row.
TWO_ROW_SCORE = 3
THREE_ROW_SCORE = 100
#This value is used to describe if you can place a dot that will win you the game.
#Also if you can block the opponent.
WINVALUE = 1000

#These constants are here just to simplify the code.
#P, C, E is for the gameList,
#Which stand for player, comp, and empty respectively.
P = "P"
C = "C"
E = 'E'
#F is used to also simplify the code,
#It is used to describe a column that is full.
F = 'F'

#These constants are used to keep track of who's turn it is.
PMOVE = 1
CMOVE = 0
PMOVEFIRST = 3
#Controls the speed in which the grid is being created at.
GRID_SPEED = 20
#The number of lines needed to create the cell box.
CELL_BOX = 4
#The x-coordinate to describe the very left of the grid.
LEFT_GRID = -245
#The y-coordinate to describe the very bottom of the grid.
BOTTOM_GRID = -195

#The grid's boundary for the left or right side of the board.
#It will be negative if used to describe the left boundary.
GRID_X_BOUNDARY = 245
GRID_TOP_BOUNDARY = 225
GRID_BOTTOM_BOUNDARY = -195

#Position for all in-game messages.
INTERFACE_X_POS = -240
CENTER_INTERFACE_X_POS = -150
INTERFACE_Y_POS = -250

#Constats used for font size and font type.
LARGE_SIZE = 35
MEDIUM_SIZE = 20
SMALL_SIZE = 15
FONT = "Times New Roman"
#X-coordinate for the introduction text.
LEFT_ALIGN = -240

##########################################################
############### CREATE THE CELL BOUNDARIES ###############
##########################################################
def leftBound():
    #Empty list
    leftMargin = []
    #multiplier is used to keep track of which cell number you are getting the bounds for.
    for multiplier in range(COLUMN):
        margins = LEFT_GRID + (multiplier * CELL)
        #appending to the empty list to create a list with all the left bounds,
        # after it goes through all of the loops.
        leftMargin.append(margins)
    return leftMargin

#Creates the constants for the right bound of each cell.
def rightBound(leftbound):
    #Empty list
    rightMargin = []
    #margins are used the left bound of each cell.
    for margins in leftbound:
        #You add cell size to get from left bound side to the right bound size.
        rightCell = int(margins) + CELL
        #appending to the empty list to create a list with all the right bounds,
        # after it goes through all of the loops.
        rightMargin.append(rightCell)
    return rightMargin
#Saving each side bound as a global constant. 
LEFTBOUND = leftBound()
RIGHTBOUND = rightBound(LEFTBOUND)

######################################################
############### GLOBALS - NOT CONSTANT ###############
######################################################

 
#Max Pieces per row
#THIS IS THE CLASS USED FOR OUR PIECES
#WE HAVE SET A BOUNDARY SO THE VALUE DOES NOT GO BEYOND 6, WHICH IS THE MAXIMUM ROW
#PARAMATER IS THE DICTIONARY
#CALLED Pieces(dict) WITH THE DICTIONARY 
MAXPIECES = 6
class Pieces(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, min(value, MAXPIECES))
#Used to determine the number of tokens in each column.
pieces = Pieces({'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0})
turn = 0
numMoves  = 0
gameList = [[E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E]]


def main():
    intro()
    grid()
    initialClick()
    clickSetup()

def intro():
    #Welcome turtle, dark orange background, welcome w/ rules
    welcome = turtle.Turtle()
    intro = turtle.Screen()
    intro.bgcolor(INTRODUCTION_COLOR)
    welcome.ht()
    welcome.up()

    #Header
    welcome.goto(LEFT_ALIGN, 100)
    welcome.write ("Welcome to Connect 4!",
                   font = (FONT, LARGE_SIZE, "bold"))

    #Rules
    welcome.goto(LEFT_ALIGN, 70)
    welcome.write("Rules:",
                  font = (FONT, MEDIUM_SIZE))
    welcome.goto(LEFT_ALIGN, 40)
    welcome.write("Players take turn to slide a token to the first available row in clicked column",
                  font = (FONT, SMALL_SIZE))
    welcome.goto(LEFT_ALIGN, 20)
    welcome.write("Goal is to get 4 in a row horizontally, vertically, or diagonally.",
                  font = (FONT, SMALL_SIZE))
    welcome.goto(LEFT_ALIGN, 0)
    welcome.write("If there are no more moves and nobody wins, the game is a tie",
                  font = (FONT, SMALL_SIZE))
    welcome.goto(LEFT_ALIGN, -20)
    welcome.write("Click anywhere on the screen to start the game.",
                  font = (FONT, SMALL_SIZE))
    welcome.goto(LEFT_ALIGN, -40)
    welcome.write("Press space to exit when you're done!",
                  font = (FONT, SMALL_SIZE))
    welcome.goto(LEFT_ALIGN, -60)
    welcome.write("Press 's' to save your game!",
                  font = (FONT, SMALL_SIZE))
    welcome.goto(LEFT_ALIGN, -80)
    welcome.write("Press 'l' and click on the screen to load. Good luck!",
                  font = (FONT, SMALL_SIZE))
    intro.exitonclick()

def grid():
    #Setting up our pretty screen with a light blue background.
    pretty = turtle.Screen()
    pretty.bgcolor(GRID_COLOR)
    #Setting up the turtle that draws the grid lines.
    grid = turtle.Turtle()
    grid.ht()
    speed = turtle.Screen()
    #Increases the speed of the grid.
    speed.tracer(GRID_SPEED)
    #Loops every time a single row is drawn.
    for row in range(ROW):
        #Sets up the position for the next cell to be created.
        for col in range(COLUMN):
            grid.up()
            grid.setpos((col * CELL) + LEFT_GRID, (row * CELL) + BOTTOM_GRID)
            grid.pd()
            #This is where each individual cell is drawn.
            for side in range(CELL_BOX):
                grid.fd(CELL)
                grid.lt(90)

def clickSetup():
    #Sets up for any onkey commands and the click.
    clickGrid = turtle.Screen()
    clickGrid.bgcolor(GRID_COLOR)
    #Onclick command which will be executed once a click has gone through.
    #Calls the function clickMove once the player clicks.
    clickGrid.onclick(clickMove)
    #Onkey commands.
    clickGrid.onkey(clickGrid.bye, "space")
    clickGrid.onkey(save,"s")
    clickGrid.onkey(load,"l")
    #Listen is required in order to use any onkey commands.
    #It waits and listens until one of onkey command are used,
    #which will than call the corresponding function.
    clickGrid.listen()
    #Creats a infinite loop which basically always listens for a click.
    clickGrid.mainloop()

def clickMove(x, y):
    global numMoves, gameList, turn
    interface = turtle.Turtle()
    interface.ht()
    #Checks to see if the click is within the y-axis of the grid.
    if y >= GRID_BOTTOM_BOUNDARY and y <= GRID_TOP_BOUNDARY:

        #Checks to see if the click is within the x-axis of the grid.
        if x >= - GRID_X_BOUNDARY and x <= GRID_X_BOUNDARY:
            #Calls the function gameOver to check if any player has won.
            winState = gameOver()

            #Checks if there are any empty cells and no one has won the game.
            if numMoves != NUM_CELLS and winState == False:

                #Checks to see if the computer had the previous turn and no one has won the game.
                if turn == CMOVE and winState == False:
                    #Updates gameList and also calls playerMove.
                    #Executes player turn.
                    gameList = playerMove(x)
                    #Updates winState to check if the player has won.
                    winState = gameOver()
                    if winState == True:
                        interface.up()
                        #The only constant that is in not global. 
                        #This will keep the user wins message centered.
                        CENTER_OFF = 35
                        interface.goto(CENTER_INTERFACE_X_POS + CENTER_OFF, INTERFACE_Y_POS)
                        interface.down()
                        interface.write("USER WINS!!!",
                                        font = (FONT, LARGE_SIZE))

                #Checks to see if the player and the previous turn and no one has won the game.
                if turn == PMOVE and not winState:
                    #Choses a random number between 1-7,
                    #which will be where the cpu will play their token.
              
                    cpu = str(makeDecision())
                    #Updates gameList and also calls move.
                    #Executes the computers turn.
                    gameList = compMove(cpu)
                    #Updates winState to check if the computer has won.
                    winState = gameOver()
                    if winState == True:
                        interface.up()
                        interface.goto(CENTER_INTERFACE_X_POS, INTERFACE_Y_POS)
                        interface.down()
                        interface.write("COMPUTER WINS!!!",
                                        font = (FONT, LARGE_SIZE))

                #Checks to see if someone has won this will be executed.
                if winState == True:
                    #Allows user to exit the screen on click.
                    exit = turtle.Screen()
                    exit.exitonclick()
            else:
                #If all 42 cells are occupied this will be executed.
                #This prints a message in the game screen,
                # telling the user it is a stalemate.
                interface.goto(INTERFACE_X_POS, INTERFACE_Y_POS)
                interface.write("The game has resulted in a stalemate.",
                                font = (FONT, LARGE_SIZE))
                #Allows user to exit the screen on click.
                exit = turtle.Screen()
                exit.exitonclick()
        else:
            #This combined with the next else statement,
            #print an error message if the user has clicked outside the grid,
            #in either direction.
            #This will be executed if the user clicks outside of the grid in the x-axis.
            #Prints an error message in the game screen,
            # telling the user to click inside the grid.
            interface.goto(INTERFACE_X_POS, INTERFACE_Y_POS)
            interface.write("Please click inside the grid.",
                            font = (FONT, MEDIUM_SIZE))
            #time.sleep is used to keep the text there for one and a half seconds,
            # it does this by pausing for the one and a half seconds.
            time.sleep(ONE_SEC_TIMER)
            #This will than clear the turtle.
            interface.clear()
    else:
        #Prints an error message in the game screen,
        # telling the user to click inside the grid,
        #only if the user clicks above or below the board.
        interface.goto(INTERFACE_X_POS, INTERFACE_Y_POS)
        interface.write("Please click inside the grid.",
                        font = (FONT, MEDIUM_SIZE))
        #time.sleep is used to keep the text there for one and a half seconds,
        # it does this by pausing for the one and a half seconds.
        time.sleep(ONE_SEC_TIMER)
        #This will than clear the turtle.
        interface.clear()

############################################
############### PLAYER PIECE ###############
############################################


def playerMove(column):
    global gameList
    index = 0
    #for each left-bound cell
    for cell in range(len(LEFTBOUND)):
        #Parameters for clicking - It must be within the grid
        if column >= LEFTBOUND[cell] and column <= RIGHTBOUND[cell]:
            #Column will be cell converted into a string, +1
            #This is because the range starts from 0 and dictionary starts at 1
            index = cell
            playerDot(str(index + 1))
            break

    if turn == PMOVE:
        #Passes new gameList to updateState
        gameList = updateState(index + 1)
    return gameList

def updateState(column):
    global gameList
    col = int(column)
    #Generates the list that will be returned
    #Takes the index given by move and updates the gameList to reflect recent move.
    gameList[(pieces[str(col)] -1 )][col -1] = P
    return gameList

def playerDot(column):
    global pieces, gameList, turn, numMoves
    interface = turtle.Turtle()
    interface.ht()
    pDot = turtle.Turtle()
    pDot.ht()
    pDot.up()
    #Pieces * Cell length for Y value
    #Conditions for pDot to move are pieces in each column must be less than the rows
    #CPU also must have moved beforehand
    #if conditions are met, pieces[column] and numMoves incremented by 1, turn reflects player
    if pieces[column] < ROW and turn == CMOVE:
        pDot.goto(CELL_CENTER[column], BOTTOM_ROW_CENTER + (pieces[column] * CELL))
        pDot.dot(DOT_SIZE, USER_COLOR)
        pieces[column] += 1
        turn = PMOVE
        numMoves += 1
    else:
        #Sets up the location in which he interface turtle has to go to.
        interface.goto(INTERFACE_X_POS, INTERFACE_Y_POS)
        #Prints an error message in the game screen,
        # telling the user to click in a column that isn't full.
        interface.write("Please chose a column that is not filled.",
                        font = (FONT, MEDIUM_SIZE))
        time.sleep(ONE_SEC_TIMER)
        interface.clear()



def initialClick():
    global gameList, turn, numMoves
    #Randomizes if computer will go first or player first
    #If firstMove == 1, computer goes first.
    firstMove = random.randrange(1, PMOVEFIRST)
    if firstMove == 1:
        turn = PMOVE
        cpu = str(OPTIMAL_FIRST_MOVE)
        gameList = compMove(cpu)
        numMoves += 1



##############################################
############### WIN CONDITIONS ###############
##############################################

#Gameover will change horiCheck, vertiCheck, diagPos or diagNeg
#They will change if any of the checks return True
#If any of them do, gameOver will return True
#Return False if else.
def gameOver():
    horiCheck = False
    vertiCheck = False
    diagPos = False
    diagNeg = False
    if hCheck(WIN_DOT, P, gameList) or hCheck(WIN_DOT, C, gameList):
        horiCheck = True
    if vCheck(WIN_DOT, P, gameList) or vCheck(WIN_DOT, C, gameList):
        vertiCheck = True
    if dCheckPos(WIN_DOT, P, gameList) or dCheckPos(WIN_DOT, C, gameList):
        diagPos = True
    if dCheckNeg(WIN_DOT, P, gameList) or dCheckNeg(WIN_DOT, C, gameList):
        diagNeg = True

    return horiCheck or vertiCheck or diagNeg or diagPos

#Calls check with the row offset of 0 and column offset of 1.
#Will check for both a win in P and win for C
def hCheck(windot, color, checkState):
    if check(0, 1, windot, color, checkState):
        return True
    else:
        return False
#Calls check with the row offset of 1 and the column offset of 0.
#Will check for both a win in P and win for C
def vCheck(windot, color, checkState):
    if check(1, 0, windot, color, checkState):
        return True
    else:
        return False

#Diagonal check for positive slope
def dCheckPos(windot, color, checkState):
    if check(1, 1, windot, color, checkState):
        return True
    else:
        return False

#Diagonal check for negative slope
def dCheckNeg(windot, color, checkState):
    if check(-1, 1, windot, color, checkState):
        return True
    else:
        return False


def check(rowOff, colOff, winDot, color, checkList):

    #Checks the position of every cell in the game
    for cellOrigin in range(NUM_CELLS):
        count = 0
        rowOrigin = cellOrigin // COLUMN
        colOrigin = cellOrigin % COLUMN

        #Checks the position in each sublist
        for positionInCheck in range(ROW):
            #Boundaries for the check
            if rowOrigin >= 0 and colOrigin >= 0 and rowOrigin <= (ROW - 1) and colOrigin <= (COLUMN - 1):
                consecDot = checkList[rowOrigin][colOrigin]
            else:
                consecDot = E

            #Checks for consecutive colors and see if they reach winDot
            #Returns true if >=
            #If not, it resets to 0

            if consecDot == color:
                count += 1
                if count >= winDot:
                    return True
            else:
                count = 0

            #The best part of our check. 
            #This is row or column offset
            #Dynamic for vertical, horizontal, and diagonal checks
            rowOrigin = rowOrigin + rowOff
            colOrigin = colOrigin + colOff

    return False


###########################################
############### COMPUTER AI ###############
###########################################

#PURE LIST
#Function will create a pure gameList for use in further functions

def pureList():
    newList = []
    for sublist in gameList:
        newSub = []
        for index in sublist:
            newSub.append(index)
        newList.append(newSub)
    return newList

#Function will create a list of ROW LOCATION of first E in available columns
#Calls FINDHEURISTIC with the purelist NEWLIST.
def getPosition(freeCol):
    newList = pureList()
    piecesList = []
    heuristicList = []
    for column in range(1, len(pieces) + 1):
        piecesList.append(pieces[str(column)])

    for row in piecesList:
        if piecesList[row] <= (ROW - 1):
            sublist = piecesList[row]
            indexInSublist = freeCol[row]

            if newList[sublist][indexInSublist] == E:
                #Changes the first E to a C
                newList[sublist][indexInSublist] = C
                #Calculates heuristic numbers (desired numbers based on checks)
                heuristic = findHeuristic(newList)
                #Appends it to a list based on column index
                heuristicList.append(heuristic)
                #Changes the C back to an E and tests next column
                newList[sublist][indexInSublist] = E
    return heuristicList

#Same as previous function but it will attempt to look for an P instead of an E
#This way, we can check to see if P is about to win and then that setups the heuristic to block
def blockSetup(freeCol):
    gameListCopy = pureList()
    piecesList = []
    heuristicList = []
    for column in range(1, len(pieces) + 1):
        piecesList.append(pieces[str(column)])

    for row in piecesList:
        if piecesList[row] <= (ROW - 1):
            sublist = piecesList[row]
            indexInSublist = freeCol[row]
            if gameListCopy[sublist][indexInSublist] == E:
                gameListCopy[sublist][indexInSublist] = P
                heuristic = findHeuristic(gameListCopy)
                heuristicList.append(heuristic)
                gameListCopy[sublist][indexInSublist] = E
    return heuristicList

#LOOKS AT HEURISTIC VALUES
#Returns index of highest value
def makeDecision():
    combinedHeuristicValList = []
    freeCol = possibleMoves()
    heuristicValList = getPosition(freeCol)
    secondHeuristicValList = blockSetup(freeCol)
    maxValue = 0
    secondMaxVal = 0

    for index in heuristicValList:
        if index >= maxValue:
            maxValue = index

    for element in secondHeuristicValList:
        if element >= secondMaxVal:
            secondMaxVal = element

    for position in range(len(heuristicValList)):
        posInList_1 = heuristicValList[position]
        posInList_2 = secondHeuristicValList[position]
        combinedHeuristicValList.append(posInList_1 + posInList_2)

    maxValue += secondMaxVal
    #If there are multiple indexs with the same value, shuffle index
    #This makes it so the game doesnt lean towards the left
    randomizeNum = shuffleList(combinedHeuristicValList, maxValue)

    return randomizeNum + 1


#Act of shuffling the index
#Takes the first index of the shuffled index
def shuffleList(heuristicList, maxValue):
    shuffleIndex = []
    validMove = possibleMoves()
    randomNum = random.randrange(COLUMN)
    for index in range(len(heuristicList)):
        if index in validMove:
            indexValue = heuristicList[index]
            if indexValue == maxValue:
                shuffleIndex.append(index)
    random.shuffle(shuffleIndex)
    if len(shuffleIndex) == 0:
        return randomNum
    else:
        firstShuffeled = shuffleIndex[0]
        return firstShuffeled



def findHeuristic(newList):
    #GREEDY

    heuristic = 0
    #Heuristic for computer horizontals
    if hCheck(WIN_DOT, C, newList):
        heuristic += (WINVALUE * 2)
    elif hCheck(THREE_IN_ROW, C, newList):
        heuristic += THREE_ROW_SCORE
    elif hCheck(TWO_IN_ROW, C, newList):
        heuristic += TWO_ROW_SCORE
    #heuristic for computer verticals
    if vCheck(WIN_DOT, C, newList):
        heuristic += (WINVALUE * 2)
    elif vCheck(THREE_IN_ROW, C, newList):
        heuristic += THREE_ROW_SCORE
    elif vCheck(TWO_IN_ROW, C, newList):
        heuristic += TWO_ROW_SCORE
    #heuristic for computer diagonals]
    if dCheckPos(WIN_DOT, C, newList):
        heuristic += (WINVALUE * 2)
    elif dCheckPos(THREE_IN_ROW, C, newList):
        heuristic += THREE_ROW_SCORE
    elif dCheckPos(TWO_IN_ROW, C, newList):
        heuristic += TWO_ROW_SCORE

    if dCheckNeg(WIN_DOT, C, newList):
        heuristic += (WINVALUE * 2)
    elif dCheckNeg(THREE_IN_ROW, C, newList):
        heuristic += THREE_ROW_SCORE
    elif dCheckNeg(TWO_IN_ROW, C, newList):
        heuristic += TWO_ROW_SCORE
        
    return heuristic

def findBlockHeuristic(newList):
    #BLOCK
    #HIGH HEURISTIC VALUE == HIGH PRIORITY
    heuristic = 0
    if hCheck(WIN_DOT, P, newList):
        heuristic += WINVALUE
    if vCheck(WIN_DOT, P, newList):
        heuristic += WINVALUE
    if dCheckNeg(WIN_DOT, P, newList):
        heuristic += WINVALUE
    if dCheckPos(WIN_DOT, P, newList):
        heuristic += WINVALUE

    return heuristic

def possibleMoves():
    #The possible moves that are left in each column.
    #Index of moves are appended to a list
    #Full moves are shown as a F
    freeCol = []
    for indexInSublist in range(COLUMN):
        if gameList[ROW - 1][indexInSublist] == E:
            freeCol.append(indexInSublist)
        else:
            freeCol.append(F)
    return freeCol

##################################################
############### COMPUTER FUNCTIONS ###############
##################################################

def compDot(column):
    global turn, numMoves
    interface = turtle.Turtle()
    interface.ht()
    #Computer turtle
    cDot = turtle.Turtle()
    cDot.ht()
    cDot.up()

    #It will only create a piece if these conditionals are met.
    #That means player must have moved first and also,
    #the specific position in the gameList must be empty and the column cannot be filled
    #It will the change turn to reflect
    #Pieces[column] and numMoves get incremented.
    if pieces[column] < ROW and turn == PMOVE:
        cDot.goto(CELL_CENTER[column], BOTTOM_ROW_CENTER + (pieces[column] * CELL))
        for flash in range(FLASH_ALTERNATIONS):
            cDot.dot(DOT_SIZE, FLASH_COLOR)
            cDot.dot(DOT_SIZE, COMP_COLOR)


        turn = CMOVE
        pieces[column] += 1
        numMoves += 1
    else:
        interface.goto(INTERFACE_X_POS, INTERFACE_Y_POS)
        interface.write("Comp tried to make an illegal move, please click again.",
                        font = (FONT, MEDIUM_SIZE))
        time.sleep(ONE_SEC_TIMER)
        interface.clear()


def compMove(column):
    global gameList
    compDot(column)
    #If turn == Computer, update the gameList
    if turn == CMOVE:
        gameList = cUpdateState(column)
    return gameList

def cUpdateState(column):
    global gameList
    col = int(column)
    #Replaces the proper index that was passed from comp -> cMove -> cUpdate to be C.
    #Reflects in the gameList
    gameList[(pieces[str(col)] -1 )][col -1] = C
    return gameList

###################################################
################## SAVE AND LOAD ##################
###################################################

#Save function will take our gamelist and copy it over into a txt file.
#What happens is we loop through the gameList
#For every sublist, we strip the spaces and add a new line at the end
#Therefore, it will be saved in a file like so:
# EEEEEEE
# EEEEEEE
# EEEEEEE
# EEEEEEE
# EEEEEEE
# EEEEEEE

def save():
    interface = turtle.Turtle()
    interface.ht()
    interface.up()
    interface.goto(INTERFACE_X_POS, INTERFACE_Y_POS)
    interface.down()
    interface.write("The game has been successfully saved.",
                        font = (FONT, MEDIUM_SIZE))
    time.sleep(ONE_HALF_SEC_TIMER)
    interface.clear()
    with open("tempGameState.txt", "w") as f:
        for row in gameList:
            rowStr = ''
            for cell in row:
                rowStr += cell + ''
            f.write(rowStr + '\n')

def load():
    global pieces
    interface = turtle.Turtle()
    interface.ht()
    interface.up()
    interface.goto(INTERFACE_X_POS, INTERFACE_Y_POS)
    interface.down()
    interface.write("Please click on the screen to open your loaded game!",
                        font = (FONT, MEDIUM_SIZE))
    time.sleep(ONE_HALF_SEC_TIMER)
    interface.clear()
    savedFile = open("tempGameState.txt","r")
    reading = savedFile.read()
    reading = reading.replace('\n',"")
    reading = reading.strip("")

    # method is to close the old grid, making a new grid
    def closeScreen():
        global turn
        #resets turn
        turn = 0
        closewn = turtle.Screen()
        closewn.exitonclick()
        grid()

    # reset the dictionary
    # params: the dictionary and the value we want it to reset to
    # return the original dictionary
    def newValue(dict,reset_to):
        global numMoves
        #resets numMoves
        numMoves = 0
        for keys in dict:
            # look at the whatever keys is and makes it = 0
            dict[keys] = reset_to
        return dict


    # convert to file into a list
    #param: the saved file
    # return the saved file as a nested list
    def to2dList(saveFile):
        converter = []
        row = []
        # loops it 42 times
        for cell in range(len(saveFile)):
            # if row has 7 letters inside the list
            # it will go to the converter
            if len(row) == COLUMN:
                converter.append(row)
                row = [saveFile[cell]]
            # keeps adding the letters to row
            else:
                row.append(saveFile[cell])
        converter.append(row)
        return converter


    # method to find where player and comp moves where made on the board
    # param: the saved filed as a nested list
    # returns: nothing
    def reDot(savedList):
        global gameList
        gameList = savedList
        #look at the sublist
        for sublist in range(len(savedList)):
            #looks at the sublist index
            for sublistIndex in range(len(savedList[sublist])):
                letter = savedList[sublist][sublistIndex]
                # if  there is a "P" then it will take that index
                # and go to the savedplayer function and stamp it on that col
                if letter == P:
                    # add a 1 because the index can equal zero and our col doesn't
                    # start from 0
                    savedPlayer(sublistIndex + 1)
                # if  there is a "C" then it will take that index
                # and go to the comp function and stamp it on that col
                if letter == C:
                    # add a 1 because the index can equal zero and our col doesn't
                    # start from 0
                    savedComp(sublistIndex + 1)


    # re-dots all the player dots from the saved file
    def savedPlayer(column):
        global pieces, turn, numMoves
        pDot = turtle.Turtle()
        pDot.ht()
        pDot.up()
        column = str(column)
        #Pieces * Cell length for Y value
        #listIndex = column
        pDot.goto(CELL_CENTER[column], BOTTOM_ROW_CENTER + (pieces[column] * CELL))
        pDot.dot(DOT_SIZE, USER_COLOR)
        pieces[column] += 1
        turn = PMOVE
        numMoves += 1

    # re-dot all the comp dots from the saved file
    def savedComp(column):
        global pieces, turn, numMoves
        cDot = turtle.Turtle()
        cDot.ht()
        cDot.up()
        column = str(column)
        cDot.goto(CELL_CENTER[column], BOTTOM_ROW_CENTER + (pieces[column] * CELL))
        cDot.dot(DOT_SIZE, COMP_COLOR)
        turn = CMOVE
        pieces[column] += 1
        numMoves += 1

    closeScreen()
    pieces = newValue(pieces, 0)
    ToList = to2dList(reading)
    reDot(ToList)
    turn = 0
    clickSetup()

main()
