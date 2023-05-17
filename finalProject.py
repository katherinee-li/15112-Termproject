from cmu_graphics import *
import random
import math
from PIL import Image
import time 
import copy


#classes
class Character:
    def __init__(self, name, money, location, app, color, position):
        self.name = name
        self.location = location
        self.money= money
        self.color = color 
        self.prop= []
        self.position= position

    def __repr__(self):
        return (f"Char(name = player{self.name} location={self.location}, money={self.money}"
        +f" prop={self.prop})")

    def draw(self, app):
        row, col = self.location
        changeX = 23
        topX, topY = getTopCoor(app, row, col)
        cellWidth, cellHeight = getCellSize(app)
        topX-=15
        topY-=15
        cellBottomX, cellBottomY= topX, topY + cellHeight
        cellRightX, cellRightY= topX+cellWidth, topY+ changeX
        cellLeftX, cellLeftY = topX - cellWidth, topY + (cellHeight-changeX)
        drawPolygon(topX, topY, cellLeftX, cellLeftY, cellBottomX, cellBottomY, cellRightX, cellRightY, 
            fill=None, border=self.color,
            borderWidth= 3)

    def drawInfo(self, app):
        x= 45+ self.position *350
        y = 50
        drawImage(app.greyBox, x,y, width = 300, height = 80)
        
        drawLabel(f'{self.name}', x+68,y+40, font='monospace', size=18, bold = True, fill = 'grey')
        drawLabel(f'MONEY: {int(self.money)}', x+200,y+25, font='monospace', size=15.5, bold = True, fill = 'darkgray')
        drawLabel(f'PROPERTIES: {len(self.prop)}', x+200,y+50, font='monospace', size=15.5, bold = True, fill = 'darkgray')
    

    def buy(self, tile):
        self.prop.append(tile)
        self.money -= tile.price    

    

class Tiles:
    def __init__(self, location, value, topCoord, app, price, color):
        self.location = location 
        self.value = value
        self.state = False
        self.topCoord = topCoord
        self.price = price
        self.item = None 
        self.color = color

    def __repr__(self):
        return (f"Tile(location={self.location}, value={self.value}"
        +f" state={self.state}) topCoord = {self.topCoord}")

    def bought(self, app):
        self.state = True 
        self.color = app.currentChar.color 

    def drawBuy(self, app):
        width = 370 
        height = 200
        x, y = 720, 335
        drawImage(app.greyBox, app.width/2- width/2 , app.height/2 - height/2-50, width = width+25, height = height-25)
        drawLabel(f"Buy property for ${app.tileInstance.price}", x, y+15, font='monospace', size=25, bold = True, fill = "darkseagreen")
        drawLabel('Press y to buy n to skip', x, y+100, font='monospace', size=22, bold = True, fill = "darkseagreen")
        
             
    def drawPay(self, app):
        width = 370 
        height = 200
        x, y = 720, 335
        drawImage(app.greyBox, app.width/2- width/2 , app.height/2 - height/2-50, width = width+25, height = height-40)
        drawLabel(f"Oops. Rent is ${int(app.tileInstance.price/10)}!", x+30, y, font='monospace', size=25, bold = True, fill = "red")
        drawLabel('Press c to continue', x+20, y+80, font='monospace', size=22, bold = True, fill = "red")

    def prop(self, app):
        if self.state == False: #not bought
            app.buyMessage = True 
            app.payMessage = False
        elif self.state ==True: #bought
            app.currentChar.money -=self.price/10
            for x in app.charList:
                if self in x.prop:
                    print("hi")
                    x.money += self.price/10

            app.payMessage = True
            app.buyMessage = False 
        
    def good(self, app):
  
        index = random.randrange(1, 4) #3 dif good choices
        if index ==1:
            app.goodMessage1= True       
        if index ==2:
            app.goodMessage2= True 
        if index ==3:
 
            app.goodMessage3 = True
    def bad(self, app):
        app.currentChar.money-=50
        index = random.randrange(1, 4) #3 dif good choices
       
        if index ==1:

            app.badMessage1= True       
        if index ==2:

            app.badMessage2= True 
        if index ==3:
         
            app.badMessage3 = True

    def store(self, app):
        app.inStore=True
        app.storeMessage = True #drawmessage

    def drawBadGood(self, app):
        row, col = self.location
        changeX = 23
        topX, topY = getTopCoor(app, row, col)
        topX-=6.5
        topY-=6
        cellWidth, cellHeight = getCellSize(app)
        cellBottomX, cellBottomY= topX, topY + cellHeight
        cellRightX, cellRightY= topX+cellWidth, topY+ changeX
        cellLeftX, cellLeftY = topX - cellWidth, topY + (cellHeight-changeX)
        drawPolygon(topX, topY, cellLeftX, cellLeftY, cellBottomX, cellBottomY, cellRightX, cellRightY, 
            fill='lightsteelblue',opacity=60, border = 'lightsteelblue', borderWidth= 3)
       
    def draw(self, app):
        row, col = self.location
        changeX = 23
        topX, topY = getTopCoor(app, row, col)
        topX-=6.5
        topY-=6
        cellWidth, cellHeight = getCellSize(app)
        cellBottomX, cellBottomY= topX, topY + cellHeight
        cellRightX, cellRightY= topX+cellWidth, topY+ changeX
        cellLeftX, cellLeftY = topX - cellWidth, topY + (cellHeight-changeX)
        drawPolygon(topX, topY, cellLeftX, cellLeftY, cellBottomX, cellBottomY, cellRightX, cellRightY, 
            fill=self.color,opacity=40, border = self.color, borderWidth= 3)
        drawLine(topX-25, topY+20, topX+1, topY+30, fill=self.color) 
        drawLine(topX+1, topY+30, topX+20, topY+22, fill=self.color) 

    def drawStore(self, app):
        x, y = self.topCoord
        x-=74
        y-=6
        drawImage(app.scotty, x, y, width = 130, height= 50)

        row, col = self.location
        changeX = 23
        topX, topY = getTopCoor(app, row, col)
        topX-=6.5
        topY-=6
        cellWidth, cellHeight = getCellSize(app)
        cellBottomX, cellBottomY= topX, topY + cellHeight
        cellRightX, cellRightY= topX+cellWidth, topY+ changeX
        cellLeftX, cellLeftY = topX - cellWidth, topY + (cellHeight-changeX)

        drawPolygon(topX, topY-2, cellLeftX-4, cellLeftY, cellBottomX, cellBottomY, cellRightX, cellRightY+1, 
            fill='mistyrose',opacity=70)
    

