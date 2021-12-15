# search.py
# ---------
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

"""
INF8215 - Devoir 1
    Guillaume Thibault - 1948612
    Jacob Brisson - 1954091
"""

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from ghostAgents import DirectionalGhost
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 1 ICI
    '''
    NEW_STATE = True
    OLD_STATE = False
    state = (problem.getStartState(), None, NEW_STATE)
    seen_state = []
    fringe = util.Stack()
    fringe.push(state)
    solution = []

    # Tant qu'il reste des états dans la fringe
    while fringe.isEmpty() is False:
        # Extraire le prochain état
        (state, direction, new_state) = fringe.pop()

        # Si on tombe sur un chemain déjà exploré, revenir en arrière
        if not new_state: solution.pop()

        # Si c'est un nouveau état, ajouter l'état à la solution et mettre dans la fringe l'était
        if direction is not None and new_state:
            solution.append(direction)
            fringe.push((state, direction, OLD_STATE))
        seen_state.append(state)

        # Si c'est un nouveau état, regarder si c'est l'état final et sinon mettre dans la fringe les états suivant
        # si se sont des nouveaux états
        if new_state:
            if problem.isGoalState(state):
                return solution
            else:
                for (state, direction, cost) in problem.getSuccessors(state):
                    if state not in seen_state:
                        fringe.push((state, direction, NEW_STATE))
    return False


def breadthFirstSearch(problem):
    """Search the shallowest states in the search tree first."""

    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 2 ICI
    '''
    state = (problem.getStartState(), None, None)
    seen_state = {}
    fringe = util.Queue()
    fringe.push(state)

    # Tant qu'il reste des états dans la fringe
    while fringe.isEmpty() is False:
        # Extraire le prochain état de la fringe
        (state, direction, state_from) = fringe.pop()

        # Vérifier c'est un état jamais vue ou non. Si oui, ajouter la node dans l'arbre
        first_exploration = False
        if state not in seen_state:
            seen_state[state] = (direction, state_from)
            first_exploration = True

        # Si c'est l'état final, construire le chemain le plus court en remontant l'arbre du chemain le plus court
        if problem.isGoalState(state):
            solution = [direction]
            while True:
                (direction, state_from) = seen_state[state_from]
                if direction is None: break
                solution.insert(0, direction)
            return solution
        # Ajouter les prochains états à la fringe si c'est la première fois qu'on est sur cet état
        elif first_exploration:
            for (next_state, direction, cost) in problem.getSuccessors(state):
                if next_state not in seen_state:
                    fringe.push((next_state, direction, state))
    return False


def uniformCostSearch(problem):
    """Search the state of least total cost first."""
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 3 ICI
    '''
    state = problem.getStartState()
    fringe = util.PriorityQueue()
    seen_state = {}
    fringe.push((state, None, None, 0), 0)

    # Tant qu'il reste des états dans la fringe
    while not fringe.isEmpty():
        # Extraire le prochain état de la fringe
        (state, direction, state_from, cost) = fringe.pop()

        # Vérifier c'est un état jamais vue ou non. Si oui, ajouter la node dans l'arbre
        first_exploration = False
        if state not in seen_state:
            seen_state[state] = (direction, state_from)
            first_exploration = True

        # Si c'est l'état final, construire le chemain le plus court en remontant l'arbre du chemain le plus court
        if problem.isGoalState(state):
            solution = [direction]
            while True:
                (direction, state_from) = seen_state[state_from]
                if direction is None: break
                solution.insert(0, direction)
            return solution
        # Ajouter les prochains états à la fringe si c'est la première fois qu'on est sur cet état
        elif first_exploration:
            for (next_state, direction, new_cost) in problem.getSuccessors(state):
                if next_state not in seen_state:
                    fringe.push((next_state, direction, state, new_cost + cost), new_cost + cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the state that has the lowest combined cost and heuristic first."""
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 4 ICI
    '''
    state = problem.getStartState()
    fringe = util.PriorityQueue()
    seen_state = {}
    fringe.push((state, None, None, 0), 0 + heuristic(state, problem))

    # Tant qu'il reste des états dans la fringe
    while not fringe.isEmpty():
        # Extraire le prochain état de la fringe
        (state, direction, state_from, cost) = fringe.pop()

        # Vérifier c'est un état jamais vue ou non. Si oui, ajouter la node dans l'arbre
        first_exploration = False
        if state not in seen_state:
            seen_state[state] = (direction, state_from)
            first_exploration = True

        # Si c'est l'état final, construire le chemain le plus court en remontant l'arbre du chemain le plus court
        if problem.isGoalState(state):
            solution = [direction]
            while True:
                (direction, state_from) = seen_state[state_from]
                if direction is None: break
                solution.insert(0, direction)
            return solution
        # Ajouter les prochains états à la fringe si c'est la première fois qu'on est sur cet état
        elif first_exploration:
            for (next_state, direction, new_cost) in problem.getSuccessors(state):
                if next_state not in seen_state:
                    h = heuristic(next_state, problem)
                    fringe.push((next_state, direction, state, new_cost + cost), new_cost + cost + h)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
