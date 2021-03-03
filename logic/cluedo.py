'''cluedo.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Adapted to course needs by Laura Brown

Copyright (C) 2008 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import cnf

class Cluedo:
    suspects = ['sc', 'mu', 'wh', 'gr', 'pe', 'pl']
    weapons  = ['kn', 'cs', 're', 'ro', 'pi', 'wr']
    rooms    = ['ha', 'lo', 'di', 'ki', 'ba', 'co', 'bi', 'li', 'st']
    casefile = "cf"
    hands    = suspects + [casefile]
    cards    = suspects + weapons + rooms

    """
    Return ID for player/card pair from player/card indicies
    """
    @staticmethod
    def getIdentifierFromIndicies(hand, card):
        return hand * len(Cluedo.cards) + card + 1

    """
    Return ID for player/card pair from player/card names
    """
    @staticmethod
    def getIdentifierFromNames(hand, card):
        return Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(card))


def deal(hand, cards):
    "Construct the CNF clauses for the given cards being in the specified hand"
    "*** YOUR CODE HERE ***" 
    temp = []
    returnArray = []
    temp.append(Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(cards[0])))
    returnArray.append(temp)   
    temp[0] = Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(cards[1]))
    returnArray.append(temp)
    temp[0] = Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(cards[2]))
    returnArray.append(temp)
    return returnArray

def axiom_card_exists():
    """
    Construct the CNF clauses which represents:
        'Each card is in at least one place'
    """
    "*** YOUR CODE HERE ***"
    retArray  = []
    tempArray = []
    for weapon in Cluedo.weapons:
        for suspect in Cluedo.suspects:
            tempArray.append(Cluedo.getIdentifierFromNames(suspect, weapon))
        tempArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, weapon))
        retArray.append(tempArray)
        tempArray = []
            
    for room in Cluedo.rooms:
        for suspect in Cluedo.suspects:
            tempArray.append(Cluedo.getIdentifierFromNames(suspect,room))
        tempArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, room))
        retArray.append(tempArray)
        tempArray = []

    for sus in Cluedo.suspects:
        for suspect in Cluedo.suspects:
            tempArray.append(Cluedo.getIdentifierFromNames(suspect, sus))
        tempArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, sus))
        retArray.append(tempArray)
        tempArray = []
    

    return retArray

def axiom_card_unique():
    """
    Construct the CNF clauses which represents:
        'If a card is in one place, it can not be in another place'
    """
    "*** YOUR CODE HERE ***"
    retArray  = []
    tempArray = []
    for player in Cluedo.suspects:
        for weapon in Cluedo.weapons:
            tempArray.append(Cluedo.getIdentifierFromNames(player, weapon))
            tempArray.append(-1*Cluedo.getIdentifierFromNames(player, weapon))
            retArray.append(tempArray)
            tempArray = []
        for room in Cluedo.rooms:
            tempArray.append(Cluedo.getIdentifierFromNames(player, room))
            tempArray.append(-1* Cluedo.getIdentifierFromNames(player, room))
            retArray.append(tempArray)
            tempArray = []
        for suspect in Cluedo.suspects:
            tempArray.append(Cluedo.getIdentifierFromNames(player, suspect))
            tempArray.append(-1*Cluedo.getIdentifierFromNames(player, suspect))
            retArray.append(tempArray)
            tempArray = []

    return retArray

def axiom_casefile_exists():
    """
    Construct the CNF clauses which represents:
        'At least one card of each category is in the case file'
    """
    "*** YOUR CODE HERE ***"
    tempArray = []
    retArray  = []
    for room in Cluedo.rooms:
        tempArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, room))
    retArray.append(tempArray)
    tempArray = []

    for weapon in Cluedo.weapons:
        tempArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, weapon))
    retArray.append(tempArray)
    tempArray = []

    for sus in Cluedo.suspects:
        tempArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, sus))
    retArray.append(tempArray)


    return retArray



def axiom_casefile_unique():
    """
    Construct the CNF clauses which represents:
        'No two cards in each category are in the case file'
    """
    "*** YOUR CODE HERE ***"

    tempArray = []
    retArray  = []


    #[[[1,2],[1,2], ...w],[[3,5],[],...r],[[x,t],[],[], ...s]]


    for weapon in Cluedo.weapons:
        tempArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, weapon))
        tempArray.append(-1*Cluedo.getIdentifierFromNames(Cluedo.casefile, weapon))
        retArray.append(tempArray)
        tempArray = []
    for room in Cluedo.rooms:
        tempArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, room))
        tempArray.append(-1* Cluedo.getIdentifierFromNames(Cluedo.casefile, room))
        retArray.append(tempArray)
        tempArray = []
    for suspect in Cluedo.suspects:
        tempArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, suspect))
        tempArray.append(-1*Cluedo.getIdentifierFromNames(Cluedo.casefile, suspect))
        retArray.append(tempArray)
        tempArray = []
    return retArray


def suggest(suggester, card1, card2, card3, refuter, cardShown):
    "Construct the CNF clauses representing facts and/or clauses learned from a suggestion"
    "*** YOUR CODE HERE ***"
    return []

def accuse(accuser, card1, card2, card3, correct):
    "Construct the CNF clauses representing facts and/or clauses learned from an accusation"
    "*** YOUR CODE HERE ***"
    return []