class Button:
    def __init__(self, x, y, function, message, app):
        self.x = x
        self.y= y
        self.function= function
        self.message= message 

    def draw(self, app):
        drawImage(app.greyBox, self.x, self.y,  width = 140, height = 58)
        drawLabel(f'{self.message}', self.x+70, self.y+29, font='monospace', bold = True, fill= 'darkgray', size = 23)

    def press(self, app, mX, mY):
        if mX>=self.x and mX<= self.x+80 and mY>= self.y and mY <= self.y+60:
            self.function(app)
  
                

def rollDiceFunc(app):
    app.diceRollComplete= True
    app.dice1= random.randrange(1, 7)
    app.dice2= random.randrange(1, 7)
    app.diceTotal = app.dice1+app.dice2
    app.diceState= False
    app.routeState = True 
    pathFindList(app)

def endTurnFunc(app):
    
    app.currentCharIndex= (app.currentCharIndex+1)%4
    app.currentChar= app.charList[app.currentCharIndex]  
    app.caughtRoaches= False
    app.caughtUSB= False
    app.caughtFood= False
    app.outStore = False
    app.diceState = True
    aiChar(app) 
    app.endTurn = False
    app.actionState = False

    #delete all messages still on screen
    app.goodMessage1= False
    app.goodMessage2= False
    app.goodMessage3= False
    app.goodMessage4= False
    app.badMessage1= False
    app.badMessage2= False
    app.badMessage3= False
    app.badMessage4= False
    app.storeMessage= False
    app.buyMessage = False
    app.payMessage = False

   
def onAppStart(app):
    restart(app)

def restart(app):  
    #user input
    app.player1Input= True
    app.player2Input= False
    app.player3Input= False
    app.player4Input= False
    app.playerName1= ""
    app.playerName2= ""
    app.playerName3= ""
    app.playerName4= 'Computer'
    
    
    app.widthPlayerBox=400
    app.heightPlayerBox=58
    app.widthPlayerBox1 = 100
    app.heightPlayerBox1 = 58


    app.startButton= False
    
    #timer
    app.counterSec = 1800
    app.counterTenSec= 180
    app.counterMin= 30
    app.counterTenMin= 3
    app.counter4= 0
    app.counter3=0
    app.counter2=0
    app.counter1=3
    app.stepsPerSecond=1

    #board functions
    app.rows = 10
    app.cols = 10
    app.boardLeft = 720
    app.boardTop = 220
    app.boardWidth = 650
    app.boardHeight = 500
    app.cellBorderWidth = 2
    app.boardCells = [(0,5), (0,6),(0,7),(0,8), (0,9), 
                      (1,5), (1,7),(1,9),
                      (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),
                      (3,0),(3,5),(3,7),(3,9),
                      (4,0),(4,3),(4,4), (4,5),(4,7),(4,9),
                      (5,0),(5,1),(5,2),(5,3),(5,5),(5,6),(5,7),(5,9),
                      (6,0),(6,3),(6,5),(6,7),(6,9),
                      (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,9),
                      (8,0),(8,3),(8,7),(8,9),
                      (9,0),(9,1),(9,2),(9,3),(9,7),(9,8),(9,9)]
    #tileTypes and values
    app.listPropTiles = [(0,6), (0,7), (0,8), 
                            (2,1), (2,5), 
                            (3,5), 
                            (5,1), (5,2), (5,5), (5,6), (5,9),
                            (6,0,), (6,9),
                            (7,0),(7,3), (7,4), (7,7), (7,9),
                            (8,7),
                            (9,1),(9,2),(9,3)
                            ]
    app.listAIbuy= [(2,1), (2,5), (3,5), (5,1), (5,2), (5,5), (5,6), (6,0), (7,0), (7,3), (7,4), (7,7)]

    app.tilePrice = [(200),(300),(400),(100), (200), 
                      (200), (300),(400),
                      (200),(100),(300),(400),(100),(200),(300),(400),(200),(100),
                      (300),(200),(300),(400),
                      (100),(100),(200), (200),(300),(200),
                      (100),(100),(200), (200),(300),(200),(100),(100),
                      (100),(100),(200), (200),(300),
                      (200),(100),(300),(400),(100),(200),(300),(400),(200),
                      (100),(100),(200), (200),
                      (200),(100),(300),(400),(100),(200),(300)
                      ]


    
    #normla tiles:
    app.listNormalTiles= [(2,3), (2, 3), (2,4), (0,5), (1,5), (1,7), (1,9), 
                        (2,4), (2,6), (2,8), (2,9), (3,7), (3,9), (4,3), (4,5), 
                        (5,0), (5,3), (5,7), (6,6), (6,7), (7,1), (7,2), (7,5),
                        (7,6), (7,7), (8,0), (8,3), (8,9), (9,8)
                                                ]
    #good tiles
    app.listGoodTiles= [( 0,9), (4,0), (4,4), (4,7), (6,3), (9,9)]
    app.goodMessage1= False
    app.goodMessage2= False
    app.goodMessage3= False
    app.goodMessage4= False

    #bad tiles
    app.listBadTiles = [(2,2), (2,7), (4,9), (6,5), (9,0)]
    app.badMessage1= False
    app.badMessage2= False
    app.badMessage3= False
    app.badMessage4= False

    #store tiles
    app.listStoreTiles = [(3,0), (9,7)]
    app.boughtTileList= []
    app.storeMessage= False
    app.inStore=False
    app.outStore=False
    app.choosenTile= None

    app.pickTileItem1= False
    app.drawItem1= False
    app.caughtRoaches=False
    

    app.pickTileItem2=False
    app.drawItem2=False
    app.caughtUSB=False

    app.pickTileItem3= False
    app.drawItem3= False
    app.caughtFood=False


    #buying property:
    app.Tiles = None
    app.tileInstance= None
    app.tileList = []
    createTileInstances(app)
    app.buyMessage = False
    app.payMessage = False

    #characters:
    app.charList= []
    app.charNum= 4
    app.charColor= ["purple", 'pink','lightgreen', 'blue']
    game_createCharInstances(app)
    app.charList[3].name = "Computer"


    app.currentCharIndex= 0
    app.currentChar= app.charList[app.currentCharIndex] #temp variable, starts at player 1 
    app.messagePickChar=None

    #moving apps
    app.pickAgainMessage= None
    app.finalSet= None

    #game states
    app.diceState=True
    app.routeState =False
    app.actionState=False
    app.endTurn= False

    #buttons
    #dice
    app.rollDice= Button(1200, 820, rollDiceFunc, "Roll Dice", app)
    app.diceRollComplete= False
    app.dice = None
    app.diceTotal= None

    #end
    app.endTurnBut= Button(900, 820, endTurnFunc,  "End Turn", app)

    
    #pathfinding
    app.dictt= {
        (0,5):[(0,6)], (0,6):[(0,7)], (0,7):[(0,8), (1,7)], (0,8):[(0,9)],(0,9):[(1,9)],
        (1,5):[(0,5)], (1,7):[(2,7)], (1,9):[(2,9)],
        (2,0):[(2,1)], (2,1):[(2,2)], (2,2):[(2,3)], (2,3):[(2,4)], (2,4):[(2,5)], (2,5):[(1,5),(3,5), (2,6)], (2,6):[(2,7)], (2,7):[(3,7)], (2,8):[(2,7)], (2,9):[(2,8), (3,9)],
        (3,0):[(2,0)], (3,5):[(4,5)], (3,7):[(4,7)], (3,9):[(4,9)],
        (4,0):[(3,0)], (4,3):[(5,3)], (4,4):[(4,3)], (4,5):[(4,4),(5,5)], (4,7):[(5,7)], (4,9):[(5,9)],
        (5,0):[(4,0)],(5,1):[(5,0)],(5,2):[(5,1)], (5,3):[(5,2),(6,3)], (5,5):[(6,5)], (5,6):[(5,5)], (5,7):[(5,6), (6,7)], (5,9):[(6,9)],
        (6,0):[(5,0)], (6,3):[(7,3)], (6,5):[(7,5)], (6,7):[(7,7)], (6,9):[(7,9)],
        (7,0):[(6,0)], (7,1):[(7,0)], (7,2):[(7,1)], (7,3):[(7,2), (8,3)], (7,4):[(7,3)], (7,5):[(7,4)], (7,6):[(7,5)], (7,7):[(7,6)], (7,9):[(8,9)],
        (8,0):[(7,0)], (8,3):[(9,3)], (8,7):[(7,7)], (8,9):[(9,9)],
        (9,0):[(8,0)], (9,1):[(9,0)], (9,2):[(9,1)], (9,3):[(9,2)], (9,7):[(8,7)], (9,8):[(9,7)], (9,9):[(9,8)]
                }
    

    #board images

    #tile image from https://www.ebay.com/itm/362782826257 
    app.boardTile= Image.open("tile.png").convert('RGBA')
    app.boardTile = CMUImage(app.boardTile)
    app.greyBox= Image.open("greyBox.png").convert('RGBA')
    app.greyBox = CMUImage(app.greyBox)

    #scotty image from https://www.cmubookstore.com
    app.scotty= Image.open("scotty.png").convert('RGBA')
    app.scotty = CMUImage(app.scotty)
    
    #created myself
    app.pinkBox= Image.open("pinkBox.png").convert('RGBA')
    app.pinkBox = CMUImage(app.pinkBox)

    #title logo designed from canva https://www.canva.com/design/DAFhOLOIea0/jSF88R4Is71DHzH_bE400w/edit
    app.titlee= Image.open("title.png").convert('RGBA')
    app.titlee = CMUImage(app.titlee)

    #created myself
    app.exit= Image.open("exit.png").convert('RGBA')
    app.exit = CMUImage(app.exit)

    #cmu logo from https://www.cmu.edu/brand/downloads/assets/images/scotty-icon-600x600-min.jpg
    app.logo= Image.open("cmuLogo.png").convert('RGBA')
    app.logo = CMUImage(app.logo)

    #food image from https://www.cleanpng.com/png-food-poisoning-hand-painted-gourmet-burger-materia-432418/
    app.food= Image.open("food.png").convert('RGBA')
    app.food = CMUImage(app.food)

    #fishing image from https://clipartpng.com/?2531,cockroach-png-clip-art
    app.fishing= Image.open("fishing.png").convert('RGBA')
    app.fishing = CMUImage(app.fishing)

    #usb image from https://www.youtube.com/watch?v=w5g6Nm5m4yA
    app.usb= Image.open("usb.png").convert('RGBA')
    app.usb = CMUImage(app.usb)

    #dice image from https://www.teacherspayteachers.com/Product/Dice-and-Dominoes-Clipart-Graphics-FREE-306749
    app.dice1Image= Image.open("dice1.png").convert('RGBA')
    app.dice1Image = CMUImage(app.dice1Image)
    app.dice2Image= Image.open("dice2.png").convert('RGBA')
    app.dice2Image = CMUImage(app.dice2Image)
    app.dice3Image= Image.open("dice3.png").convert('RGBA')
    app.dice3Image = CMUImage(app.dice3Image)
    app.dice4Image= Image.open("dice4.png").convert('RGBA')
    app.dice4Image = CMUImage(app.dice4Image)
    app.dice5Image= Image.open("dice5.png").convert('RGBA')
    app.dice5Image = CMUImage(app.dice5Image)
    app.dice6Image= Image.open("dice6.png").convert('RGBA')
    app.dice6Image = CMUImage(app.dice6Image)

    
    

