#!/usr/bin/env python
#
# Test cases for tennis.py

from tennis import *

def testDelete():
    deletePlayers()
    deleteScores()
    print "1. Player records can be deleted."


def testCount():
    deletePlayers()
    deleteScores()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "2. After deleting, countPlayers() returns zero."


def testRegister():
    deletePlayers()
    deleteScores()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "3. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deletePlayers()
    deleteScores()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    errorMessage = registerPlayer("Batman")
    if not errorMessage:
        raise ValueError("Should not be able to add three players.")
    c = countPlayers()
    if c != 2:
        raise ValueError(
            "After registering two players, countPlayers should be 2.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "4. Players can be registered and deleted."

def testInitialScoreSet():
    deletePlayers()
    deleteScores()
    registerPlayer("Chucky")
    string = setInitialScore(1, "And")
    if (string != """The initial score for player 1 - (one of Love, Fifteen, 
            Thirty, Forty, Advantage)"""):
        raise ValueError("Should recive an error on wrong entry")
    string = setInitialScore(1, "Love")
    if string != "Player %s's score has been set to %s" % (1, "Love"):
        raise ValueError(string)
    print "5. Can set inital scores for players"


def testGame():
    deletePlayers()
    deleteScores()
    player1_id = registerPlayer("Twilight Sparkle")
    player2_id = registerPlayer("Fluttershy")
    setInitialScore(player1_id, "Thirty")
    setInitialScore(player2_id, "Fifteen")
    scoreHolder = getCurrentScore()
    [(pid1, pscore1), (pid2, pscore2)] = scoreHolder
    if(reportScore(pid1) != "Forty-Fifteen"):
        raise ValueError("Wrong score message returned")

    reportScore(pid2)
    if(reportScore(pid2) != "Deuce!"):
        raise ValueError("Scores should be tied!")
    if(reportScore(pid2) != "Advantage Player 2!"):
        raise ValueError("Player 2 should have the advantage!")
    if(reportScore(pid2) != "Player 2 wins the game!"):
        raise ValueError("Player 2 should have won the game!")
    
    print "6. Game code can be used successfully."


if __name__ == '__main__':
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testInitialScoreSet()
    testGame()
    print "Success!  All tests pass!"


