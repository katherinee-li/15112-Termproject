"""Regression tests for the game logic in finalProject.py.

Run with: python3 -m unittest discover -s tests
"""
import os
import sys
import types
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stubs import installStubs

installStubs()

import finalProject as game


def makeApp():
    app = types.SimpleNamespace(width=1440, height=900)
    game.restart(app)
    return app


class BoardDataTest(unittest.TestCase):
    def testEveryCellHasAPrice(self):
        app = makeApp()
        self.assertEqual(len(app.boardCells), len(app.tilePrice))
        self.assertEqual(len(app.tileList), len(app.boardCells))

    def testPathGraphOnlyUsesBoardCells(self):
        app = makeApp()
        for node, neighbors in app.dictt.items():
            self.assertIn(node, app.boardCells)
            for neighbor in neighbors:
                self.assertIn(neighbor, app.boardCells)

    def testSpecialTilesAreOnTheBoard(self):
        app = makeApp()
        for tileList in (app.listPropTiles, app.listGoodTiles,
                         app.listBadTiles, app.listStoreTiles):
            for location in tileList:
                self.assertIn(location, app.boardCells)


class LoadImageTest(unittest.TestCase):
    def testMissingAssetFallsBackInsteadOfCrashing(self):
        self.assertIsNotNone(game.loadImage('thisFileDoesNotExist.png'))

    def testAssetsAreResolvedRelativeToTheSourceFile(self):
        cwd = os.getcwd()
        try:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            self.assertIsNotNone(game.loadImage('tile.png'))
        finally:
            os.chdir(cwd)


class LegalMoveTest(unittest.TestCase):
    def setUp(self):
        self.app = makeApp()

    def testOffBoardMovesAreIllegal(self):
        self.assertFalse(game.legalMoveUp(self.app, -1, 5))
        self.assertFalse(game.legalMoveDown(self.app, 10, 5))
        self.assertFalse(game.legalMoveLeft(self.app, 5, -1))
        self.assertFalse(game.legalMoveRight(self.app, 5, 10))

    def testUnconnectedNodesDoNotRaise(self):
        #(4,1) is not a board cell, so no graph entry exists for its neighbors
        self.assertFalse(game.legalMoveUp(self.app, 4, 1))
        self.assertFalse(game.legalMoveRight(self.app, 4, 1))
        self.assertFalse(game.legalMoveDown(self.app, 4, 1))
        self.assertFalse(game.legalMoveLeft(self.app, 4, 1))

    def testConnectedMoveIsLegal(self):
        #(2,0) -> (2,1) is an edge in the board graph
        self.assertTrue(game.legalMoveRight(self.app, 2, 1))


class PathFindingTest(unittest.TestCase):
    def setUp(self):
        self.app = makeApp()

    def testSingleStepFromStart(self):
        self.app.diceTotal = 1
        self.app.currentChar.location = (2, 0)
        game.pathFindList(self.app)
        self.assertEqual(self.app.finalSet, {(2, 1)})

    def testDestinationsAreAlwaysBoardCells(self):
        for total in range(2, 13):
            self.app.diceTotal = total
            self.app.currentChar.location = (2, 0)
            game.pathFindList(self.app)
            self.assertNotEqual(self.app.finalSet, set())
            for cell in self.app.finalSet:
                self.assertIn(cell, self.app.boardCells)

    def testBranchingKeepsEveryReachableDestination(self):
        #(2,5) branches up to (1,5), down to (3,5) and right to (2,6)
        self.app.diceTotal = 1
        self.app.currentChar.location = (2, 5)
        game.pathFindList(self.app)
        self.assertEqual(self.app.finalSet, {(1, 5), (3, 5), (2, 6)})

    def testWalkingEveryBoardCellNeverRaises(self):
        for cell in self.app.boardCells:
            self.app.currentChar.location = cell
            self.app.diceTotal = 6
            game.pathFindList(self.app)
            self.assertTrue(len(self.app.finalSet) >= 1)


class RentTest(unittest.TestCase):
    def setUp(self):
        self.app = makeApp()
        self.tile = self.app.tileList[0]
        self.tile.price = 300

    def testUnownedTileOffersAPurchase(self):
        self.tile.prop(self.app)
        self.assertTrue(self.app.buyMessage)
        self.assertFalse(self.app.payMessage)

    def testRentMovesMoneyFromVisitorToOwner(self):
        owner = self.app.charList[1]
        owner.prop.append(self.tile)
        self.tile.state = True
        visitor = self.app.currentChar
        visitorMoney, ownerMoney = visitor.money, owner.money

        self.tile.prop(self.app)

        self.assertEqual(visitor.money, visitorMoney - 30)
        self.assertEqual(owner.money, ownerMoney + 30)
        self.assertTrue(self.app.payMessage)

    def testOwnerDoesNotPayRentOnOwnTile(self):
        owner = self.app.currentChar
        owner.prop.append(self.tile)
        self.tile.state = True
        ownerMoney = owner.money

        self.tile.prop(self.app)

        self.assertEqual(owner.money, ownerMoney)
        self.assertFalse(self.app.payMessage)