def aiChar(app):
    if app.currentChar == app.charList[3]:
        if app.diceState==True:
            rollDiceFunc(app)
            
        if app.routeState==True:
            if len(app.finalSet)==1:
                for tile in app.tileList:
                    if tile.location in app.finalSet:
                        currentTile = tile 
                        app.tileInstance = currentTile
                        app.currentChar.location= currentTile.location
                
                    
            else:
                for tile in app.tileList:
                    if tile.location in app.finalSet:
                        currentTile = tile 
                        if currentTile.state == False or currentTile.location in app.listStoreTiles:
                            app.tileInstance = currentTile
                            app.currentChar.location= currentTile.location

                        elif currentTile.location in app.listNormalTiles:
                            app.tileInstance = currentTile
                            app.currentChar.location= currentTile.location

                        elif currentTile.location in app.listBadTiles or currentTile.location in app.listGoodTiles:
                            app.tileInstance = currentTile
                            app.currentChar.location= currentTile.location
                            
                            
                        elif currentTile.state==True:
                            app.tileInstance = currentTile
                            app.currentChar.location= currentTile.location
                            app.tileInstance.prop(app)

                        else:
                            app.tileInstance = currentTile
                            app.currentChar.location= currentTile.location
            


            if app.tileInstance.location in app.listPropTiles: #if (row,col) of tile is a property tile

                if app.tileInstance.state == False and app.tileInstance.location in app.listAIbuy and app.currentChar.money >=500: #buy land
                    app.tileInstance.bought(app)
                    app.currentChar.buy(app.tileInstance) 

                elif app.tileInstance.state ==True: #bought
                    app.currentChar.money -=app.tileInstance.price/10
                    for x in app.charList:
                        if app.tileInstance in x.prop:
                            x.money += app.tileInstance.price/10


            elif app.tileInstance.location in app.listGoodTiles:
                app.tileInstance.good(app)

            elif app.tileInstance.location in app.listBadTiles:
                app.tileInstance.bad(app)
                

            elif app.tileInstance.location in app.listStoreTiles:
                app.tileInstance.store(app)
                
        
            elif app.tileInstance.item =="item1":
                app.caughtRoaches = True 
                app.currentChar.money -=100
                app.tileInstance.item =None
                app.boughtTileList.remove(app.tileInstance.location)
                

            elif app.tileInstance.item =="item2":
                app.caughtUSB = True 
                app.currentChar.money -=120
                app.tileInstance.item =None
                app.boughtTileList.remove(app.tileInstance.location)
                
                

            elif app.tileInstance.item =="item3":
                app.caughtFood = True 
                app.currentChar.money -=150
                app.tileInstance.item =None
                app.boughtTileList.remove(app.tileInstance.location)
                
               
            time.sleep(0.5)
            endTurnFunc(app)
        app.routeState=False
        app.actionState =True
            
       
    
def game_onStep(app):
    app.counterSec-=1

    app.counter4= app.counterSec%10
    if (app.counterSec+1)%10 == 0: #every 10 sec
        app.counterTenSec-=1
        app.counter3 =(app.counterTenSec)%6
    if (app.counterSec+1)%60 == 0:
        app.counterMin-=1
        app.counter2= app.counterMin%10
    if (app.counterSec+1) % 600 == 0:
        app.counterTenMin -=1
        app.counter1= app.counterTenMin%6
    if app.counterSec== 0:
        setActiveScreen('win')
    
#creating classes-------------------------------------------------------------
def game_createCharInstances(app):
    for x in range(4):
        color = app.charColor[x]
        char = Character(x, 2000, (2,0), app, color, x)
        app.charList.append(char)
    
def createTileInstances(app): #creates a list of tile instances 
    for x in range(len(app.boardCells)):
        (row,col) = app.boardCells[x] #tile location
        value = app.tilePrice[x] #tile value
        topCoord = getTopCoor(app, row, col)
        price = app.tilePrice[x]
        color = 'darkseagreen'
        tiles = Tiles((row,col), value, topCoord, app, price, color)
        app.tileList.append(tiles)
   

#moving pieces
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)



def game_onKeyPress(app, key):
    if key == "r":
        restart(app)
        setActiveScreen('start')

    if app.buyMessage == True: 
        if key == 'y':
            app.tileInstance.bought(app)
            app.currentChar.buy(app.tileInstance) 
            app.buyMessage = False
            app.endTurn = True 

        elif key == 'n':
            app.buyMessage = False
            app.endTurn = True 
    if app.payMessage ==True:
        if key =='c':
            app.payMessage =False
            app.endTurn = True 

    if app.goodMessage1 == True or app.goodMessage2 ==True or app.goodMessage3 ==True:
        if key =='c':
            app.currentChar.money+=50
            app.goodMessage1=app.goodMessage2=app.goodMessage3= False
            app.endTurn = True 
    if app.badMessage1 == True or app.badMessage2 ==True or app.badMessage3 ==True:
        if key =='c':
            app.badMessage1=app.badMessage2=app.badMessage3= False
            app.endTurn = True 

    if app.inStore == True:
        if key == "1":
            app.storeMessage =False
            app.pickTileItem1= True #pick a tile to put object on 
            app.pickTileItem2= False
            app.pickTileItem3= False
        
            
            app.outStore = True
            app.inStore = False
            app.endTurn = True 

        if key == "2":
            app.storeMessage =False
            app.pickTileItem2= True 
            app.pickTileItem1= False
            app.pickTileItem3= False

            
            app.inStore = False
            app.outStore = True
            app.endTurn = True 


        if key == "3":
            app.storeMessage =False
            app.pickTileItem3= True 
            app.pickTileItem2= False
            app.pickTileItem1= False
            
            app.inStore = False
            app.outStore = True
            app.endTurn = True 

        if key == 'e':
            app.storeMessage =False
            app.inStore = False
            app.endTurn = True 


    if app.outStore == True:    
        if app.drawItem1== True or app.drawItem2== True or app.drawItem3== True:
            if key== 's':
                app.drawItem1=False
                app.drawItem2=False
                app.drawItem3=False
                app.outStore == False
                app.inStore = True
                app.storeMessage = True
                    

        if app.drawItem1== True:
            if key =='y': 
                app.choosenTile.item= "item1"
                app.boughtTileList.append(app.choosenTile.location)
                app.currentChar.money-=20
                app.pickTileItem1= False
                app.outStore= False
                app.endTurn = True

        if app.drawItem2== True:
            if key =='y':
                app.choosenTile.item= "item2"
                app.boughtTileList.append(app.choosenTile.location)
                app.currentChar.money-=30
                 
                app.outStore= False
                app.pickTileItem2= False
                app.endTurn = True

        if app.drawItem3== True:
            if key =='y':
                app.choosenTile.item= "item3"
                app.boughtTileList.append(app.choosenTile.location)
                app.currentChar.money-=40
           
                app.outStore= False
                app.pickTileItem3= False
                app.endTurn = True

                   

def pickTileItem1(app, mouseX,mouseY):
    cellIndex = getCellIndex(app, mouseX, mouseY) 
    if cellIndex not in app.listNormalTiles or cellIndex in app.boughtTileList:
        app.pickAgainMessage = "Pick A Valid Position"

    else:
        app.pickAgainMessage = None
        for x in range(len(app.boardCells)):
            if app.boardCells[x]== cellIndex:
                currentTile = x 
        app.choosenTile = app.tileList[currentTile]
       
        app.drawItem1= True 

def pickTileItem2(app, mouseX,mouseY):
    cellIndex = getCellIndex(app, mouseX, mouseY) 
    if cellIndex not in app.listNormalTiles or cellIndex in app.boughtTileList:
        app.pickAgainMessage = "Pick A Valid Position"

    else:
        app.pickAgainMessage = None
        for x in range(len(app.boardCells)):
            if app.boardCells[x]== cellIndex:
                currentTile = x 
        app.choosenTile = app.tileList[currentTile]
        app.drawItem2= True 

