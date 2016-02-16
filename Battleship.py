#
# Battleship
#
# Austin Chen
#
# This module contains the code for the Human player board and the landing screen.
#

from graphics import *
import math
import random
import time
#list of column possibilities
#the x is there in place of 10, because of the method of searching for coordinates
column = ["1","2","3","4","5","6","7","8","9","X"]
#list of row possibilities
row = ["A","B","C","D","E","F","G","H", "I", "J"]
shipresults = ["afloat","afloat","afloat","afloat","afloat"]
#blank lists for later
AIpositions = []
shotlist = []
results = []
flagnum = 0
#blank lists for the ships
UserPatrol = ["",""]
UserSub = ["","",""]
UserDestroy = ["","",""]
UserBattle = ["","","",""]
UserCarrier = ["","","","",""]


#
# Human player GUI + AI Update Screen
#   input: none
#

def userGUI(diff):

    # Creating User's board
    userWin = GraphWin("Player Board", 600, 650)
    userWin.setCoords(-50,600,550,-50)
    userWin.setBackground(color_rgb(16,58,200))

    # Drawing vertical gridlines
    x = 0
    y = 0
    for i in range(11):
        gridLine = Line(Point(x,y), Point(x, y+500))
        gridLine.draw(userWin)
        x = x + 50

    # Drawing horizontal gridlines
    x = 0
    y = 0
    for i in range(11):
        gridLine = Line(Point(x,y), Point(x+500, y))
        gridLine.draw(userWin)
        y = y + 50

    # Drawing horizontal coordinate markings
    x = 25
    y = -12.5
    z = 0
    columnLabel = ["1","2","3","4","5","6","7","8","9","10"]
    for i in range(10):
        columnDraw = Text(Point(x,y),columnLabel[z])
        columnDraw.setSize(16)
        columnDraw.setFace('courier')
        columnDraw.draw(userWin)
        x = x + 50
        z = z + 1
        
    # Drawing vertical coordinate markings
    x = -12.5
    y = 25
    z = 0
    rowLabel = ["A", "B", "C", "D", "E", "F", "G", "H", "I","J"]
    for i in range(10):
        rowDraw = Text(Point(x,y),rowLabel[z])
        rowDraw.setFace('courier')
        rowDraw.setSize(16)
        rowDraw.draw(userWin)
        y = y + 50
        z = z + 1

    # Bottom boxes in Player Board
    boxColor = color_rgb(250,165,45)
    
    # Box that houses up arrow
    upBox = Rectangle(Point(438,542),Point(462,518))
    upBox.setFill(boxColor)
    upBox.setWidth(1.2)
    upBox.draw(userWin)

    # Up arrow
    upArrow = Line(Point(450,538),Point(450,521))
    upArrow.setArrow('last')
    upArrow.draw(userWin)

    # Box that houses left arrow
    leftBox = Rectangle(Point(413,567),Point(437,543))
    leftBox.setFill(boxColor)
    leftBox.setWidth(1.2)
    leftBox.draw(userWin)

    # Left arrow
    leftArrow = Line(Point(433,555),Point(416,555))
    leftArrow.setArrow('last')
    leftArrow.draw(userWin)

    # Box that houses down arrow
    downBox = Rectangle(Point(438,568),Point(462,592))
    downBox.setFill(boxColor)
    downBox.setWidth(1.2)
    downBox.draw(userWin)
    
    # Down arrow
    downArrow = Line(Point(450,572),Point(450,589))
    downArrow.setArrow('last')
    downArrow.draw(userWin)
    
    # Box that houses right arrow
    rightBox = Rectangle(Point(463,567),Point(487,543))
    rightBox.setFill(boxColor)
    rightBox.setWidth(1.2)
    rightBox.draw(userWin)
    
    # Right arrow
    rightArrow = Line(Point(467,555),Point(484,555))
    rightArrow.setArrow('last')
    rightArrow.draw(userWin)
    
    # Box that houses "lock in" text
    lockBox = Rectangle(Point(200,575),Point(300,525))
    lockBox.setFill(boxColor)
    lockBox.draw(userWin)
    
    # "Lock in" text
    lockBoxText = Text(Point(250,550),"LOCK IN")
    lockBoxText.setFace('courier')
    lockBoxText.setSize(18)
    lockBoxText.setStyle('bold')
    lockBoxText.draw(userWin)

    # Box that houses "Rotate" text
    rotateBox = Rectangle(Point(18,575),Point(82,525))
    rotateBox.setFill(boxColor)
    rotateBox.draw(userWin)
    
    # "Rotate" text
    rotateText = Text(Point(50,550), "ROTATE")
    rotateText.setFace('courier')
    rotateText.draw(userWin)

    # Confirmation Symbols
    # The way this works is that the dimensions of each icon can be expressed in terms of xZ. This effectively makes a grid system in which
    # the window will graph points and trace it as a polygon.
    # Therefore, the xZ can be modified to increase or decrease the size of these icons.
    xZ = 12

    # X
    xPic = Polygon(Point(141,550-xZ),Point(141+xZ,550-(2*xZ)),Point(141+(2*xZ),550-xZ),Point(141+xZ,550),Point(141+(2*xZ),550+xZ),Point(141+xZ,550+(2*xZ)),Point(141,550+xZ),Point(141-xZ,550+(2*xZ)),Point(141-(2*xZ), 550+xZ),Point(141-xZ,550),Point(141-(2*xZ),550-xZ),Point(141-xZ,550-(2*xZ)))
    xPic.setWidth(2)
    xPic.setFill('red')
    
    # Check
    cPic = Polygon(Point(350,550),Point(350+(2.5*xZ),550-(2.5*xZ)),Point(350+(3.5*xZ),550-(1.5*xZ)),Point(350,550+(2*xZ)),Point(350-(2*xZ),550),Point(350-xZ,550-xZ))
    cPic.setWidth(2)
    cPic.setFill('green')

    # Used for indexing and knowing where the boats are placed (in terms of coordinates
    rowCoord = ["error","A","B","C","D","E","F","G","H","I","J"]
    columnCoord = ["error","1","2","3","4","5","6","7","8","9","10"]
    
    # spaceTaken will be filled in as ships are locked in.
    spaceTaken = []

    # Carrier placement

    carrierPlaced = False

    # Default coordinates that the carrier will appear at
    x = 225
    y = 275

    # The z value will determine the orientation of the ship (vertical or horizontal)
    # As you will see later, 1 is added to z each time the user flips orientations.
    # This method effectively oscillates the value of z between even and odd numbers.
    # Therefore, if the z value is 0, the orientation is vertical. If the z value is 1,
    # the orientation is horizontal.
    z = 0

    while carrierPlaced == False:
        userWin.update()

        # Choosing which orientation to draw
        if (z % 2) == 0:
            carrier = Image(Point(x,y),"carrierVert.gif")
            carrier.draw(userWin)
        elif (z % 2) == 1:
            carrier = Image(Point(x,y),"carrierHoriz.gif")
            carrier.draw(userWin)

        # Gathering user clicks each loop
        click = userWin.getMouse()
        clickX = click.getX()
        clickY = click.getY()

        # Gathering image center each loop
        carrierX = carrier.getAnchor().getX()
        carrierY = carrier.getAnchor().getY()
        

        # For the rest of this loop, there are 7 options.
        # 1. Lock in
        # 2. Rotate
        # 3. Move up
        # 4. Move down
        # 5. Move right
        # 6. Move left
        # 7. User clicked elsewhere and screen just updates
        
        # Locking in
        if clickX >= 200 and clickX <= 300 and clickY >= 525 and clickY <= 575:
            # countUp is the coordinate point that is furthest from the anchorpoint.
            countUp = -100
            # Depends on vertical or horizontal orientation
            if (z % 2) == 0:
                # Loops 5 times to gather all 5 cells the ship occupies
                for i in range(5):
                    points = rowCoord[int(((carrierY+countUp)/50) + .5)] + columnCoord[int((carrierX/50) + .5)]
                    # spaceTaken is the list in which every cell is stored as a string.
                    spaceTaken.append(points)
                    countUp = countUp + 50
                # Visual confirmation
                cPic.draw(userWin)
                time.sleep(1)
                cPic.undraw()
                carrierPlaced = True
                
            countUp = -100
            if (z % 2) == 1:
                for i in range(5):
                    points = rowCoord[int((carrierY/50) + .5)] + columnCoord[int(((carrierX+countUp)/50) + .5)]
                    spaceTaken.append(points)
                    countUp = countUp + 50
                cPic.draw(userWin)
                time.sleep(1)
                cPic.undraw()
                carrierPlaced = True

        # Rotating ship
        elif clickX >= 18 and clickX <= 82 and clickY >= 525 and clickY <= 575:
            if (z % 2) == 0:
                if carrierX < 125 or carrierX > 375:
                    carrier.undraw()
                else:
                    # Oscillating z that was mentioned earlier
                    carrier.undraw()
                    z = z + 1
            elif (z % 2) == 1:
                if carrierY < 125 or carrierY > 375:
                    carrier.undraw()
                else:
                    carrier.undraw()
                    z = z + 1

        # Moving ship up
        elif clickX >= 438 and clickX <= 462 and clickY >= 518 and clickY <= 542:
            if (z % 2) == 0:
                if carrierY < 175:
                    carrier.undraw()
                else:
                    carrier.undraw()
                    y = y - 50
            elif (z % 2) == 1:
                if carrierY < 75:
                    carrier.undraw()
                else:
                    carrier.undraw()
                    y = y - 50
                
        # Moving ship left    
        elif clickX >= 413 and clickX <= 437 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if carrierX < 75:
                    carrier.undraw()
                else:
                    carrier.undraw()
                    x = x - 50
            elif (z % 2) == 1:
                if carrierX < 175:
                    carrier.undraw()
                else:
                    carrier.undraw()
                    x = x - 50

        # Moving ship down
        elif clickX >= 438 and clickX <= 462 and clickY >= 568 and clickY <= 592:
            if (z % 2) == 0:
                if carrierY > 325:
                    carrier.undraw()
                else:
                    carrier.undraw()
                    y = y + 50
            elif (z % 2) == 1:
                if carrierY > 425:
                    carrier.undraw()
                else:
                    carrier.undraw()
                    y = y + 50

        # Moving ship right
        elif clickX >= 463 and clickX <= 487 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if carrierX > 425:
                    carrier.undraw()
                else:
                    carrier.undraw()
                    x = x + 50
            elif (z % 2) == 1:
                if carrierX > 325:
                    carrier.undraw()
                else:
                    carrier.undraw()
                    x = x + 50

        # User clicked somewhere else
        else:
            carrier.undraw()


    # Battleship placement

    battleshipPlaced = False

    x = 225
    y = 300
    z = 0

    battleshipSpace = []

    # checkLog is a new list introduced after the carrier has been placed. The reason this list did not exist
    # before is because the user is able to place the carrier anywhere (no other ships can interfere)
    # checkLog will be explained further later.
    checkLog = []
    
    
    while battleshipPlaced == False:
        
        userWin.update()

        if (z % 2) == 0:
            battleship = Image(Point(x,y),"battleshipVert.gif")
            battleship.draw(userWin)
        elif (z % 2) == 1:
            battleship = Image(Point(x,y),"battleshipHoriz.gif")
            battleship.draw(userWin)

        click = userWin.getMouse()
        clickX = click.getX()
        clickY = click.getY()

        battleshipX = battleship.getAnchor().getX()
        battleshipY = battleship.getAnchor().getY()

        # Locking in ship position
        if clickX >= 200 and clickX <= 300 and clickY >= 525 and clickY <= 575:

            # Every time the "Lock in" button is pressed, the battleshipSpace and checkLog lists are cleared.
            # This is to ensure that the data collected is only for the ships current placement and not any
            # past placements.
            battleshipSpace = []
            checkLog = []

            # Countup is -50 to be multiplied by 4. 200 is range of 4 space battleship.
            countUp = -50

            if (z % 2) == 0:
                for i in range(4):
                    points = rowCoord[int(((battleshipY+countUp-25)/50) + .5)] + columnCoord[int((battleshipX/50) + .5)]
                    # Every time the loop iterates, each point will be appended to list battleshipSpace.
                    # battleshipSpace should end up with 4 coordinate cells by the end of 4 iterations.
                    battleshipSpace.append(points)
                    countUp = countUp + 50
                # For loop here is used to compare each value in current battleship orientation to coordinates in list spaceTaken
                for i in battleshipSpace:
                    # i in spaceTaken outputs a true or false condition. If i is found in spaceTaken, the condition is true. Otherwise, it's false.
                    if i in spaceTaken:
                        # At this point, checkLog should still be empty.
                        # When a battleship's current coordinate span overlaps with any space that has been taken,
                        # checkLog will append string "Taken"
                        checkLog.append("Taken")
                    else:
                        # If no matches are found, checkLog appends "We chillin".
                        checkLog.append("We chillin'")

                # After, if the code finds any "Taken" strings in checkLog, the "locking in" process will fail
                # and the user will see a graphical rejection.
                if "Taken" in checkLog:
                    xPic.draw(userWin)
                    time.sleep(.65)
                    xPic.undraw()
                    battleship.undraw()

                # If the checkLog is filled with all "We chillin'", there are no overlaps between ships.
                # Thus, the locking in will be successful. The non-overlapping coordinates will be added
                # to the master "spaceTaken" list of occupied cells.
                else:
                    for i in battleshipSpace:
                        spaceTaken.append(i)
                    cPic.draw(userWin)
                    time.sleep(1)
                    cPic.undraw()
                    # battleshipPlaced will be switched to true which will break the while loop.
                    battleshipPlaced = True
            
            elif (z % 2) == 1:
                for i in range(4):
                    points = rowCoord[int((battleshipY/50) + .5)] + columnCoord[int(((battleshipX+countUp-25)/50) + .5)]
                    battleshipSpace.append(points)
                    countUp = countUp + 50
                for i in battleshipSpace:
                    if i in spaceTaken:
                        checkLog.append("Taken")
                    else:
                        checkLog.append("We chillin'")
                if "Taken" in checkLog:
                    xPic.draw(userWin)
                    time.sleep(.65)
                    xPic.undraw()
                    battleship.undraw()
                else:
                    for i in battleshipSpace:
                        spaceTaken.append(i)
                    cPic.draw(userWin)
                    time.sleep(1)
                    cPic.undraw()
                    battleshipPlaced = True

        # Rotating ship
        elif clickX >= 18 and clickX <= 82 and clickY >= 525 and clickY <= 575:
            if (z % 2) == 0:
                if battleshipX < 75 or battleshipX > 400:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    y = y - 25
                    x = x + 25
                    z = z + 1
            elif (z % 2) == 1:
                if battleshipY < 75 or battleshipY > 400:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    y = y + 25
                    x = x - 25
                    z = z + 1

        # Moving ship up
        elif clickX >= 438 and clickX <= 462 and clickY >= 518 and clickY <= 542:
            if (z % 2) == 0:
                if battleshipY < 125:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    y = y - 50
            elif (z % 2) == 1:
                if battleshipY < 50:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    y = y - 50
                
        # Moving ship left    
        elif clickX >= 413 and clickX <= 437 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if battleshipX < 75:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    x = x - 50
            elif (z % 2) == 1:
                if battleshipX < 150:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    x = x - 50

        # Moving ship down
        elif clickX >= 438 and clickX <= 462 and clickY >= 568 and clickY <= 592:
            if (z % 2) == 0:
                if battleshipY > 375:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    y = y + 50
            elif (z % 2) == 1:
                if battleshipY > 425:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    y = y + 50

        # Moving ship right
        elif clickX >= 463 and clickX <= 487 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if battleshipX > 425:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    x = x + 50
            elif (z % 2) == 1:
                if battleshipX > 350:
                    battleship.undraw()
                else:
                    battleship.undraw()
                    x = x + 50

        # User clicked somewhere else
        else:
            battleship.undraw()


    # Destroyer placement

    destroyerPlaced = False

    x = 225
    y = 275
    z = 0

    destroyerSpace = []
    checkLog = []

    while destroyerPlaced == False:
        userWin.update()
        if (z % 2) == 0:
            destroyer = Image(Point(x,y),"destroyerVert.gif")
            destroyer.draw(userWin)
        elif (z % 2) == 1:
            destroyer = Image(Point(x,y),"destroyerHoriz.gif")
            destroyer.draw(userWin)

        click = userWin.getMouse()
        clickX = click.getX()
        clickY = click.getY()

        destroyerX = destroyer.getAnchor().getX()
        destroyerY = destroyer.getAnchor().getY()

        # Locking in ship position
        if clickX >= 200 and clickX <= 300 and clickY >= 525 and clickY <= 575:
            
            destroyerSpace = []
            checkLog = []
            countUp = -50
            
            if (z % 2) == 0:
                for i in range(3):
                    points = rowCoord[int(((destroyerY+countUp)/50) + .5)] + columnCoord[int((destroyerX/50) + .5)]
                    destroyerSpace.append(points)
                    countUp = countUp + 50
                for i in destroyerSpace:
                    if i in spaceTaken:
                        checkLog.append("Taken")
                    else:
                        checkLog.append("We chillin'")
                if "Taken" in checkLog:
                    xPic.draw(userWin)
                    time.sleep(.65)
                    xPic.undraw()
                    destroyer.undraw()
                else:
                    for i in destroyerSpace:
                        spaceTaken.append(i)
                    cPic.draw(userWin)
                    time.sleep(1)
                    cPic.undraw()
                    destroyerPlaced = True
            
            elif (z % 2) == 1:
                for i in range(3):
                    points = rowCoord[int((destroyerY/50) + .5)] + columnCoord[int(((destroyerX+countUp)/50) + .5)]
                    destroyerSpace.append(points)
                    countUp = countUp + 50
                for i in destroyerSpace:
                    if i in spaceTaken:
                        checkLog.append("Taken")
                    else:
                        checkLog.append("We chillin'")
                if "Taken" in checkLog:
                    xPic.draw(userWin)
                    time.sleep(.65)
                    xPic.undraw()
                    destroyer.undraw()
                else:
                    for i in destroyerSpace:
                        spaceTaken.append(i)
                    cPic.draw(userWin)
                    time.sleep(1)
                    cPic.undraw()
                    destroyerPlaced = True

        # Rotating ship
        elif clickX >= 18 and clickX <= 82 and clickY >= 525 and clickY <= 575:
            if (z % 2) == 0:
                if destroyerX < 75 or destroyerX > 425:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    z = z + 1
            elif (z % 2) == 1:
                if destroyerY < 75 or destroyerY > 425:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    z = z + 1

        # Moving ship up
        elif clickX >= 438 and clickX <= 462 and clickY >= 518 and clickY <= 542:
            if (z % 2) == 0:
                if destroyerY < 125:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    y = y - 50
            elif (z % 2) == 1:
                if destroyerY < 75:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    y = y - 50
                
        # Moving ship left    
        elif clickX >= 413 and clickX <= 437 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if destroyerX < 75:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    x = x - 50
            elif (z % 2) == 1:
                if destroyerX < 125:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    x = x - 50

        # Moving ship down
        elif clickX >= 438 and clickX <= 462 and clickY >= 568 and clickY <= 592:
            if (z % 2) == 0:
                if destroyerY > 375:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    y = y + 50
            elif (z % 2) == 1:
                if destroyerY > 425:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    y = y + 50

        # Moving ship right
        elif clickX >= 463 and clickX <= 487 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if destroyerX > 425:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    x = x + 50
            elif (z % 2) == 1:
                if destroyerX > 375:
                    destroyer.undraw()
                else:
                    destroyer.undraw()
                    x = x + 50

        # User clicked somewhere else
        else:
            destroyer.undraw()

    # submarine placement

    submarinePlaced = False

    x = 225
    y = 275
    z = 0

    submarineSpace = []
    checkLog = []
    

    while submarinePlaced == False:
        userWin.update()
        if (z % 2) == 0:
            submarine = Image(Point(x,y),"submarineVert.gif")
            submarine.draw(userWin)
        elif (z % 2) == 1:
            submarine = Image(Point(x,y),"submarineHoriz.gif")
            submarine.draw(userWin)

        click = userWin.getMouse()
        clickX = click.getX()
        clickY = click.getY()

        submarineX = submarine.getAnchor().getX()
        submarineY = submarine.getAnchor().getY()

        # Locking in ship position
        if clickX >= 200 and clickX <= 300 and clickY >= 525 and clickY <= 575:
            
            submarineSpace = []
            checkLog = []
            countUp = -50
            
            if (z % 2) == 0:
                for i in range(3):
                    points = rowCoord[int(((submarineY+countUp)/50) + .5)] + columnCoord[int((submarineX/50) + .5)]
                    submarineSpace.append(points)
                    countUp = countUp + 50
                for i in submarineSpace:
                    if i in spaceTaken:
                        checkLog.append("Taken")
                    else:
                        checkLog.append("We chillin'")
                if "Taken" in checkLog:
                    xPic.draw(userWin)
                    time.sleep(.65)
                    xPic.undraw()
                    submarine.undraw()
                else:
                    for i in submarineSpace:
                        spaceTaken.append(i)
                    cPic.draw(userWin)
                    time.sleep(1)
                    cPic.undraw()
                    submarinePlaced = True
            
            elif (z % 2) == 1:
                for i in range(3):
                    points = rowCoord[int((submarineY/50) + .5)] + columnCoord[int(((submarineX+countUp)/50) + .5)]
                    submarineSpace.append(points)
                    countUp = countUp + 50
                for i in submarineSpace:
                    if i in spaceTaken:
                        checkLog.append("Taken")
                    else:
                        checkLog.append("We chillin'")
                if "Taken" in checkLog:
                    xPic.draw(userWin)
                    time.sleep(.65)
                    xPic.undraw()
                    submarine.undraw()
                else:
                    for i in submarineSpace:
                        spaceTaken.append(i)
                    cPic.draw(userWin)
                    time.sleep(1)
                    cPic.undraw()
                    submarinePlaced = True

        # Rotating ship
        elif clickX >= 18 and clickX <= 82 and clickY >= 525 and clickY <= 575:
            if (z % 2) == 0:
                if submarineX < 75 or submarineX > 425:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    z = z + 1
            elif (z % 2) == 1:
                if submarineY < 75 or submarineY > 425:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    z = z + 1

        # Moving ship up
        elif clickX >= 438 and clickX <= 462 and clickY >= 518 and clickY <= 542:
            if (z % 2) == 0:
                if submarineY < 125:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    y = y - 50
            elif (z % 2) == 1:
                if submarineY < 75:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    y = y - 50
                
        # Moving ship left    
        elif clickX >= 413 and clickX <= 437 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if submarineX < 75:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    x = x - 50
            elif (z % 2) == 1:
                if submarineX < 125:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    x = x - 50

        # Moving ship down
        elif clickX >= 438 and clickX <= 462 and clickY >= 568 and clickY <= 592:
            if (z % 2) == 0:
                if submarineY > 375:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    y = y + 50
            elif (z % 2) == 1:
                if submarineY > 425:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    y = y + 50

        # Moving ship right
        elif clickX >= 463 and clickX <= 487 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if submarineX > 425:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    x = x + 50
            elif (z % 2) == 1:
                if submarineX > 375:
                    submarine.undraw()
                else:
                    submarine.undraw()
                    x = x + 50

        # User clicked somewhere else
        else:
            submarine.undraw()

        
    # Patrol boat placement

    patrolPlaced = False

    x = 225
    y = 300
    z = 0

    patrolSpace = []
    checkLog = []

    while patrolPlaced == False:
        userWin.update()
        if (z % 2) == 0:
            patrol = Image(Point(x,y),"patrolVert.gif")
            patrol.draw(userWin)
        elif (z % 2) == 1:
            patrol = Image(Point(x,y),"patrolHoriz.gif")
            patrol.draw(userWin)

        click = userWin.getMouse()
        clickX = click.getX()
        clickY = click.getY()

        patrolX = patrol.getAnchor().getX()
        patrolY = patrol.getAnchor().getY()
        
        # Locking in ship position
        if clickX >= 200 and clickX <= 300 and clickY >= 525 and clickY <= 575:
            patrolSpace = []
            checkLog = []
            countUp = 0
            
            if (z % 2) == 0:
                for i in range(2):
                    points = rowCoord[int(((patrolY+countUp-25)/50) + .5)] + columnCoord[int((patrolX/50) + .5)]
                    patrolSpace.append(points)
                    countUp = countUp + 50
                for i in patrolSpace:
                    if i in spaceTaken:
                        checkLog.append("Taken")
                    else:
                        checkLog.append("We chillin'")
                if "Taken" in checkLog:
                    xPic.draw(userWin)
                    time.sleep(.65)
                    xPic.undraw()
                    patrol.undraw()
                else:
                    for i in patrolSpace:
                        spaceTaken.append(i)
                    cPic.draw(userWin)
                    time.sleep(1)
                    cPic.undraw()
                    patrolPlaced = True
            
            elif (z % 2) == 1:
                for i in range(2):
                    points = rowCoord[int((patrolY/50) + .5)] + columnCoord[int(((patrolX+countUp-25)/50) + .5)]
                    patrolSpace.append(points)
                    countUp = countUp + 50
                for i in patrolSpace:
                    if i in spaceTaken:
                        checkLog.append("Taken")
                    else:
                        checkLog.append("We chillin'")
                if "Taken" in checkLog:
                    xPic.draw(userWin)
                    time.sleep(.65)
                    xPic.undraw()
                    patrol.undraw()
                else:
                    for i in patrolSpace:
                        spaceTaken.append(i)
                    cPic.draw(userWin)
                    time.sleep(1)
                    cPic.undraw()
                    patrolPlaced = True


        # Rotating ship
        elif clickX >= 18 and clickX <= 82 and clickY >= 525 and clickY <= 575:
            if (z % 2) == 0:
                if patrolX < 25 or patrolX > 450:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    y = y - 25
                    x = x + 25
                    z = z + 1
            elif (z % 2) == 1:
                if patrolY < 25 or patrolY > 450:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    y = y + 25
                    x = x - 25
                    z = z + 1

        # Moving ship up
        elif clickX >= 438 and clickX <= 462 and clickY >= 518 and clickY <= 542:
            if (z % 2) == 0:
                if patrolY < 75:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    y = y - 50
            elif (z % 2) == 1:
                if patrolY < 50:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    y = y - 50
                
        # Moving ship left    
        elif clickX >= 413 and clickX <= 437 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if patrolX < 75:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    x = x - 50
            elif (z % 2) == 1:
                if patrolX < 100:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    x = x - 50

        # Moving ship down
        elif clickX >= 438 and clickX <= 462 and clickY >= 568 and clickY <= 592:
            if (z % 2) == 0:
                if patrolY > 425:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    y = y + 50
            elif (z % 2) == 1:
                if patrolY > 425:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    y = y + 50

        # Moving ship right
        elif clickX >= 463 and clickX <= 487 and clickY >= 543 and clickY <= 567:
            if (z % 2) == 0:
                if patrolX > 425:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    x = x + 50
            elif (z % 2) == 1:
                if patrolX > 400:
                    patrol.undraw()
                else:
                    patrol.undraw()
                    x = x + 50

        # User clicked somewhere else
        else:
            patrol.undraw()

    # Once the user has placed the last ship, all the ship movement controls will disappear.
    upBox.undraw()
    upArrow.undraw()
    leftBox.undraw()
    leftArrow.undraw()
    downBox.undraw()
    downArrow.undraw()
    rightBox.undraw()
    rightArrow.undraw()
    lockBox.undraw()
    lockBoxText.undraw()
    rotateBox.undraw()
    rotateText.undraw()
    
    # Then, the program will launch into the side-by-side AI window.
    # The AI window is where the user will guess.
    
    # Drawing the AI window
    aiWin = GraphWin("AI Board", 600, 650)
    aiWin.setCoords(-50,600,550,-50)
    aiWin.setBackground(color_rgb(126,136,144))

    # Drawing horizontal gridlines
    x = 0
    y = 0
    for i in range(11):
        gridLine = Line(Point(x,y), Point(x, y+500))
        gridLine.draw(aiWin)
        x = x + 50

    #Drawing vertical gridlines
    x = 0
    y = 0
    for i in range(11):
        gridLine = Line(Point(x,y), Point(x+500, y))
        gridLine.draw(aiWin)
        y = y + 50

    # Drawing horizontal coordinate markings
    x = 25
    y = -12.5
    z = 0
    columnLabel = ["1","2","3","4","5","6","7","8","9","10"]
    for i in range(10):
        columnDraw = Text(Point(x,y),columnLabel[z])
        columnDraw.setFace('courier')
        columnDraw.setSize(16)
        columnDraw.draw(aiWin)
        x = x + 50
        z = z + 1
        
    # Drawing vertical coordinate markings
    x = -12.5
    y = 25
    z = 0
    rowLabel = ["A", "B", "C", "D", "E", "F", "G", "H", "I","J"]
    for i in range(10):
        rowDraw = Text(Point(x,y),rowLabel[z])
        rowDraw.setFace('courier')
        rowDraw.setSize(16)
        rowDraw.draw(aiWin)
        y = y + 50
        z = z + 1

    # Easy
    #see hard for comments
    #hard follows hits
    #easy is random
    if diff == 0:
        usershotlist = []
        shotlist = []
        flagnum = 0
        (userCarrier,userBattle,userDestroy,userSub,userPatrol) = userPoints(patrol,submarine,destroyer,battleship,carrier)
        (AICarrier, AIBattle, AIDestroy, AISub, AIPatrol) = AIplacement()
        userresults = []
        AIresults = []
        turnnum = 0
        usershipcount = ["afloat","afloat","afloat","afloat","afloat"]
        AIshipcount = ["afloat","afloat","afloat","afloat","afloat"]
        hitcount = 0
        hitlist = []
        victory = -1
        while True:
            (choice,userhom1) = userTurn(AICarrier, AIBattle, AIDestroy, AISub, AIPatrol,usershotlist,aiWin)
            texta = userhom1
            usershotlist = usershotlist+[choice]
            usertext = Text(Point(250,550)," ".join(texta[0]).title())
            usertext.setFace('courier')
            usertext.draw(aiWin)
            usertextprime = ""
            if AIshipcount[0] == "afloat" and check(AIPatrol):
                AIshipcount[0] = "sunk"
                usertextprime = "You have sunk my Patrol Boat."
            if AIshipcount[1] == "afloat" and check(AISub):
                AIshipcount[1] = "sunk"
                usertextprime = "You have sunk my Submarine."
            if AIshipcount[2] == "afloat" and check(AIDestroy):
                AIshipcount[2] = "sunk"
                usertextprime = "You have sunk my Destroyer."
            if AIshipcount[3] == "afloat" and check(AIBattle):
                AIshipcount[3] = "sunk"
                usertextprime = "You have sunk my Battleship."
            if AIshipcount[4] == "afloat" and check(AICarrier):
                AIshipcount[4] = "sunk"
                usertextprime = "You have sunk my Aircraft Carrier."
            if "".join(AIshipcount).count("sunk") == 5:
                victory = 0
                time.sleep(1)
                break
            usertext2 = Text(Point(250,590),usertextprime)
            usertext2.setFace('courier')
            usertext2.setSize(18)
            usertext2.setStyle('bold')
            usertext2.draw(aiWin)
            time.sleep(1)
            usertext.undraw()
            usertext2.undraw()
            #only different line
            (hitcount,hitlist,flagnum,shotlist,AIresults,aihom1) = AIturnEasy(hitcount,hitlist,AIresults,shotlist,flagnum,userCarrier,userBattle,userDestroy,userSub,userPatrol,turnnum,userWin)
            if usershipcount[0] == "afloat":
                if check(userPatrol):
                    usershipcount[0] = "sunk"
                    flagnum = flagnum-1
            if usershipcount[1] == "afloat":
                if check(userSub):
                    usershipcount[1] = "sunk"
                    flagnum = flagnum-1
            if usershipcount[2] == "afloat":
                if check(userDestroy):
                    usershipcount[2] = "sunk"
                    flagnum = flagnum-1
            if usershipcount[3] == "afloat":
                if check(userBattle):
                    usershipcount[3] = "sunk"
                    flagnum = flagnum-1           
            if usershipcount[4] == "afloat":
                if check(userCarrier):
                    usershipcount[4] = "sunk"
                    flagnum = flagnum-1
            if "".join(usershipcount).count("sunk") == 5:
                victory = 1
                time.sleep(1)
                break
            turnnum = turnnum+1        

    # Hard
    elif diff == 1:

        #some blank values
        usershotlist = []
        shotlist = []
        flagnum = 0
        #create the lists the corrospond to each ship
        (userCarrier,userBattle,userDestroy,userSub,userPatrol) = userPoints(patrol,submarine,destroyer,battleship,carrier)
        (AICarrier, AIBattle, AIDestroy, AISub, AIPatrol) = AIplacement()
        #blank lists for latter use
        userresults = []
        AIresults = []
        AIresults2 = []
        #alternating turn numbers that grow with the loop
        turnnum = 0
        #Each player has all ships listed as "afloat" initially
        usershipcount = ["afloat","afloat","afloat","afloat","afloat"]
        AIshipcount = ["afloat","afloat","afloat","afloat","afloat"]
        #basic value for latter use
        hitcount = 0
        hitlist = []
        #initial setting of victory to not allow for an error
        victory = -1
        #while loop is where the game is played and breaks when victory is met
        while True:
            (choice,userhom1) = userTurn(AICarrier, AIBattle, AIDestroy, AISub, AIPatrol,usershotlist,aiWin)
            texta = userhom1
            usershotlist = usershotlist+[choice]
            usertext = Text(Point(250,550)," ".join(texta[0]).title())
            usertext.setFace('courier')
            usertext.draw(aiWin)
            usertextprime = ""
            #checks to see if a ship is sunk and changes the status
            if AIshipcount[0] == "afloat" and check(AIPatrol):
                AIshipcount[0] = "sunk"
                usertextprime = "You have sunk my Patrol Boat."
            if AIshipcount[1] == "afloat" and check(AISub):
                AIshipcount[1] = "sunk"
                usertextprime = "You have sunk my Submarine."
            if AIshipcount[2] == "afloat" and check(AIDestroy):
                AIshipcount[2] = "sunk"
                usertextprime = "You have sunk my Destroyer."
            if AIshipcount[3] == "afloat" and check(AIBattle):
                AIshipcount[3] = "sunk"
                usertextprime = "You have sunk my Battleship."
            if AIshipcount[4] == "afloat" and check(AICarrier):
                AIshipcount[4] = "sunk"
                usertextprime = "You have sunk my Aircraft Carrier."
            #victory conditions happen when all of one side's ships are sunk
            if "".join(AIshipcount).count("sunk") == 5:
                victory = 0
                break
            #Draws the user text to gain feedback from the AI
            usertext2 = Text(Point(250,570),usertextprime)
            usertext2.setFace('courier')
            usertext2.setSize(18)
            usertext2.setStyle('bold')
            usertext2.draw(aiWin)
            time.sleep(1)
            usertext.undraw()
            usertext2.undraw()
            #performs the AI's turn and retrives the appropriate values
            (hitcount,hitlist,flagnum,shotlist,AIresults,AIresults2,aihom1) = AIturn(hitcount,hitlist,AIresults,AIresults2,shotlist,flagnum,userCarrier,userBattle,userDestroy,userSub,userPatrol,turnnum,userWin)
            for i in range(len(AIresults)):
                AIresults2 = AIresults2+[AIresults[i]]
            #checks to see if a ship is sunk and changes the status
            if usershipcount[0] == "afloat":
                if check(userPatrol):
                    usershipcount[0] = "sunk"
                    flagnum = flagnum-2
            if usershipcount[1] == "afloat":
                if check(userSub):
                    usershipcount[1] = "sunk"
                    flagnum = flagnum-3
            if usershipcount[2] == "afloat":
                if check(userDestroy):
                    usershipcount[2] = "sunk"
                    flagnum = flagnum-3
            if usershipcount[3] == "afloat":
                if check(userBattle):
                    usershipcount[3] = "sunk"
                    flagnum = flagnum-4         
            if usershipcount[4] == "afloat":
                if check(userCarrier):
                    usershipcount[4] = "sunk"
                    flagnum = flagnum-5
            #victory conditions happen when all of one side's ships are sunk
            if "".join(usershipcount).count("sunk") == 5:
                victory = 1
                break
            #variable to keep track of turn num
            turnnum = turnnum+1
    #closes window
    aiWin.close()
    userWin.close()

    # In order to loop back and repeat gameplay or end
    if endscreen(victory) == 0:
        main()
    elif endscreen(victory) == 1:
        print("Done")
        
