# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhost = successorGameState.getGhostPositions()
        

        #we check for each ghost which one is the closest    
        for ghost in newGhost:
            closestGhost = util.manhattanDistance(newPos,ghost)
            if closestGhost < 3:            #if the ghost is close that is bad so return a large negative number
                return -float("inf")
        
        
        foodList = newFood.asList() #get the food as a list
        minimum = float("inf")      #temp variable to be overwritten by the closest food value
        #for each food find the closest one
        for food in foodList:       
            minimum = min(util.manhattanDistance(newPos, food), minimum)


        "*** YOUR CODE HERE ***"
        return successorGameState.getScore() + (1.0/minimum) #return the score plus the reciprical of the minimum

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def maximum(self, gameState, actions, agentIndex, depth):
        tempMax = ("max", -float("inf"))   
        agentIndex = agentIndex + 1
        #check to see if we are out of hte bounds of our agent indexes
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
        #print("agent #{} -- actions {}".format(agentIndex, actions))

        #for each action find the greatest value
        for action in actions:    
            tempSuc = (action, self.minmax(depth + 1, gameState.generateSuccessor(agentIndex - 1, action), agentIndex)) #minmax gets cost from successor recursivly
            if tempMax[1] <= tempSuc[1]:
                tempMax = tempSuc
        return tempMax  #return the maximum cost action as a tuple (action, cost)



    def minimum(self, gameState, actions, agentIndex, depth):
        tempMin = ("min" ,float("inf")) 
        agentIndex = agentIndex + 1
        #check to see if we are out of the bounds of our agents
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0 
        #print("agent #{} -- actions {}".format(agentIndex, actions))
        #check for each action what has the lowest cost then we will return that value
        for action in actions:
            tempSuc = (action, self.minmax(depth + 1, gameState.generateSuccessor(agentIndex - 1, action), agentIndex))
            if tempMin[1] >= tempSuc[1]:
                tempMin = tempSuc
            #print(tempSuc[1])
        return tempMin      #Return lowest cost action as a tuple (action, cost)



    def minmax(self, depth, gameState, agentIndex):
        if gameState.isLose() or gameState.isWin() or (depth >= self.depth * gameState.getNumAgents()): #check first if we have won or lost or 
            return self.evaluationFunction(gameState)
        if agentIndex == 0:                                                                             #check if we are minmaxing for pacman 
            #print("Max -- depth: {}, agent index: {}".format(depth, agentIndex));
            return self.maximum(gameState, gameState.getLegalActions(0), 0, depth)[1]                   #Pacman has an agent value of 0 ########################!!!
                                                                                                        
        else:                                                                                           #or for one of the ghosts
            #print("min -- depth: {}, agent index: {}".format(depth, agentIndex));
            return self.minimum(gameState, gameState.getLegalActions(agentIndex), agentIndex, depth)[1]#
        






    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #return self.minmax(0, gameState, 0)[0]
        return self.maximum(gameState, gameState.getLegalActions(0), 0, 0)[0]       # The first agent is pacman so, we pass the maximum function as a return
                                                                                    # then the maximum function will call minmax.
    


        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def maximum(self, gameState, actions, agentIndex, depth, alpha, beta):
        tempMax = ("max", -float("inf"))   
        agentIndex = agentIndex + 1
        #check to see if we are out of hte bounds of our agent indexes
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
        #print("agent #{} -- actions {}".format(agentIndex, actions))

        #for each action find the greatest value
        for action in actions:    
            tempSuc = (action, self.alphaBeta(depth + 1, gameState.generateSuccessor(agentIndex - 1, action), agentIndex, alpha, beta)) #minmax gets cost from successor recursivly
            if tempMax[1] <= tempSuc[1]:
                tempMax = tempSuc
            if alpha < tempMax[1]:
                alpha = tempMax[1]
            if tempMax[1] > beta:
                return tempMax

        
        
        return tempMax  #return the maximum cost action as a tuple (action, cost)



    def minimum(self, gameState, actions, agentIndex, depth, alpha, beta):
        tempMin = ("min" ,float("inf")) 
        agentIndex = agentIndex + 1
        #check to see if we are out of the bounds of our agents
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0 
        #print("agent #{} -- actions {}".format(agentIndex, actions))
        #check for each action what has the lowest cost then we will return that value
        for action in actions:
            tempSuc = (action, self.alphaBeta(depth + 1, gameState.generateSuccessor(agentIndex - 1, action), agentIndex, alpha, beta))
            if tempMin[1] >= tempSuc[1]:
                tempMin = tempSuc
            if beta > tempMin[1]:
                beta = tempMin[1]
            if tempMin[1] < alpha:
                return tempMin
            
            #print(tempSuc[1])

        
        
        return tempMin      #Return lowest cost action as a tuple (action, cost)





    def alphaBeta(self, depth, gameState, agentIndex, alpha, beta):
        if gameState.isLose() or gameState.isWin() or (depth >= self.depth * gameState.getNumAgents()): #check first if we have won or lost or 
            return self.evaluationFunction(gameState)
        if agentIndex == 0:                                                                             #check if we are minmaxing for pacman 
            #print("Max -- depth: {}, agent index: {}".format(depth, agentIndex));
            return self.maximum(gameState, gameState.getLegalActions(0), 0, depth, alpha, beta)[1]      #Pacman has an agent value of 0                                           
        else:                                                                                           #or for one of the ghosts
            #print("min -- depth: {}, agent index: {}".format(depth, agentIndex));
            return self.minimum(gameState, gameState.getLegalActions(agentIndex), agentIndex, depth, alpha, beta)[1]#
        




    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        return self.maximum(gameState, gameState.getLegalActions(0), 0, 0, -float("inf"), float("inf"))[0]