def pickTileItem3(app, mouseX,mouseY):
    cellIndex = getCellIndex(app, mouseX, mouseY) 
    if cellIndex not in app.listNormalTiles or cellIndex in app.boughtTileList:
        app.pickAgainMessage = "Pick A Valid Position"

    else:
        app.pickAgainMessage = None
        for x in range(len(app.boardCells)):
            if app.boardCells[x]== cellIndex:
                currentTile = x 
        app.choosenTile = app.tileList[currentTile]
        app.drawItem3= True 

def game_onMousePress(app, mouseX, mouseY):
    #dice
    if app.diceState== True and app.currentChar!= app.charList[3]:
        app.rollDice.press(app, mouseX, mouseY)

    app.endTurnBut.press(app, mouseX, mouseY)


    #buying items:
    if app.outStore == True:
        if app.pickTileItem1== True:
            pickTileItem1(app, mouseX,mouseY)

        elif app.pickTileItem2==True:
            pickTileItem2(app, mouseX,mouseY)

        elif app.pickTileItem3==True:
            pickTileItem3(app, mouseX,mouseY)
    

    #moving character
    if app.routeState== True:
        cellIndex = getCellIndex(app, mouseX, mouseY)
        if cellIndex ==None or cellIndex not in app.boardCells or cellIndex not in app.finalSet:
            #app.pickAgainMessage = "Pick A Valid Position"
            app.buyMessage = False
            app.payMessage = False

        else:
            for x in range(len(app.boardCells)):
                if app.boardCells[x]== cellIndex:
                    currentTile = x 

            app.tileInstance = app.tileList[currentTile]
            app.currentChar.location= cellIndex
            app.pickAgainMessage = None
            
            
            #determine what type the tile is 
            if app.tileInstance.location in app.listPropTiles: #if (row,col) of tile is a property tile
                app.tileInstance.prop(app)

            elif app.tileInstance.location in app.listGoodTiles:
                app.tileInstance.good(app)

            elif app.tileInstance.location in app.listBadTiles:
                app.tileInstance.bad(app)

            elif app.tileInstance.location in app.listStoreTiles:
                app.tileInstance.store(app)

            else:
                if app.tileInstance.item =="item1":
                    app.caughtRoaches = True 
                    app.currentChar.money -=100
                    app.tileInstance.item =None
                    app.boughtTileList.remove(app.tileInstance.location)

                if app.tileInstance.item =="item2":
                    app.caughtUSB = True 
                    app.currentChar.money -=120
                    app.tileInstance.item =None
                    app.boughtTileList.remove(app.tileInstance.location)

                if app.tileInstance.item =="item3":
                    app.caughtFood = True 
                    app.currentChar.money -=150
                    app.tileInstance.item =None
                    app.boughtTileList.remove(app.tileInstance.location)

                app.endTurn = True 
            app.routeState=False
            app.actionState =True
       

def game_redrawAll(app):
    #timer
    drawImage(app.greyBox, 750, 820, width = 100, height = 58)
    drawLabel(f'{app.counter1}{app.counter2}:{app.counter3}{app.counter4}', 800,850, size=25, font='monospace')
    drawLabel('Green spaces are property tiles', 220,750, size=15, font='monospace', bold = True, fill = 'darkgray')
    drawLabel('Blue spaces are special tiles', 220,775, size=15, font='monospace', bold = True, fill = 'darkgray')
    drawLabel('Press r at any point to restart game', 220,800, size=15, font='monospace', bold = True, fill = 'darkgray')

    #board
    drawRect(0, 0, app.width, app.height, fill = "bisque", opacity = 35)
    drawCurrentMove(app)
    drawBoard(app)
    drawImages(app)
    drawPickAgain(app)
    drawPickChar(app)
    drawPropTiles(app)
    drawStoreTiles(app)
    drawBadGoodTiles(app)
    
    #dice
    if app.diceState == True:
        app.rollDice.draw(app)
    if app.diceRollComplete==True:
        if app.dice1==1:
            drawImage(app.dice1Image, 1200, 750, width = 50, height= 50)
        elif app.dice1==2:
            drawImage(app.dice2Image, 1200, 750, width = 50, height= 50)
        elif app.dice1==3:
            drawImage(app.dice3Image, 1200, 750, width = 50, height= 50)
        elif app.dice1==4:
            drawImage(app.dice4Image, 1200, 750, width = 50, height= 50)
        elif app.dice1==5:
            drawImage(app.dice5Image, 1200, 750, width = 50, height= 50)
        elif app.dice1==6:
            drawImage(app.dice6Image, 1200, 750, width = 50, height= 50)

        if app.dice2==1:
            drawImage(app.dice1Image, 1300, 750, width = 50, height= 50)
        elif app.dice2==2:
            drawImage(app.dice2Image, 1300, 750, width = 50, height= 50)
        elif app.dice2==3:
            drawImage(app.dice3Image, 1300, 750, width = 50, height= 50)
        elif app.dice2==4:
            drawImage(app.dice4Image, 1300, 750, width = 50, height= 50)
        elif app.dice2==5:
            drawImage(app.dice5Image, 1300, 750, width = 50, height= 50)
        elif app.dice2==6:
            drawImage(app.dice6Image, 1300, 750, width = 50, height= 50)
    
        
    if app.endTurn == True:
        app.endTurnBut.draw(app)
        

    #drawChar
    for x in range(len(app.charList)):
        app.charList[x].draw(app)
       

    if app.buyMessage == True:
        app.tileInstance.drawBuy(app)
    if app.payMessage == True:
        app.tileInstance.drawPay(app)

    if app.routeState==True:
        drawLabel('Dots indicate all possible tile positions.', app.width/2,200, size=15, font='monospace', bold = True, fill = 'darkgray')
        drawPath(app)
 

    #tilemessages
    drawGoodMessage(app)
    drawBadMessage(app)
    drawStoreMessage(app)

    #store buying
    if app.outStore==True:
        drawLabel("Choose item position by clicking a grey tile", 252, 200, fill ='darkgray', font= 'monospace', size = 15, bold= True)
        drawLabel("Press y to confirm item position",198, 240, fill ='darkgray', font= 'monospace', size = 15, bold= True)
        drawLabel("Press s to return to store",170, 280, fill ='darkgray', font= 'monospace', size = 15, bold= True)

    if app.drawItem1== True and app.outStore ==True:
        x, y = app.choosenTile.topCoord
        drawImage(app.fishing, x-5, y, width = 25, height = 25)

    if app.caughtRoaches == True:
        drawLabel("You had to pay for roach extermination! You lose $100!", 200, 300)
   
    for tile in app.tileList:
        if tile.item =='item1':
            x, y = tile.topCoord
            drawImage (app.fishing, x-5, y, width = 20, height = 20)

    if app.drawItem2== True and app.outStore ==True:
        x, y = app.choosenTile.topCoord
        drawImage(app.usb, x-10, y, width = 35, height = 35)
    
    if app.caughtUSB == True:
       drawLabel("You fell for a USB scam! You lose $120!", 200, 300)
   
    for tile in app.tileList:
        if tile.item =='item2':
            x, y = tile.topCoord
            drawImage (app.usb, x-10, y, width = 35, height = 35)

    if app.drawItem3== True and app.outStore ==True:
        x, y = app.choosenTile.topCoord
        drawImage (app.food, x-10, y, width = 35, height = 35)
    
    if app.caughtFood == True:
       drawLabel("You got food poisoning! You lose $160!", 200, 300)
   
    for tile in app.tileList:
        if tile.item =='item3':
            x, y = tile.topCoord
            drawImage (app.food, x-10, y, width = 35, height = 35)
    
