#!/usr/bin/env python
# 
# tennis.py -- implementation of a tennis game
#
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tennis_model import Base, Player, Score
import sys

engine = create_engine('sqlite:///tennis.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
#
score_list = {1: "Love", 2: "Fifteen", 3: 'Thirty', 4: "Forty", 5: "Advantage"}


#Code to delete players from the database
def deletePlayers():
    """Remove all the player records from the database."""
    session.query(Player).delete()

def deleteScores():
    """Remove all the score records from the database"""
    session.query(Score).delete()

#Code to get correct score from tennis score name
def getScoreValue(name):
    """Searches through score values for name

    Args:
        name: the tennis appropriate name of the score
    """
    for num, val in score_list.iteritems():
        if val == name:
            return str(num)
    return False

#Code to count all players in the database
def countPlayers():
    """Returns the number of players currently registered.

    Returns:
        count: Integer of how many players are in the database
    """
    return session.query(Player).count()

#Code to regoster a player in the database.
def registerPlayer(name):
    """Adds a player to the tennis database.
  
    Args:
      name: the player's full name (need not be unique).

    Return:
        id: database id row id of the recently created player on success
        string: an error string on failure
    """
    if(countPlayers() < 2):
        newplayer = Player(name = name)
        session.add(newplayer)
        session.commit()
        message = "Player %s's name has been set to %s" % (newplayer.id , name)
        value = {'success': True, 'message': message, 'id': newplayer.id}
    else:
        message = "You can only have two players at a time"
        value = {'success': False, 'message': message}

    return value

#code to set initial score in the database
def setInitialScore(pid, raw_entry):
    """Sets the initial score from the  tennis friendly name

    Args:
        player: the id of the player who is getting their score set
        raw_entry: the tennis friendly name to use to find the score
    """
    tennis = str(raw_entry).title().strip()
    num_score = getScoreValue(tennis)
    if num_score:
        if session.query(Score).filter_by(player_id = pid).first() != None:
            message = "Initial score has already been set for player %s" % pid
            value = {'success': False, 'message': message}
            return value
        newscore = Score(points = num_score, player_id = pid)
        session.add(newscore)
        session.commit()
        message = "Player %s's score has been set to %s" % (pid, tennis)
        value = {'success': True, 'message': message}
        return value
    else:
        message = """The initial score for player %s - (one of Love, Fifteen, 
            Thirty, Forty, Advantage)""" % pid
        value = {'success': False, 'message': message}
        return value

def isInt(s):
    """Rturns whether the value passed in is an integer"""
    try: 
        int(s)
        return True
    except ValueError:
        return False

def getCurrentScore():
    """Returns current scores"""
    players = []
    current_scores = session.query(Score).all()

    for p in current_scores:
        players.append((p.player_id, p.points))

    return players

def reportScore(scorer):
    """Reports the score and returns corresponding message

    Args:
        Scorer: player who scored
    """
    recordScore(scorer)
    score_holder = getCurrentScore()
    [(pid1, pscore1), (pid2, pscore2)] = score_holder
    message = ""

    if pscore1 <= 4 and pscore2 <= 4 and pscore1 != pscore2:
        message = "%s-%s" % (score_list[pscore1], score_list[pscore2])
    elif pscore1 == pscore2:
        message = "Deuce!"
    elif (pscore1 > pscore2 and pscore1 > 4 
        and (pscore2 != 4 or pscore1 > pscore2 + 1)):
        message = "Player %s wins the game!" % pid1
    elif (pscore2 > pscore1 and pscore2 > 4 
        and (pscore1 != 4 or pscore2 > pscore1 + 1)):
        message = "Player %s wins the game!" % pid2
    elif pscore1 > pscore2 and pscore1 > 4 and pscore1 == pscore2 + 1:
        message = "Advantage Player %s!" % pid1
    elif pscore2 > pscore1 and pscore2 > 4 and pscore2 == pscore1 + 1:
        message = "Advantage Player %s!" % pid2

    return message


#Code to eecord outcome of the game
def recordScore(scorer):
    """Records who scored the point this round

    Args:
      scorer:  the id number of the player who got the point
    """
    points = session.query(Score).filter_by(player_id = scorer).first()
    if points != None:
        points.points = points.points + 1
        session.add(points)
        session.commit()
    else:
        return "Couldn't find that user in the database"

#Code Wrapper to get user entry for registerPlayer
def getNameRegister(pid):
    """Code to get user input for registerPlayer function"""
    message = ""

    while True:
        if message:
            print message
        else: 
            print "Please enter player %s's name:" % pid

        choice = raw_input("> ")
        value = registerPlayer(choice)        
        if value['success']:
            print value['message']
            return value['id']
        else:
            message = value['message']

#Code Wrapper to get user entry for setInitialScore
def getInitialScore(pid):
    """"Code to get user input setInitialScore function"""
    message = ""

    while True:
        if message:
            print message
        else:
            print "Enter the inital score for player %s" % pid

        choice = raw_input("> ")
        value = setInitialScore(pid, choice)
        if value['success']:
            print value['message']
            return None
        else:
            message = value['message']


def play_game():
    """Code to play through game"""
    deletePlayers()
    deleteScores()

    p1id = getNameRegister(1)
    p2id = getNameRegister(2)

    getInitialScore(p1id)
    getInitialScore(p2id)

    while True:


play_game()