#
#input:ships as shapes in graphics
#output: the points of the ships
#
def userPoints(patrol,submarine,destroyer,battleship,carrier):
    #determines anchorpoint of the boat
    patrolp = patrol.getAnchor()
    #finds if horizontal or vertical bsed on the width of each ship
    if patrol.getWidth() > patrol.getHeight():
        xlist = ["",""]
        patrolpx = patrolp.getX()-25
        for i in range(2):
            xlist[i] = patrolpx +50*i
        patrolpy = patrolp.getY()
        ylist = [patrolpy, patrolpy]
        #creats list acording ly
        for i in range(2):
            UserPatrol[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    #same thing for other orinentations.
    else:
        ylist = ["",""]
        patrolpy = patrolp.getY()-25
        for i in range(2):
            ylist[i] = patrolpy +50*i
        patrolpx = patrolp.getX()
        xlist = [patrolpx, patrolpx]
        for i in range(2):
            UserPatrol[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    submarinep = submarine.getAnchor()
    if submarine.getWidth() > submarine.getHeight():
        xlist = ["","",""]
        submarinepx = submarinep.getX()-50
        for i in range(3):
            xlist[i] = submarinepx +50*i
        submarinepy = submarinep.getY()
        ylist = [submarinepy, submarinepy, submarinepy]
        for i in range(3):
            UserSub[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    else:
        ylist = ["","",""]
        submarinepy = submarinep.getY()-50
        for i in range(3):
            ylist[i] = submarinepy +50*i
        submarinepx = submarinep.getX()
        xlist = [submarinepx, submarinepx, submarinepx]
        for i in range(3):
            UserSub[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    destroyerp = destroyer.getAnchor()
    if destroyer.getWidth() > destroyer.getHeight():
        xlist = ["","",""]
        destroyerpx = destroyerp.getX()-50
        for i in range(3):
            xlist[i] = destroyerpx +50*i
        destroyerpy = destroyerp.getY()
        ylist = [destroyerpy, destroyerpy, destroyerpy]
        for i in range(3):
            UserDestroy[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    else:
        ylist = ["","",""]
        destroyerpy = destroyerp.getY()-50
        for i in range(3):
            ylist[i] = destroyerpy +50*i
        destroyerpx = destroyerp.getX()
        xlist = [destroyerpx, destroyerpx, destroyerpx]
        for i in range(3):
            UserDestroy[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    battleshipp = battleship.getAnchor()
    if battleship.getWidth() > battleship.getHeight():
        xlist = ["","","",""]
        battleshippx = battleshipp.getX()-75
        for i in range(4):
            xlist[i] = battleshippx +50*i
        battleshippy = battleshipp.getY()
        ylist = [battleshippy, battleshippy, battleshippy, battleshippy]
        for i in range(4):
            UserBattle[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    else:
        ylist = ["","","",""]
        battleshippy = battleshipp.getY()-75
        for i in range(4):
            ylist[i] = battleshippy +50*i
        battleshippx = battleshipp.getX()
        xlist = [battleshippx, battleshippx, battleshippx, battleshippx]
        for i in range(4):
            UserBattle[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    carrierp = carrier.getAnchor()
    if carrier.getWidth() > carrier.getHeight():
        xlist = ["","","","",""]
        carrierpx = carrierp.getX()-100
        for i in range(5):
            xlist[i] = carrierpx +50*i
        carrierpy = carrierp.getY()
        ylist = [carrierpy, carrierpy, carrierpy, carrierpy, carrierpy]
        for i in range(5):
            UserCarrier[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    else:
        ylist = ["","","","",""]
        carrierpy = carrierp.getY()-100
        for i in range(5):
            ylist[i] = carrierpy +50*i
        carrierpx = carrierp.getX()
        xlist = [carrierpx, carrierpx, carrierpx, carrierpx, carrierpx]
        for i in range(5):
            UserCarrier[i] = row[int((ylist[i]-25)/50)]+column[int((xlist[i]-25)/50)]
    #repeats for all values and returns the ships
    return (UserCarrier,UserBattle,UserDestroy,UserSub,UserPatrol)
#
#input:AI's ships, user's shots and AI window
#output: the point chosen and the results of the choice
#
def userTurn(AICarrier, AIBattle, AIDestroy, AISub, AIPatrol,usershotlist, AIWin):
    while True:
        #get's mouse's points
        p1 = AIWin.getMouse()
        x = ((p1.getX()//50)*50)+25
        y = ((p1.getY()//50)*50)+25
        #makes sure it is on grid
        if 0<x<500 and 0<y<500:
            #only continues if location has not been chosen before
            choice = row[int((y)/50)]+column[int((x)/50)]
            if "".join(usershotlist).find(choice) == -1:
                break
    #checks turn and creates circle
    turn = hitcheck2(AICarrier,AIBattle,AIDestroy,AISub,AIPatrol,choice)
    mark = Circle(Point(x,y),15)
    mark.draw(AIWin)
    hom1 = turn.split("_")
    hom = hom1[0]
    if hom == "hit":
         mark.setFill('Red')
    else:
        mark.setFill('White')
    #print turn to dialouge box
    return choice,hom1
#
#input:none
#output:The AI's ships as lists of points
#
def AIplacement():
    while True:
        #measuring from tip of the boat
        x = random.randint(0,9)
        y = random.randint(0,9)
        orient = random.randint(0,1)
        #0 = horizontal
        #1 = vertical
        #creates a list of points with the row and column lists
        if orient == 0 and (x < 6):
            AICarrier = ["","","","",""]
            #goes through a loop to do this
            for i in range(5):
                AICarrier[i] =row[y]+column[x+i]
            break
        #does it in a vertical case also
        if orient == 1 and (y < 6):
            AICarrier = ["","","","",""]
            for i in range(5):
                AICarrier[i] = row[y+i]+column[x]
            break
    while True:
        #creates a list to check for overlaps
        shipcheck = []
        #measuring from tip of the boat
        x = random.randint(0,9)
        y = random.randint(0,9)
        orient = random.randint(0,1)
        #0 = horizontal
        #1 = vertical
        if orient == 0 and (x < 7):
            AIBattle = ["","","",""]
            for i in range(4):
                AIBattle[i] = row[y]+column[x+i]
        elif orient == 1 and (y < 7):
            AIBattle = ["","","",""]
            for i in range(4):
                AIBattle[i] = row[y+i]+column[x]
        #if statement to make sure that everything is in bounds
        if (orient == 0 and (x < 7)) or (orient == 1 and (y < 7)):
            #nested for loop compares each term on ship A to  each term on ship B
            for b in AIBattle:
                for a in AICarrier:
                    #checks if any points are ahared and marks them
                    if b == a:
                        shipcheck = shipcheck+["0"]
                    else:
                        shipcheck = shipcheck+["1"]
            #only breaks loop if there are no overlaps
            if "".join(shipcheck).count("0") == 0:
                break
    #same checking process is repeated for multiple ships
    while True:
        shipcheck1 = []
        shipcheck2 = []
        #measuring from tip of the boat
        x = random.randint(0,9)
        y = random.randint(0,9)
        orient = random.randint(0,1)
        #0 = horizontal
        #1 = vertical
        if orient == 0 and (x < 8):
            AIDestroy = ["","",""]
            for i in range(3):
                AIDestroy[i] = row[y]+column[x+i]
        if orient == 1 and (y < 8):
            AIDestroy = ["","",""]
            for i in range(3):
                AIDestroy[i] = row[y+i]+column[x]
        if (orient == 0 and (x < 8)) or (orient == 1 and (y < 8)):
            for i in AIDestroy:
                for a in AICarrier:
                    if i == a:
                        shipcheck1 = shipcheck1+["0"]
                    else:
                        shipcheck1 = shipcheck1+["1"]
            for i in AIDestroy:
                for a in AIBattle:
                    if i == a:
                        shipcheck2 = shipcheck2+["0"]
                    else:
                        shipcheck2 = shipcheck2+["1"]
            if "".join(shipcheck1).count("0") == 0 and "".join(shipcheck2).count("0") == 0:
                break
    while True:
        shipcheck1 = []
        shipcheck2 = []
        shipcheck3 = []
        #measuring from tip of the boat
        x = random.randint(0,9)
        y = random.randint(0,9)
        orient = random.randint(0,1)
        #0 = horizontal
        #1 = vertical
        if orient == 0 and (x < 8):
            AISub = ["","",""]
            for i in range(3):
                AISub[i] = row[y]+column[x+i]
        if orient == 1 and (y < 8):
            AISub = ["","",""]
            for i in range(3):
                AISub[i] = row[y+i]+column[x]
        if (orient == 0 and (x < 8)) or (orient == 1 and (y < 8)):
            for i in AISub:
                for a in AICarrier:
                    if i == a:
                        shipcheck1 = shipcheck1+["0"]
                    else:
                        shipcheck1 = shipcheck1+["1"]
            for i in AISub:
                for a in AIBattle:
                    if i == a:
                        shipcheck2 = shipcheck2+["0"]
                    else:
                        shipcheck2 = shipcheck2+["1"]
            for i in AISub:
                for a in AIDestroy:
                    if i == a:
                        shipcheck3 = shipcheck3+["0"]
                    else:
                        shipcheck3 = shipcheck3+["1"]
            if "".join(shipcheck1).count("0") == 0 and "".join(shipcheck2).count("0") == 0 and "".join(shipcheck3).count("0") == 0:
                break
    while True:
        shipcheck1 = []
        shipcheck2 = []
        shipcheck3 = []
        shipcheck4 = []
        #measuring from tip of the boat
        x = random.randint(0,9)
        y = random.randint(0,9)
        orient = random.randint(0,1)
        #0 = horizontal
        #1 = vertical
        if orient == 0 and (x < 9):
            AIPatrol = ["",""]
            for i in range(2):
                AIPatrol[i] = row[y]+column[x+i]
        if orient == 1 and (y < 9):
            AIPatrol = ["",""]
            for i in range(2):
                AIPatrol[i] = row[y+i]+column[x]
        if (orient == 0 and (x < 9)) or (orient == 1 and (y < 9)):
            for i in AIPatrol:
                for a in AICarrier:
                    if i == a:
                        shipcheck1 = shipcheck1+["0"]
                    else:
                        shipcheck1 = shipcheck1+["1"]
            for i in AIPatrol:
                for a in AIBattle:
                    if i == a:
                        shipcheck2 = shipcheck2+["0"]
                    else:
                        shipcheck2 = shipcheck2+["1"]
            for i in AIPatrol:
                for a in AIDestroy:
                    if i == a:
                        shipcheck3 = shipcheck3+["0"]
                    else:
                        shipcheck3 = shipcheck3+["1"]
            for i in AIPatrol:
                for a in AISub:
                    if i == a:
                        shipcheck4 = shipcheck4+["0"]
                    else:
                        shipcheck4 = shipcheck4+["1"]
            if "".join(shipcheck1).count("0") == 0 and "".join(shipcheck2).count("0") == 0 and "".join(shipcheck3).count("0") == 0 and "".join(shipcheck4).count("0") == 0:
                break
    return (AICarrier, AIBattle, AIDestroy, AISub, AIPatrol)

#
#input: choice of square shot and ships
#output: result as hit or miss
#
def hitcheck2(Carrier,Battle,Destroy,Sub,Patrol,choice):
    #has if statement check if the point chosen was even part of the ship
    if choice == Patrol[0] or choice == Patrol[1]:
        #goes through the ship and replaces the hit point with "hit"
        for i in range(2):
            if choice == Patrol[i]:
                Patrol[i] = "hit"
                #returns a statement and breaks loop
                turn = "hit_Patrol Boat"
                break
    #same
    elif choice == Sub[0] or choice == Sub[1] or choice == Sub[2]:
        for i in range(3):
            if choice == Sub[i]:
                Sub[i] = "hit"
                turn = "hit_Submarine"
                break
    #same
    elif choice == Destroy[0] or choice == Destroy[1] or choice == Destroy[2]:
        for i in range(3):
            if choice == Destroy[i]:
                Destroy[i] = "hit"
                turn = "hit_Destroyer"
                break
    #same
    elif choice == Battle[0] or choice == Battle[1] or choice == Battle[2] or choice == Battle[3]:
        for i in range(4):
            if choice == Battle[i]:
                Battle[i] = "hit"
                turn = "hit_Battleship"
                break
    #same
    elif choice == Carrier[0] or choice == Carrier[1] or choice == Carrier[2] or choice == Carrier[3] or choice == Carrier[4]:
        for i in range(5):
            if choice == Carrier[i]:
                Carrier[i] = "hit"
                turn = "hit_Aircraft Carrier"
                break
    #final case is here incase nothing matched
    else:
        turn = "miss"
    #returns the statement of whether something was hit or missed
    return turn
#
#input:turn number and graphics window
#output: AI's turn
#
def AIturnEasy(hitcount,hitlist,results,shotlist,flagnum,userCarrier,userBattle,userDestroy,userSub,userPatrol,turnnum,userWin):
    #chooses randomly and makes sure of no repeat by running through list of already existing points
    while True:
        rchoice = random.randint(0,9)
        cchoice = random.randint(0,9)
        choice = row[rchoice]+column[cchoice]
        if "".join(shotlist).find(choice) == -1  and 0<=rchoice<=9 and 0<=cchoice<=9:
            break
    turn = hitcheck2(userCarrier,userBattle,userDestroy,userSub,userPatrol,choice)
    hom1 = turn.split("_")
    hom = hom1[0]
    x = (cchoice)*50+25
    y = (rchoice)*50+25
    mark = Circle(Point(x,y),15)
    mark.draw(userWin)
    #hom1 = turn.split("_")
    #hom = hom1[0]
    if hom == "hit" and "".join(hitlist).find(hom[1]) == -1:
        flagnum = flagnum+1
    if hom == "hit":
        hitlist = hitlist+[hom1[1]]
    results = results+[hom]
    if hom == "hit":
         mark.setFill('Red')
         hitcount = hitcount+1
    else:
        mark.setFill('White')
    #print turn to dialouge box
    shotlist = shotlist+[choice]
    return (hitcount,hitlist,flagnum,shotlist,results,hom1)
#
#input:number of times hit,shipshit,hit or miss log,list of coordinates shot at, number of flags, user ships, turn number and graphics window
#output: Anumber of times hit,shipshit,hit or miss log,list of coordinates shot at, and the results of this turn
#
def AIturn(hitcount,hitlist,results,results2,shotlist,flagnum,userCarrier,userBattle,userDestroy,userSub,userPatrol,turnnum,userWin):
    count = 0
    #first checks if there are any existing flags
    if flagnum == 0:
        #creates a loop that goes until it finds an unused point
        while True:
            rchoice = random.randint(0,9)
            cchoice = random.randint(0,9)
            choice = row[rchoice]+column[cchoice]
            #checks to see that point does not already exist and breaks loop
            if "".join(shotlist).find(choice) == -1  and 0<=rchoice<=9 and 0<=cchoice<=9:
                break
        #goes to function to check for hits
        turn = hitcheck2(userCarrier,userBattle,userDestroy,userSub,userPatrol,choice)
        hom1 = turn.split(" ")
        hom = hom1[0]
        #starts flags if it gets a hit
        if hom == "hit":
            flagnum = 1
    else:
        #checks if there are consecutive hits to get direction
        if results[turnnum-1] == "hit" and results[turnnum-2] == "hit":
            last = shotlist[turnnum-2]
            rowlast = last[0]
            columnlast = last[1]
            #create a list of possible place to select from by finding all combinations of directions
            possible = []
            #determines from possible directions
            if -1<1+"".join(row).find(rowlast)<10:
                rchoice1 = 1+"".join(row).find(rowlast)
                cchoice1 = "".join(column).find(columnlast)
                choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                possible = possible+[choice1]
            if -1<-1+"".join(row).find(rowlast)<10:
                rchoice1 = -1+"".join(row).find(rowlast)
                cchoice1 = "".join(column).find(columnlast)
                choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                possible = possible+[choice1]
            if -1<1+"".join(column).find(columnlast)<10:
                rchoice1 = "".join(row).find(rowlast)
                cchoice1 = 1+"".join(column).find(columnlast)
                choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                possible = possible+[choice1]
            if -1<-1+"".join(column).find(columnlast)<10:
                rchoice1 = "".join(row).find(rowlast)
                cchoice1 = -1+"".join(column).find(columnlast)
                choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                possible = possible+[choice1]
            #checks each possible point if it had been shot at yet
            if "".join(shotlist).find(possible[0]) == -1:
                free = 1
            if "".join(shotlist).find(possible[1]) == -1:
                free = 1
            if len(possible) >= 3:
                if "".join(shotlist).find(possible[2]) == -1:
                    free = 1
            if len(possible) == 4:
                if "".join(shotlist).find(possible[3]) == -1:
                    free = 1
            #if there is a possible place then it will select one randomly
            while True:
                pick = random.randint(0,3)
                if pick == 0:
                    if rowlast == "A":
                        rchoice = 2
                        cchoice = "".join(column).find(columnlast)
                    elif rowlast == "J":
                        rchoice = 7
                        cchoice = "".join(column).find(columnlast)
                    else:
                        rchoice = 1+"".join(row).find(rowlast)
                        cchoice = "".join(column).find(columnlast)
                elif pick == 1:
                    if columnlast == "1":
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 2
                    elif columnlast == "X":
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 7
                    else:
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 1+"".join(column).find(columnlast)
                elif pick == 2:
                    if rowlast == "A":
                        rchoice = 2
                        cchoice = "".join(column).find(columnlast)
                    elif rowlast == "J":
                        rchoice = 7
                        cchoice = "".join(column).find(columnlast)
                    else:
                        rchoice = -1+"".join(row).find(rowlast)
                        cchoice = "".join(column).find(columnlast)
                elif pick == 3:
                    if columnlast == "1":
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 2
                    elif columnlast == "X":
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 7
                    else:
                        rchoice = "".join(row).find(rowlast)
                        cchoice = -1+"".join(column).find(columnlast)
                choice = row[int(rchoice)]+column[int(cchoice)]
                #exits loop if it found a place not shot at yet
                if "".join(shotlist).find(choice) == -1 and 0<=rchoice<=9 and 0<=cchoice<=9:
                    break
        #for a single non-consecutive hit
        elif results[turnnum-1] == "hit":
            last = shotlist[turnnum-1]
            rowlast = last[0]
            columnlast = last[1]
            #follows similar process with possible spaces
            possible = []
            if -1<1+"".join(row).find(rowlast)<10:
                rchoice1 = 1+"".join(row).find(rowlast)
                cchoice1 = "".join(column).find(columnlast)
                choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                possible = possible+[choice1]
            if -1<-1+"".join(row).find(rowlast)<10:
                rchoice1 = -1+"".join(row).find(rowlast)
                cchoice1 = "".join(column).find(columnlast)
                choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                possible = possible+[choice1]
            if -1<1+"".join(column).find(columnlast)<10:
                rchoice1 = "".join(row).find(rowlast)
                cchoice1 = 1+"".join(column).find(columnlast)
                choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                possible = possible+[choice1]
            if -1<-1+"".join(column).find(columnlast)<10:
                rchoice1 = "".join(row).find(rowlast)
                cchoice1 = -1+"".join(column).find(columnlast)
                choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                possible = possible+[choice1]
            if "".join(shotlist).find(possible[0]) == -1:
                free = 1
            if "".join(shotlist).find(possible[1]) == -1:
                free = 1
            if len(possible) >= 3:
                if "".join(shotlist).find(possible[2]) == -1:
                    free = 1
            if len(possible) == 4:
                if "".join(shotlist).find(possible[3]) == -1:
                    free = 1
            while True:
                pick = random.randint(0,3)
                if pick == 0:
                    if rowlast == "A":
                        rchoice = 1
                        cchoice = "".join(column).find(columnlast)
                    elif rowlast == "J":
                        rchoice = 8
                        cchoice = "".join(column).find(columnlast)
                    else:
                        rchoice = 1+"".join(row).find(rowlast)
                        cchoice = "".join(column).find(columnlast)
                elif pick == 1:
                    if columnlast == "1":
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 1
                    elif columnlast == "X":
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 8
                    else:
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 1+"".join(column).find(columnlast)
                elif pick == 2:
                    if rowlast == "A":
                        rchoice = 1
                        cchoice = "".join(column).find(columnlast)
                    elif rowlast == "J":
                        rchoice = 8
                        cchoice = "".join(column).find(columnlast)
                    else:
                        rchoice = -1+"".join(row).find(rowlast)
                        cchoice = "".join(column).find(columnlast)
                elif pick == 3:
                    if columnlast == "1":
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 1
                    elif columnlast == "X":
                        rchoice = "".join(row).find(rowlast)
                        cchoice = 8
                    else:
                        rchoice = "".join(row).find(rowlast)
                        cchoice = -1+"".join(column).find(columnlast)
                choice = row[int(rchoice)]+column[int(cchoice)]
                #makes sure choice works
                if "".join(shotlist).find(choice) == -1 and 0<=rchoice<=9 and 0<=cchoice<=9:
                    break
        #if its a miss then it goes through this function
        elif results[turnnum-1] == "miss":
            #finds last hit with space
            free = 0
            maxnum = -1
            mover = 0
            resultsb = results
            #checks the position of the last hit
            for i in results:
                resultsb[mover] = i
                mover = mover+1 
            #checks for position of last instance of hit
            while True:
                maxnum1 = -1
                for i in resultsb:
                    maxnum1 = maxnum1+1
                    if i == "hit":
                        maxnum = maxnum1
                #back up random selection
                if maxnum == 0:
                    while True:
                        rchoice = random.randint(0,9)
                        cchoice = random.randint(0,9)
                        choice = column[cchoice]+row[rchoice]
                        if "".join(shotlist).find(choice) == -1 and 0<=rchoice<=9 and 0<=cchoice<=9:
                            break
                last2 = shotlist[maxnum]
                rowlast2 = last2[0]
                columnlast2 = last2[1]
                #similar process with the possible spaces
                possible = []
                if -1<1+"".join(row).find(rowlast2)<10:
                    rchoice1 = 1+"".join(row).find(rowlast2)
                    cchoice1 = "".join(column).find(columnlast2)
                    choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                    possible = possible+[choice1]
                if -1<-1+"".join(row).find(rowlast2)<10:
                    rchoice1 = -1+"".join(row).find(rowlast2)
                    cchoice1 = "".join(column).find(columnlast2)
                    choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                    possible = possible+[choice1]
                if -1<1+"".join(column).find(columnlast2)<10:
                    rchoice1 = "".join(row).find(rowlast2)
                    cchoice1 = 1+"".join(column).find(columnlast2)
                    choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                    possible = possible+[choice1]
                if -1<-1+"".join(column).find(columnlast2)<10:
                    rchoice1 = "".join(row).find(rowlast2)
                    cchoice1 = -1+"".join(column).find(columnlast2)
                    choice1 = row[int(rchoice1)]+column[int(cchoice1)]
                    possible = possible+[choice1]
                count = count+1
                if "".join(shotlist).find(possible[0]) == -1:
                    free = 1
                if "".join(shotlist).find(possible[1]) == -1:
                    free = 1
                if len(possible) >= 3:
                    if "".join(shotlist).find(possible[2]) == -1:
                        free = 1
                if len(possible) == 4:
                    if "".join(shotlist).find(possible[3]) == -1:
                        free = 1
                #if alll adjacent spaces are taken from the last hit the list is changed to go to the next position down
                resultsb = resultsb[:(maxnum-1)]
                if free == 1:
                    break
            while True:
                #calculates shot for no repeat
                number = random.randint(0,1)
                if number == 0:
                    rchoice = (-1)**random.randint(0,1)+"".join(row).find(rowlast2)
                    cchoice = "".join(column).find(columnlast2)
                elif number == 1:
                    rchoice = "".join(row).find(rowlast2)
                    cchoice = (-1)**random.randint(0,1)+"".join(column).find(columnlast2)          
                choice = row[int(rchoice)]+column[int(cchoice)]
                #makes sure no repeat
                if "".join(shotlist).find(choice) == -1 and 0<=rchoice<=9 and 0<=cchoice<=9:
                    break
        #random selection in case of error
        else:
            while True:
                rchoice = random.randint(0,9)
                cchoice = random.randint(0,9)
                choice = column[cchoice]+row[rchoice]
                if "".join(shotlist).find(choice) == -1 and 0<=rchoice<=9 and 0<=cchoice<=9:
                    break
        turn = hitcheck2(userCarrier,userBattle,userDestroy,userSub,userPatrol,choice)
    #takes the choices of row and column to determine the centerpoint of the circle
    x = (cchoice)*50+25
    y = (rchoice)*50+25
    #creates and draws a cricle at the select point
    mark = Circle(Point(x,y),15)
    mark.draw(userWin)
    #splits the results statement
    hom1 = turn.split("_")
    hom = hom1[0]
    #creates new flag
    if hom == "hit":
        flagnum = flagnum+1
    #adds part of statement to list and increases hitcount by 1
    if hom == "hit":
        hitlist = hitlist+[hom1[1]]
        hitcount = hitcount+1
    #increases results list
    results = results+[hom]
    #determines color of circle by results statement
    if hom == "hit":
         mark.setFill('Red')
    else:
        mark.setFill('White')
    #adds choice to list of shots
    shotlist = shotlist+[choice]
    return (hitcount,hitlist,flagnum,shotlist,results,results2,hom1)
#
#input: ship name
#output: if the ship is sunk
#
def check(ship):
    #checks if every point on a ship is hit then it decides if it is sunk
    if "".join(ship).count("hit") == len(ship):
        return True
    else:
        return False
#
# This function will play the endscreen menu after the game is completed.
#   input: victory condition (0 or 1)
#   output: endgame decision (0 or 1)
#

def endscreen(n):

    # Defining all colors, images and objects to be called later
    boxColor = color_rgb(250,165,45)
    vicColor = color_rgb(17,50,158)
    defColor = color_rgb(170,0,0)
    endWin = GraphWin("End", 1265, 735)
    
    # User won text
    eText1 = Text(Point(632.5, 300), "YOU ARE VICTORIOUS!!!")
    eText1.setFace('courier')
    eText1.setSize(36)
    eText1.setStyle('bold')

    # User lost text
    eText2 = Text(Point(632.5, 300), "YOU HAVE BEEN DEFEATED")
    eText2.setFace('courier')
    eText2.setSize(36)
    eText2.setStyle('bold')

    # Bomb image
    bombMod = 140
    bombL = Image(Point(180,bombMod), "bomb.gif")
    bombR = Image(Point(1055,bombMod), "bomb.gif")
    
    # Box that houses "play again" text"
    playAgainBox = Rectangle(Point(482.5,525),Point(782.5, 440))
    playAgainBox.setFill(boxColor)
    playAgainBox.setWidth(4)
    playAgainBox.draw(endWin)

    # Box that houses "quit" text
    quitBox = Rectangle(Point(582.5,625),Point(682.5,590))
    quitBox.setFill(boxColor)
    quitBox.setWidth(3)
    quitBox.draw(endWin)
    
    # "Play Again" text
    playAgainText = Text(Point(632.5, 482.5), "PLAY AGAIN?")
    playAgainText.setSize(26)
    playAgainText.setFace('courier')
    playAgainText.draw(endWin)
    
    # "Quit" text
    quitBoxText = Text(Point(632.5, 607.5), "QUIT")
    quitBoxText.setSize(16)
    quitBoxText.setFace('courier')
    quitBoxText.draw(endWin)
    
    # This set of modifiers will be able to cycle through gif images.
    ex = 1
    exMod = str(ex)
    exFile = exMod + "explosion.gif"

    explosionLeft = Image(Point(180,600),exFile)
    explosionRight = Image(Point(1055,600),exFile)

    # Same thing, will cycle through in order to play an animated gif
    flagX = 1
    flagMod = str(flagX)
    flagFile = flagMod + "flag.gif"

    flagLeft = Image(Point(180,367.5),flagFile)
    flagRight = Image(Point(1055,367.5),flagFile)

    # If the user won
    if n == 0:

        # Background will be set to a victorious blue color
        endWin.setBackground(vicColor)
        # Will draw winning text prompt
        eText1.draw(endWin)

        
        # Checkmouse animation loop
        endPressed = False
        
        while endPressed == False:

            # This information is reassigned at the end of each loop iteration in order to properly repeat over and over
            flagX = 1
            flagMod = str(flagX)
            flagFile = flagMod + "flag.gif"

            # Tracks the user's clicks in order to get info on what to do next
            click = endWin.checkMouse()
            if type(click) == type(None):
                endPressed = False
            elif ((click.getX() >= 482.5 and click.getX() <= 782.5 and click.getY() >= 440 and click.getY() <= 525)):
                boxPressed = 0
                break
            elif ((click.getX() >= 582.5 and click.getX() <= 682.5 and click.getY() >= 590 and click.getY() <= 625)):
                boxPressed = 1
                break

            # Animation loops for waving flag
            for i in range(9):
                flagLeft = Image(Point(180,367.5),flagFile)
                flagRight = Image(Point(1055,367.5),flagFile)
                flagLeft.draw(endWin)
                flagRight.draw(endWin)
                time.sleep(.1)
                flagLeft.undraw()
                flagRight.undraw()

                flagX = flagX + 1
                flagMod = str(flagX)
                flagFile = flagMod + "flag.gif"

        # User clicked play again
        if boxPressed == 0:
            endWin.close()
            return 0

        # User clicked quit
        elif boxPressed == 1:
            endWin.close()
            return 1

    # If the user lost
    elif n == 1:

        # Will set background to a red defeat color
        endWin.setBackground(defColor)
        # Will display loser text
        eText2.draw(endWin)
    
        endPressed = False

        # Similar to above
        while endPressed == False:
            ex = 1
            exMod = str(ex)
            exFile = exMod + "explosion.gif"
            bombMod = 140

            click = endWin.checkMouse()
            if type(click) == type(None):
                endPressed = False
            elif ((click.getX() >= 482.5 and click.getX() <= 782.5 and click.getY() >= 440 and click.getY() <= 525)):
                boxPressed = 0
                break
            elif ((click.getX() >= 582.5 and click.getX() <= 682.5 and click.getY() >= 590 and click.getY() <= 625)):
                boxPressed = 1
                break

            # Animation of bombs dropping
            for i in range(4):
                bombL = Image(Point(180,bombMod), "bomb.gif")
                bombR = Image(Point(1055,bombMod), "bomb.gif")
                bombL.draw(endWin)
                bombR.draw(endWin)
                time.sleep(.65)
                bombL.undraw()
                bombR.undraw()
                bombMod = bombMod + 140

            # Animation of explosions happening
            for i in range(9):
                explosionLeft = Image(Point(180,600), exFile)
                explosionRight = Image(Point(1055,600),exFile)
                explosionLeft.draw(endWin)
                explosionRight.draw(endWin)
                time.sleep(.05)
                explosionLeft.undraw()
                explosionRight.undraw()

                ex = ex + 1
                exMod = str(ex)
                exFile = exMod + "explosion.gif"

        # If user selects "play again"
        if boxPressed == 0:
            endWin.close()
            return 0

        # If user selects "quit"
        elif boxPressed == 1:
            endWin.close()
            return 1
#
# The main function will launch the program.
#   input: none
#

def main():

    # Defining the start menu window sizes
    x = 1265
    y = 735
    menuWin = GraphWin("Menu",x,y)
    menuWin.setBackground(color_rgb(17,50,158))

    # Assigning colors to variables to be used in shading
    grey1 = color_rgb(109,117,140)
    grey2 = color_rgb(114,120,140)
    grey3 = color_rgb(124,129,143)
    grey4 = color_rgb(129,132,138)
    grey5 = color_rgb(143,143,143)
    
    # Title image
    title = Image(Point((x/2)+5,230),"battleshipTitle.gif")
    title.draw(menuWin)

    # Box that houses "Start" text
    startButton = Rectangle(Point(x/3,400),Point((x/3)*2,550))
    startButton.setWidth(5)
    startButton.setFill(grey1)
    startButton.draw(menuWin)

    # "Start" text
    startButtonText = Text(Point(x/2,475),"START")
    startButtonText.setFace('courier')
    startButtonText.setSize(36)
    startButtonText.draw(menuWin)

    # Author text
    authorText = Text(Point(x/2,675), "AUSTIN CHEN AND DANIEL FINER '15")
    authorText.setFace('courier')
    authorText.setSize(20)
    authorText.draw(menuWin)

    # Animation loop
    startPressed = 0
    
    while startPressed == 0:
        click = menuWin.checkMouse()
        if type(click) == type(None):
            startPressed = 0
        elif ((click.getX() >= (x/3) and click.getX() <= ((x/3)*2)) and (click.getY() >= 400 and click.getY() <= 550)):
            break

        # Oscillating between <50 shades of gray
        startButton.setFill(grey1)
        time.sleep(.075)
        menuWin.update()
        startButton.setFill(grey2)
        time.sleep(.075)
        menuWin.update()
        startButton.setFill(grey3)
        time.sleep(.075)
        menuWin.update()
        startButton.setFill(grey4)
        time.sleep(.075)
        menuWin.update()
        startButton.setFill(grey5)
        time.sleep(.075)
        menuWin.update()

        time.sleep(.75)

        startButton.setFill(grey4)
        time.sleep(.075)
        menuWin.update()
        startButton.setFill(grey3)
        time.sleep(.075)
        menuWin.update()
        startButton.setFill(grey2)
        time.sleep(.075)
        menuWin.update()
        startButton.setFill(grey1)
        time.sleep(.075)
        menuWin.update()

    # Waits for user to click box in order to stop loop
    startButton.undraw()
    startButtonText.undraw()
    authorText.undraw()
    title.undraw()

    # Instructions

    # Instructions Text1
    iText1 = Text(Point(200,100),"INSTRUCTIONS:")
    iText1.setFace('courier')
    iText1.setSize(36)
    iText1.draw(menuWin)

        
    # Instructions Text2
    iText2 = Text(Point(534,175),"1.  Click on-screen arrow keys to move ship placement.")
    iText2.setFace('courier')
    iText2.setSize(28)
    iText2.draw(menuWin)

    # Instructions Text3
    iText3 = Text(Point(593.48,250),"2.  Click 'Rotate' and 'Lock In' to orient and lock the ship.")
    iText3.setFace('courier')
    iText3.setSize(28)
    iText3.draw(menuWin)

    # Instructions Text4
    iText4 = Text(Point(560,325),"3.  You will take turns with the computer dropping bombs.")
    iText4.setFace('courier')
    iText4.setSize(28)
    iText4.draw(menuWin)
    
    # Instructions Text5
    iText5 = Text(Point(502,400),"4.  Whoever sinks all their opponents' ships wins!")
    iText5.setFace('courier')
    iText5.setSize(28)
    iText5.draw(menuWin)

    # Continue Text
    continueText = Text(Point(632.5,690),">>> Click anywhere on the screen to continue >>>")
    continueText.setFace('courier')
    continueText.setSize(14)
    continueText.draw(menuWin)
    
    # Pause for user clickxt
    menuWin.getMouse()

    iText1.undraw()
    iText2.undraw()
    iText3.undraw()
    iText4.undraw()
    iText5.undraw()
    continueText.undraw()

    chooseText = Text(Point(632.5,200), "CHOOSE YOUR DIFFICULTY:")
    chooseText.setFace('courier')
    chooseText.setSize(32)
    chooseText.draw(menuWin)

    easyBox = Rectangle(Point(468.518519,330),Point(796.48149,420))
    easyBox.setFill(color_rgb(250,165,45))
    easyBox.setWidth(4)
    easyBox.draw(menuWin)

    hardBox = Rectangle(Point(468.518519, 450), Point(796.48149, 540))
    hardBox.setFill(color_rgb(250,165,45))
    hardBox.setWidth(4)
    hardBox.draw(menuWin)

    easyText = Text(Point(632.5,375), "EASY")
    easyText.setFace('courier')
    easyText.setSize(28)
    easyText.draw(menuWin)

    hardText = Text(Point(632.5,495), "HARD")
    hardText.setFace('courier')
    hardText.setSize(28)
    hardText.draw(menuWin)

    #click to get selection
    selection = False
    while not selection:
        click2 = menuWin.getMouse()
    
    #boxes to determine the difficulty
        if (click2.getX() >= 468.518519 and click2.getX() <= 796.48149 and click2.getY() >= 330 and click2.getY() <= 420):
            diff = 0
            selection = True
        elif (click2.getX() >= 468.518519 and click2.getX() <= 796.48149 and click2.getY() >= 450 and click2.getY() <= 540):
            diff = 1
            selection = True

    menuWin.close()
    
    userGUI(diff)
                          
    

main()