def drawStoreTiles(app):
    for x in app.tileList:
        if x.location in app.listStoreTiles:
            x.drawStore(app)

def drawPropTiles(app):
    for x in app.tileList:
        if x.location in app.listPropTiles:
            x.draw(app)

def drawBadGoodTiles(app):
    for x in app.tileList:
        if x.location in app.listBadTiles or x.location in app.listGoodTiles:
            x.drawBadGood(app)


def drawImages(app):
    #tiles
    cellWidth, cellHeight = getCellSize(app)
    for tile in app.tileList:
        x, y = tile.topCoord
        leftX = x-75
        leftY = y-7
        drawImage(app.boardTile, leftX, leftY, width= 135, height =60, rotateAngle= -0.5)
    
    #character info
    for x in app.charList:
        x.drawInfo(app)
   
#drawing different messages------------------------------------------------------

def drawStoreMessage(app):
    widthh = 400
    heightt = 250
    if app.storeMessage== True:
        drawImage(app.pinkBox, app.width/2- widthh/2 , app.height/2 - heightt/2-80, width = widthh, height = heightt+83)
        drawImage(app.fishing, app.width/2- widthh/2+20, app.height/2 - heightt/2+15, width =50, height= 50)
        drawLabel("Press 1 to buy roaches                    $20", app.width/2- widthh/2+230, app.height/2 - heightt/2+15, fill = "maroon", size = 15, bold = True)
        drawLabel("Whoever lands on it has roaches releases into their", app.width/2- widthh/2+240, app.height/2 - heightt/2+33, fill = "maroon", size = 12,  bold = True)
        drawLabel("dorm and loses $100", app.width/2- widthh/2+152, app.height/2 - heightt/2+48, fill = "maroon", size = 12, bold = True)


        drawImage(app.usb, app.width/2- widthh/2+20, app.height/2 - heightt/2+80, width =50, height= 50)
        drawLabel("Press 2 to buy scam USBs                 $30", app.width/2- widthh/2+235, app.height/2 - heightt/2+85, fill = "maroon", size = 15, bold = True)
        drawLabel("Whoever lands on it has all their computer data", app.width/2- widthh/2+225, app.height/2 - heightt/2+103, fill = "maroon", size = 12,  bold = True)
        drawLabel("stolen and loses $120", app.width/2- widthh/2+152, app.height/2 - heightt/2+121, fill = "maroon", size = 12, bold = True)


        drawImage(app.food, app.width/2- widthh/2+20, app.height/2 - heightt/2+155, width =50, height= 50)
        drawLabel("Press 3 to buy bad food.                 $40", app.width/2- widthh/2+225, app.height/2 - heightt/2+158, fill = "maroon", size = 15, bold = True)
        drawLabel("Whoever lands on it inevitably develops food   ", app.width/2- widthh/2+225, app.height/2 - heightt/2+176, fill = "maroon", size = 12,  bold = True)
        drawLabel("poisoning and loses $160",  app.width/2- widthh/2+163, app.height/2 - heightt/2+194, fill = "maroon", size = 12,  bold = True)

        drawLabel("Press e to exit store", app.width/2- widthh/2+220, app.height/2 - heightt/2+220, fill = "maroon", size = 15,  bold = True)

        drawImage(app.logo, app.width/2- widthh/2+130 , app.height/2 - heightt/2-70, width = 140, height = 70)



