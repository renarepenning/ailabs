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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from collections import deque
from util import Stack
from util import Queue
from util import PriorityQueue

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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    "*** YOUR CODE HERE ***"

    #nodes corrosponding to an orig state
    fringe = Stack()
    #maintain a set of visited states (not nodes)
    visited = []
    #create a first node using the start state
    firstNode = (problem.getStartState(), [], 1)
    fringe.push(firstNode)
   
    while not fringe.isEmpty():
        #chose and remove the top node v from fringe
        v = fringe.pop()
        #never expand a node whose state has been visited
        if v[0] not in visited:
            visited += [v[0]]
            #check if v's state is a goal state;
            if problem.isGoalState(v[0]):
                return v[1]
            #add each successor node to the fringe so we know to explore itggfggfgfgfg
            else:                
                for i in problem.getSuccessors(v[0]):
                    #add a new node with a path to fringe possibility
                    path = v[1] + [i[1]]
                    newNode = (i[0], path, 1)
                    #add the node to the fringe
                    fringe.push(newNode)
    return False


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #nodes corrosponding to an orig state
    fringe = Queue()
    #maintain a set of visited states (not nodes)
    visited = []
    #create a first node using the start state
    firstNode = (problem.getStartState(), [], 0)
    fringe.push(firstNode)
    
    while not fringe.isEmpty():
        #chose and remove the top node v from fringe
        v = fringe.pop()
        #never expand a node whose state has been visited
        if v[0] not in visited:
            visited += [v[0]]
            #check if v's state is a goal state;
            if problem.isGoalState(v[0]):
                return v[1] 
            #add each successor node to the fringe so we know to explore it
            else:                
                for i in problem.getSuccessors(v[0]):
                    #add a new node with a path to fringe possibility
                    path = v[1] + [i[1]]
                    newNode = (i[0], path, 1)
                    #add the node to the fringe
                    fringe.push(newNode)
            
    return False


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # use a priority queue
    fringe = PriorityQueue()
    visited = [] #maintain a list of visited states (not nodes)
    fringe.push((problem.getStartState(), [], 0), 1)
    
    while not fringe.isEmpty():
        #chose and remove the top node from fringe
        curr, path, path_cost = fringe.pop()
        #never expand a node whose state has been visited
        if curr not in visited:
            visited += [curr]
            #check if v's state is a goal state;
            if problem.isGoalState(curr):
                return path
                
            #add each successor node to the fringe so we know to explore it
            else:                
                for c, p, pc in problem.getSuccessors(curr):
                    #add a new node with a path to fringe possibility
                    fringe.push((c, path+[p], pc), pc)

    return False


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start= problem.getStartState()
    fringe=util.PriorityQueue()
    heur=heuristic(start,problem)
    fringe.push((start,[],1),heur)
    visitedStates=set()

    while fringe.isEmpty()==False:
        v=fringe.pop()
       
        if problem.isGoalState(v[0])==True:
           return v[1] #return the path to the goal (current) state
           
        elif (v[0] not in visitedStates): #if v's state has been visited before, skip    
            visitedStates.add(v[0])

            #expand v, inserting resulting nodes into fringe
            for i in problem.getSuccessors(v[0]):
               
                currentState=i[0] #current state being visited (child of v, visited after) to add to queue

                currentPath=v[1] #path that already exists
               
                newPath=[i[1]] # direction from parent (v) to child
               
                pathToCurrent=currentPath+newPath #add direction from parent to child

                cost=i[2] #cost of child being added to queue

                totalcost=v[2]+i[2] #total cost of the entire path

                newHeur=totalcost+ heuristic(i[0],problem) #total cost of path with new heuristic from expanded node

                newNode=(currentState,pathToCurrent,totalcost)
               
                fringe.push(newNode,newHeur) #add new Node to the queue




# Abbreviations

bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch