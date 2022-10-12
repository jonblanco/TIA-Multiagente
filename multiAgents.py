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


from cmath import inf
from hashlib import new
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

        #se ejecuta cada vez que el pacman se mueve
        #por tanto, esto solo nos va a dar el score del siguiente pasito que va a dar
        # entonces hay que hacer un score de como de bien o mal estamos en ese momento
        # basicamente el juego va a tener una serie de opciones a realizar y nosotros vamos
        # a establecer cómo de bueno es el estado en el que vamos a estar si realizamos esa accion (es decir, vamos a ver su utilidad)       
        
        valoracion = 0
        superint = (2**31)-1
        miniint = -(2**31)-1
        distancias_a_comidas =  list()
        distancias_a_fantasmas = list()
        
        #estados finales:

        if successorGameState.isWin():
            return superint
        if successorGameState.isLose():
            return miniint

       
          #distancias a los fantasmas

        posFantasmas = successorGameState.getGhostPositions()
        for fantasmaPos in posFantasmas:
            dist = manhattanDistance(newPos , fantasmaPos)
            distancias_a_fantasmas.append(dist)

        #tenemos que tener en cuenta que cuanto mas cerca
        #estemos de los fantasmas peor es la utilidad, es decir,
        #peor es el estado:

        for dist in distancias_a_fantasmas:
            if dist<=1: #si esta muy cerca
                valoracion = miniint #mala opcion
                return valoracion

       
            
        #distancias a las comidas
        
        for comida in newFood.asList():
            dist = manhattanDistance(newPos, comida)
            distancias_a_comidas.append(dist)
        
        #tenemos que tener en cuenta que cuanto mas cerca
        #estemos de la comida mayor es la utilidad, es decir,
        #mejor es el estado:

        if len(distancias_a_comidas) == 0: #si estan las distancias vacias significaria que ya no hay comidas, es decir
                                            #estariamos en una situacion muy beneficiosa
            valoracion = superint
            return valoracion


        if newPos==currentGameState.getPacmanPosition():
            valoracion=miniint
            return valoracion


        return  currentGameState.getScore() +  99999/len(distancias_a_comidas) + 1/sum(distancias_a_comidas) 
        
  
        

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
        print('Get legal actions pacman: ', gameState.getLegalActions(0))
        print('Get legal actions fantasmas 1: ', gameState.getLegalActions(1))
        print('Get legal actions fantasmas 2: ', gameState.getLegalActions(2))
        print('Get legal actions fantasmas 3: ', gameState.getLegalActions(3))
        print('Get number of agents: ', gameState.getNumAgents())
        print('Is win? ', gameState.isWin())
        print('Is lose? ', gameState.isLose())
        print('\n')
        
        #util.raiseNotDefined()
    
    def maxvalue(self, state):
        max_v = -((2**31)-1) #integer minimo
        for sucesor in state.getSuccessors():
            max_v = max(max_v, self.minvalue(sucesor))
        return max_v

    
    def minvalue(self, state):
        min_v = (2**31)-1
        for sucesor in state.getSuccessors():
            min_v = min(min_v, self.maxvalue(sucesor))
        return min_v


    


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