def drawBadMessage(app):
    width = 370 
    height = 200
    x, y = 720, 335
    color = app.currentChar.color
    if app.badMessage1 ==True:
        drawImage(app.greyBox, app.width/2- width/2 , app.height/2 - height/2-50, width = width, height = height)
        drawLabel("Oh no!", x, y, font='monospace', size=25, bold = True, fill = "white")
        drawLabel("You were caught in a ", x, y+40, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("phising scheme. You lose $50", x, y+70, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("Press c to continue", x, y+120, font='monospace', size=20, bold = True, fill = color)
        

    elif app.badMessage2 ==True:
        drawImage(app.greyBox, app.width/2- width/2 , app.height/2 - height/2-50, width = width, height = height)
        drawLabel("Oh no!", x, y, font='monospace', size=25, bold = True, fill = "white")
        drawLabel("You lost your student ID. ", x, y+20, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("You lose $50 because", x, y+70, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("you overpaid by $20 ", x, y+100, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("Press c to continue", x, y+130, font='monospace', size=20, bold = True, fill = color)
        
    
    
    elif app.badMessage3 ==True:
        drawImage(app.greyBox, app.width/2- width/2 , app.height/2 - height/2-50, width = width+25, height = height-25)
        drawLabel("Oh no!", x, y, font='monospace', size=25, bold = True, fill = "white")
        drawLabel("Vending machines are broken.", x, y+20, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("You lose $50 because ", x, y+70, font='monospace', size=18, bold = True, fill = "White")
        drawLabel("you wouldn't give up ", x, y+100, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("Press c to continue", x+10, y+130, font='monospace', size=20, bold = True, fill = color)
        
    

def drawGoodMessage(app):
    width = 370 
    height = 200
    x, y = 720, 335
    color = app.currentChar.color
    if app.goodMessage1 ==True:
        drawImage(app.greyBox, app.width/2- width/2 , app.height/2 - height/2-50, width = width, height = height)
        drawLabel("Congrats!", x, y, font='monospace', size=25, bold = True, fill = "white")
        drawLabel("You completed the", x, y+40, font='monospace', size=20, bold = True, fill = "White")
        drawLabel(" Tartan Voices Survey", x, y+70, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("Press c to collect $50", x, y+120, font='monospace', size=20, bold = True, fill = color)


    elif app.goodMessage2 ==True:
        drawImage(app.greyBox, app.width/2- width/2 , app.height/2 - height/2-50, width = width, height = height)
        drawLabel("Congrats!", x, y, font='monospace', size=25, bold = True, fill = "white")
        drawLabel("You found $50 on the ground", x, y+50, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("Press c to collect $50", x, y+120, font='monospace', size=20, bold = True, fill = color)
    
    
    elif app.goodMessage3 ==True:
        drawImage(app.greyBox, app.width/2- width/2 , app.height/2 - height/2-50, width = width+25, height = height-25)
        drawLabel("Congrats!", x, y, font='monospace', size=25, bold = True, fill = "white")
        drawLabel("112 homework was a piece of cake", x+10, y+50, font='monospace', size=20, bold = True, fill = "White")
        drawLabel("Press c to collect $50", x+10, y+120, font='monospace', size=20, bold = True, fill = color)

def drawCurrentMove(app): 
    drawImage(app.greyBox, 45, 820, width = 650, height = 58)
    drawLabel(f"{app.currentChar.name}'s TURN", 200,850, font='monospace', size=25, bold = True, fill = app.currentChar.color)

    if app.diceState== True:
        drawLabel("ROLL DICE", 550, 850, font='monospace', size=25, bold = True, fill = 'grey')
    if app.routeState== True:
        drawLabel("PICK ROUTE", 550, 850, font='monospace', size=25, bold = True, fill = 'grey')
    if app.actionState== True:
        drawLabel("RESOLVE ACTION", 550, 850, font='monospace', size=25, bold = True, fill = 'grey')

def drawPickChar(app):
    if app.messagePickChar!=None:
        drawLabel(f'{app.messagePickChar}', 250, 80, size=16)
   

def drawPickAgain(app):
    if app.pickAgainMessage!= None:
        drawLabel(app.pickAgainMessage, app.width/2, 200, fill ='darkgray', font= 'monospace', size = 15, bold= True)



#path finding
def drawPath(app):
    for (x,y) in app.finalSet:
        drawCellDot(app, x, y, 5, app.currentChar.color)

def pathFindList(app):
    app.finalSet = set(pathFinder(app))
    
def pathFinder(app):
    currentX, currentY = app.currentChar.location
    return pathFindSolve(app, currentX, currentY, 0, [])

def pathFindSolve(app, currentX, currentY, count, result):
    if count==app.diceTotal:
    #if count==15:
   

        result.append((currentX, currentY))
        return result

    else:
        if legalMoveUp(app, currentX-1, currentY) and legalMoveRight(app, currentX, currentY+1) and legalMoveDown(app, currentX+1, currentY):
            return pathFindSolve(app, currentX-1, currentY, count+1, result) + pathFindSolve(app, currentX, currentY+1, count+1, result) + pathFindSolve(app, currentX+1, currentY, count+1, result)
        
        elif legalMoveRight(app, currentX, currentY+1) and legalMoveDown(app, currentX+1, currentY):
            return pathFindSolve(app, currentX, currentY+1, count+1, result) + pathFindSolve(app, currentX+1, currentY, count+1, result)
       
        elif legalMoveLeft(app, currentX, currentY-1) and legalMoveDown(app, currentX+1, currentY):
            return pathFindSolve(app, currentX, currentY-1, count+1, result) + pathFindSolve(app, currentX+1, currentY, count+1, result)


        elif legalMoveUp(app, currentX-1, currentY): #move up
            return pathFindSolve(app, currentX-1, currentY, count+1, result)

        elif legalMoveRight(app, currentX, currentY+1): #move right
            return pathFindSolve(app, currentX, currentY+1, count+1, result)

        elif legalMoveDown(app, currentX+1, currentY): #move down
  
        
            return pathFindSolve(app, currentX+1, currentY, count+1, result)

        elif legalMoveLeft(app, currentX, currentY-1): #move left 
            return pathFindSolve(app, currentX, currentY-1, count+1, result)

def legalMoveUp(app, currentX, currentY):
    if currentX < 0 or currentX > 9 or currentY<0 or currentY>9: #off the board
        return False 
    if (currentX, currentY) not in app.dictt[(currentX+1, currentY)]: #check for node connection
        return False 
    else: 
        return True 

def legalMoveRight(app, currentX, currentY):
    if currentX<0 or currentX> 9 or currentY<0 or currentY>9: #off the board
        return False 
    if (currentX, currentY) not in app.dictt[(currentX, currentY-1)]: #check for node connection
        return False 
    else:
        return True 

def legalMoveDown(app, currentX, currentY):
    if currentX<0 or currentX> 9 or currentY<0 or currentY>9: #off the board
        return False 
    if (currentX, currentY) not in app.dictt[(currentX-1, currentY)]: #check for node connection
        return False 
    else: return True 

def legalMoveLeft(app, currentX, currentY):
    if currentX<0 or currentX> 9 or currentY<0 or currentY>9: #off the board
        return False 
    if (currentX, currentY) not in app.dictt[(currentX, currentY+1)]: #check for node connection
        return False 
    else: return True 


def drawCellDot(app,row,col,r, color):
    topX, topY = getTopCoor(app, row, col)
    drawCircle (topX, topY+20, 5, fill = color)

def drawBoard(app):
    for x in range(len(app.boardCells)):
        (row,col) = app.boardCells[x]
        drawCell(app, row, col, x)

def getTopCoor( app, row, col):
    changeX = 23
    cellWidth, cellHeight = getCellSize(app)
    startX = app.boardLeft - (cellWidth)*row
    startY = app.boardTop + (cellHeight-changeX)*row
    topX, topY = getCellTop(app, row, col, startX, startY, cellWidth, cellHeight, changeX)
    return topX, topY

def getCellTop (app, row, col, startX, startY, cellWidth, cellHeight, changeX):
    x= startX + col *cellWidth 
    y= startY + col * changeX
    return x,y 

def drawCell(app, row, col, index):
    changeX = 23
    topX, topY = getTopCoor(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    #drawCircle (topX, topY, 5, fill = "red")
    cellBottomX, cellBottomY= topX, topY + cellHeight
    cellRightX, cellRightY= topX+cellWidth, topY+ changeX
    cellLeftX, cellLeftY = topX - cellWidth, topY + (cellHeight-changeX)

    label = app.tilePrice[index]
    
    drawPolygon(topX, topY, cellLeftX, cellLeftY, cellBottomX, cellBottomY, cellRightX, cellRightY, 
            fill=None, border='black',
             borderWidth=app.cellBorderWidth)

    #drawLabel(f'{label}',cellLeft+cellWidth/2,cellTop+cellHeight/2)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def getCellIndex(app, mouseX, mouseY):
    cellWidth, cellHeight = getCellSize(app)
    radius = cellHeight/2 - 5
    for x in app.tileList:
        topX, topY = x.topCoord
        
        centerX, centerY = topX, topY+cellHeight/2
        
        dist = distance(centerX, centerY, mouseX, mouseY)
      
        if dist <= radius:
            return x.location
        else: 
            None

def distance(x1, y1, x2, y2):
    changeY= abs(y2-y1)
    changeX = abs(x2-x1)
    return (changeY**2+changeX**2)**0.5



#start screen
def start_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = "bisque", opacity = 35)
    drawImage(app.titlee,  450, 200, width =500, height = 350)

    if app.player1Input == True:
        drawImage(app.greyBox, app.width/2-app.widthPlayerBox/2, 720, width = app.widthPlayerBox, height = app.heightPlayerBox)
        drawLabel("Player 1's name. Press enter to continue. ", 700, 700, font='monospace', size=20, bold = True, fill = "darkgray")
        drawLabel(f'{app.playerName1}', 730, 750, font='monospace', size=25, bold = True, fill = "darkgray")

    elif app.player2Input == True:
        drawImage(app.greyBox, app.width/2-app.widthPlayerBox/2, 720, width = app.widthPlayerBox, height = app.heightPlayerBox)
        drawLabel("Player 2's name. Press enter to continue", 700, 700, font='monospace', size=20, bold = True, fill = "darkgray")
        drawLabel(f'{app.playerName2}', 730, 750, font='monospace', size=25, bold = True, fill = "darkgray")
        
    elif app.player3Input == True:
        drawImage(app.greyBox, app.width/2-app.widthPlayerBox/2, 720, width = app.widthPlayerBox, height = app.heightPlayerBox)
        drawLabel("Player 3's name. Press enter to continue", 700, 700, font='monospace', size=20, bold = True, fill = "darkgray")
        drawLabel(f'{app.playerName3}', 730, 750, font='monospace', size=25, bold = True, fill = "darkgray")
        

        

    else:
        drawImage(app.greyBox, app.width/2-app.widthPlayerBox1/2, 720, width = app.widthPlayerBox1, height = app.heightPlayerBox1)
        drawLabel("PLAY", app.width/2-app.widthPlayerBox1/2+50, 745, font='monospace', size=25, bold = True, fill = "darkgray")
        


def start_onMouseMove(app, mouseX, mouseY):

    if mouseX<= app.width/2-app.widthPlayerBox1/2+app.widthPlayerBox1 and mouseX>=  app.width/2-app.widthPlayerBox1/2 and mouseY<= 778 and mouseY>= 720:
        app.widthPlayerBox1 = 110
        app.heightPlayerBox1 = 68
        
    else:
        app.widthPlayerBox1 =100
        app.heightPlayerBox1 =58
        

def start_onMousePress(app, mouseX, mouseY):
    if app.startButton== True:
        if mouseX<= app.width/2-app.widthPlayerBox1/2+app.widthPlayerBox1 and mouseX>=  app.width/2-app.widthPlayerBox1/2 and mouseY<= 778 and mouseY>= 720:
            setActiveScreen('game')
            app.startButton= False

def start_onKeyPress(app, key):

    if app.player1Input:
        if key =='backspace':
            app.playerName1= app.playerName1[:-1]
        if key !='enter' and key!='backspace':
            app.playerName1 += key  
        if key == 'enter':
            app.charList[0].name = app.playerName1
            app.player1Input =False
            app.player2Input =True 
        

    elif app.player2Input:
        if key =='backspace':
            app.playerName2= app.playerName2[:-1]

        if key != 'enter':
            app.playerName2 +=key  

        if key == 'enter':
            app.charList[1].name = app.playerName2
            app.player2Input =False
            app.player3Input =True 

    elif app.player3Input:
        if key =='backspace':
            app.playerName3= app.playerName3[:-1]

        if key != 'enter':
            app.playerName3 +=key  

        if key == 'enter':
            app.charList[2].name = app.playerName3
            app.player3Input =False
            app.startButton= True

   

#win screen
def win_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = "bisque", opacity = 35)

    for x in app.charList:
        x.drawInfo(app)
   
  
    charList = copy.copy(app.charList)
    bestChar1= None
    bestMoney1 = 0

    for x in charList:
        currentMoney = x.money
        if currentMoney> bestMoney1:
            bestChar1= f"{x.name}"
            bestMoney1= currentMoney
        elif currentMoney == bestMoney1:
            if isinstance(bestChar1, str): #theres no set yet
                newBestChar1= []
                newBestChar1.append(f"{bestChar1}") #add prev name into new set
                bestChar1=newBestChar1
            bestChar1.append(f"{x.name}") #add current name into new set
    
    #first place:
    if isinstance(bestChar1, str)== False: #multiple winners
        drawLabel("Winners!", app.width/2, app.height/2-100, font= "monospace", bold= True, size= 40, fill = "darkgray")
        for nameIndex in range(len(bestChar1)):
            drawLabel(f"{bestChar1[nameIndex]}",app.width/2-100+ 200*nameIndex, 500, font= "monospace", bold= True, size= 30, fill = "gold")
    else:
        drawLabel("Winner!", app.width/2, app.height/2-100, font= "monospace", bold= True, size= 40, fill = "darkgray")
        drawLabel(f"{bestChar1}",  app.width/2, 450, font= "monospace", bold= True, size= 30, fill = "gold")

def win_onKeyPress(app, key):
    if key == "r":
        restart(app)
        setActiveScreen('start')

    
def main():
    runAppWithScreens(initialScreen='start')
    runApp()

    


main()