class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maximum(self, gameState, actions, agentIndex, depth):
        tempMax = ("max",-float("inf"))   
        agentIndex = agentIndex + 1
        #check to see if we are out of hte bounds of our agent indexes
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
        #print("agent #{} -- actions {}".format(agentIndex, actions))

        #for each action find the greatest value
        for action in actions:    
            tempSuc = self.expectimax(depth + 1, gameState.generateSuccessor(agentIndex - 1, action), agentIndex, action) #minmax gets cost from successor recursivly
            if tempMax[1] <= tempSuc[1]:
                tempMax = (action, tempSuc[1])
        return tempMax  #return the maximum cost action as a tuple (action, cost)


    def average(self, gameState, actions, agentIndex, depth):
        avg = 0
        children = 0
        act = "a"
        agentIndex = agentIndex + 1
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
        for action in actions:
            avg = avg + self.expectimax(depth + 1, gameState.generateSuccessor(agentIndex - 1, action), agentIndex, action)[1]
            children = children + 1
        avg = float(avg) / float(children)
        return (act, avg)
    

    def expectimax(self, depth, gameState, agentIndex, action):
        if gameState.isWin() or gameState.isLose() or (depth >= self.depth * gameState.getNumAgents()):
            return (action, self.evaluationFunction(gameState))
        if agentIndex == 0:
            return self.maximum(gameState, gameState.getLegalActions(0), 0, depth)
        else: 
            return self.average(gameState, gameState.getLegalActions(agentIndex), agentIndex, depth)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        return self.expectimax(0, gameState, 0,gameState.getLegalActions(0))[0]
        #return self.maximum(gameState, gameState.getLegalActions(0), 0, 0)[0]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newGhost = currentGameState.getGhostPositions()
        

    #we check for each ghost which one is the closest    
    for ghost in newGhost:
        closestGhost = util.manhattanDistance(newPos,ghost)
        if closestGhost < 2:            #if the ghost is close that is bad so return a large negative number
            return -float("inf")
        
        
    foodList = newFood.asList() #get the food as a list
    minimum = float("inf")      #temp variable to be overwritten by the closest food value
    #for each food find the closest one
    for food in foodList:       
        minimum = min(util.manhattanDistance(newPos, food), minimum)


    "*** YOUR CODE HERE ***"
    return currentGameState.getScore() + (1.0/minimum)*10 + (1.0/closestGhost)*100 #return the score plus the reciprical of the minimum    
    
# Abbreviation
better = betterEvaluationFunction