class BuyingTest(unittest.TestCase):
    def setUp(self):
        self.app = makeApp()
        self.tile = self.app.tileList[0]
        self.tile.price = 300

    def testBuyDeductsPriceAndRecordsProperty(self):
        char = self.app.currentChar
        money = char.money
        char.buy(self.tile)
        self.assertEqual(char.money, money - 300)
        self.assertIn(self.tile, char.prop)

    def testCannotBuyWithoutEnoughMoney(self):
        char = self.app.currentChar
        char.money = 100
        self.assertFalse(char.canBuy(self.tile))

    def testCannotBuyAnOwnedTile(self):
        self.tile.state = True
        self.assertFalse(self.app.currentChar.canBuy(self.tile))

    def testKeyPressDoesNotAllowOverdraft(self):
        char = self.app.currentChar
        char.money = 100
        self.app.tileInstance = self.tile
        self.app.buyMessage = True

        game.game_onKeyPress(self.app, 'y')

        self.assertEqual(char.money, 100)
        self.assertEqual(char.prop, [])
        self.assertFalse(self.tile.state)


class TurnOrderTest(unittest.TestCase):
    def testTurnsCycleThroughEveryPlayer(self):
        app = makeApp()
        seen = []
        #the fourth player is the computer, whose turn resolves automatically
        for _ in range(len(app.charList) - 1):
            seen.append(app.currentCharIndex)
            game.endTurnFunc(app)
        self.assertEqual(seen, [0, 1, 2])
        self.assertEqual(app.currentCharIndex, 0)

    def testEndTurnClearsMessages(self):
        app = makeApp()
        app.goodMessage1 = app.badMessage2 = app.storeMessage = True
        app.buyMessage = app.payMessage = True
        game.endTurnFunc(app)
        for flag in (app.goodMessage1, app.badMessage2, app.storeMessage,
                     app.buyMessage, app.payMessage):
            self.assertFalse(flag)


class WinnerTest(unittest.TestCase):
    def makeChars(self, amounts):
        return [types.SimpleNamespace(name=f'p{i}', money=money)
                for i, money in enumerate(amounts)]

    def testSingleWinner(self):
        self.assertEqual(game.getWinners(self.makeChars([10, 50, 20])), ['p1'])

    def testTiedWinners(self):
        self.assertEqual(game.getWinners(self.makeChars([50, 50, 20])),
                         ['p0', 'p1'])

    def testAllPlayersInDebtStillHasAWinner(self):
        self.assertEqual(game.getWinners(self.makeChars([-100, -50, -300])),
                         ['p1'])

    def testNoPlayers(self):
        self.assertEqual(game.getWinners([]), [])


class NameEntryTest(unittest.TestCase):
    def setUp(self):
        self.app = makeApp()

    def testBackspaceDeletesInsteadOfTypingItsName(self):
        self.app.player1Input = False
        self.app.player2Input = True
        for key in ('a', 'b', 'backspace'):
            game.start_onKeyPress(self.app, key)
        self.assertEqual(self.app.playerName2, 'a')

    def testEnterStoresTheName(self):
        game.start_onKeyPress(self.app, 'a')
        game.start_onKeyPress(self.app, 'enter')
        self.assertEqual(self.app.playerName1, 'a')
        self.assertEqual(self.app.charList[0].name, 'a')
        self.assertTrue(self.app.player2Input)


class ButtonTest(unittest.TestCase):
    def testPressIsDetectedAcrossTheWholeDrawnButton(self):
        app = makeApp()
        pressed = []
        button = game.Button(100, 200, lambda a: pressed.append(True),
                             'test', app)
        button.press(app, 235, 255)  #inside the 140x58 image
        self.assertEqual(len(pressed), 1)

    def testPressOutsideButtonIsIgnored(self):
        app = makeApp()
        pressed = []
        button = game.Button(100, 200, lambda a: pressed.append(True),
                             'test', app)
        button.press(app, 300, 255)
        button.press(app, 235, 300)
        self.assertEqual(pressed, [])


class ItemCostTest(unittest.TestCase):
    def testBadFoodPenaltyMatchesTheStoreDescription(self):
        app = makeApp()
        tile = app.tileList[0] #(0,5), a normal tile that can hold an item
        tile.item = 'item3'
        app.boughtTileList.append(tile.location)
        app.routeState = True
        app.finalSet = {tile.location}
        char = app.currentChar
        money = char.money

        cellWidth, cellHeight = game.getCellSize(app)
        topX, topY = tile.topCoord
        game.game_onMousePress(app, topX, topY + cellHeight/2)

        self.assertTrue(app.caughtFood)
        #the store advertises a $160 loss for bad food
        self.assertEqual(char.money, money - 160)
        self.assertIsNone(tile.item)
        self.assertNotIn(tile.location, app.boughtTileList)


if __name__ == '__main__':
    unittest.main()
