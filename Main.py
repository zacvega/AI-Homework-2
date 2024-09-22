from enum import Enum
import copy
import time

# class syntax
class Actions(Enum):
    SUCK = .6
    DOWN = .7
    UP = .8
    RIGHT = .9
    LEFT = 1

class Node:
    def __init__(self, state, actions = list(), pathCost = 0, depth = 0, parent = None,):
        self.state = state
        self.actions = actions
        self.pathCost = pathCost
        self.depth = depth
        self.parent = parent
        self.result = None
    
    def __lt__(self, other):
        if(self.pathCost != other.pathCost):
            return self.pathCost < other.pathCost
        elif(self.state.vacLoc[0] != other.state.vacLoc[0]):
                return self.state.vacLoc[0] < other.state.vacLoc[0]
        elif(self.state.vacLoc[1] != other.state.vacLoc[1]):
                return self.state.vacLoc[1] < other.state.vacLoc[1]

    
    def __str__(self):
        a = list()
        for i in self.actions:
           a.append(i.name) 
        return f'Actions: {a}\n\tCost: {self.pathCost:.1f}\n\tDepth: {self.depth}\n\tDirt Left: {len(self.state.dirtLocs)}'

def goal_test(node):
    if(len(node.state.dirtLocs) == 0):
        return True
    else:
        return False

def expand(node):
    sensibleActions = list()
    for i in Actions:
        sensibleActions.append(i)

    # the agent wont try and undo its last move
    if(len(node.actions) > 0):
        match node.actions[len(node.actions)-1].name:
            case 'UP':
                sensibleActions.remove(Actions.DOWN)
            case 'DOWN':
                sensibleActions.remove(Actions.UP)
            case 'LEFT':
                sensibleActions.remove(Actions.RIGHT)
            case 'RIGHT':
                sensibleActions.remove(Actions.LEFT)
    

    successors = set()
    for move in sensibleActions:
        state = copy.deepcopy(node.state)
        # only adds the move to the expansion if it is valid (makes sense to do so)
        if(state.isActionPossible(move)):
            state.performAction(move)
            s = Node(copy.deepcopy(state), node.actions + [move], node.pathCost + move.value, node.depth+1, node)
            successors.add(s)
            if(move == Actions.SUCK):
                break

    return list(successors)

def pairMax(xlst):
    xMax = 0
    yMax = 0
    for i in xlst:
        xMax = max(xMax, i[0])
        yMax = max(yMax, i[1])

    return xMax, yMax

class Space:
    def __init__(self, vacuumStartLoc, dirty_squares, rows = None, columns = None):
        """
        Initializes the space with a vacuum and dirty rooms

        ## Parameters
        * rows:  Number of rows for space 
            * Type: int

        * columns: Number of columns for space 
            * Type: int

        * vacuumStartLoc: Starting space (ordered pair) for vacuum 
            * Type: (int, int)
            * (1 based index)

        * dirty_squares: List of location(s) (ordered pairs) for dirty rooms 
            * Type: [(int, int),...]
            * (1 based index)
        """
        if(rows != None):
            self.rows = rows
        else:
            self.rows = pairMax([vacuumStartLoc]+dirty_squares)[0]

        if(columns != None):
            self.columns = columns
        else:
            self.columns = pairMax([vacuumStartLoc]+dirty_squares)[1]

        self.goalCost = 0
        self.vacLoc = vacuumStartLoc
        self.dirtLocs = dirty_squares

    def printFloorLayout(self):
        """
        Displays the layout of the space
        each sell has format (row, colum)
        * If the space contains the vacuum it will additionally display 'Vac'
        * If the space is dirty it will additionally display 'Dirty'
        """

        for i in range(self.rows):
            for j in range(self.columns):
                text = "[({0}, {1}) {2:3} {3:5}]"
                print(text.format(i+1, j+1, ("", "Vac")[(i+1,j+1)==self.vacLoc], ("", "Dirty")[(i+1, j+1) in self.dirtLocs]), end="")
                if j != self.columns - 1:
                    print(", ", end="") 
            print("")

    def printFloorState(self):
        """
        Displays which room has the vacuum and which rooms are dirty
        """

        print("[V", self.vacLoc, end="")
        
        if(self.dirtLocs):
            for pair in self.dirtLocs:
                print(", d"+str(pair), end="")
        print(f"] with g = {self.goalCost:.1f}")

    def performAction(self, action: Actions, verbose=False):
        possible = self.isActionPossible(action)
        if(possible):
            match action.name:
                case 'LEFT':
                    self.vacLoc = (self.vacLoc[0], self.vacLoc[1] - 1)
                case 'RIGHT':
                    self.vacLoc = (self.vacLoc[0], self.vacLoc[1] + 1)
                case 'UP':
                    self.vacLoc = (self.vacLoc[0] - 1, self.vacLoc[1])
                case 'DOWN':
                    self.vacLoc = (self.vacLoc[0]+1, self.vacLoc[1]) 
                case 'SUCK':
                    self.dirtLocs.remove(self.vacLoc)
                    
            if(verbose):
                if(action == Actions.SUCK):
                    print("Cleaned " + str(self.vacLoc))
                else:
                    print("Moved "+action.name+" to " + str(self.vacLoc))

            self.goalCost += action.value
        else:
            if(verbose):
                print("Didn't perform action " + action.name)
  
    def isActionPossible(self, action: Actions):
        match action.name:
            case 'LEFT':
                if(self.vacLoc[1] != 1):
                    return True

            case 'RIGHT':
                if(self.vacLoc[1] != self.columns):
                    return True

            case 'UP':
                if(self.vacLoc[0] != 1 ):
                    return True

            case 'DOWN':
                if(self.vacLoc[0] != self.rows):
                    return True
            case 'SUCK':
                if(self.vacLoc in self.dirtLocs):
                    return True
        return False

# function Depth-Limited-Search( problem,limit) returns soln/fail/cutoff
# Recursive-DLS(Make-Node(Initial-Stat e [problem]),problem,limit)
# function Recursive-DLS(node,problem,limit) returns soln/fail/cutoff
# cutoff-occurred? ← false
# if Goal-Test(problem,State[node]) then return node
# else if Depth[node] = limit then return cutoff
# else for each successor in Expand(node,problem) do
# result ← Recursive-DLS(successor,problem,limit)
# if result = cutoff then cutoff-occurred? ← true
# else if result ≠ failure then return result
# if cutoff-occurred? then return cutoff else return failure

def iddfs(node,limit):
        def dls(depth):
            if len(node.state.dirtLocs) == 0:
                return 1
            if depth == 0:
                return None
            for action in Actions:
                node.state.performAction(action)
            return None
        depth = 0
        while True:
            result = dls(depth)
            if result == 1:
                print(node.state.ActionList)
                return 0
            depth += 1

def general_tree_search(problem):
    fringe = [Node(problem)]
    count = 0
    while True:
        if (len(fringe) == 0):
            node.result = False
            return False, count  
        node = fringe.pop()
        if goal_test(node):
            node.result = True
            return node, count 
        fringe = fringe + expand(node)
        count += 1

def uniform_cost_tree_search(problem):
    fringe = [Node(problem)]
    first5nodes = list()
    expandedCount = 0
    while True:
        if (len(fringe) == 0):
            node.result = False
            return False, expandedCount, len(fringe), first5nodes
        node = fringe.pop()
        if goal_test(node):
            node.result = True
            return node, expandedCount, len(fringe), first5nodes
        expandedCount +=1
        newNodes = expand(node)
        if (len(first5nodes) < 5):
            for i in newNodes:
                if (len(first5nodes) >= 5):
                    break
                else:    
                    first5nodes.append(i)
            
        fringe = fringe + newNodes
        fringe.sort(reverse=True)

def main():
    instance1 = Space((2,2), [(1,2),(2,4),(3,5)], 4, 5)
    instance2 = Space((3,2), [(1,2),(2,1),(2,4),(3,3)], 4, 5)
    
    # the following 2 instances set up by limiting the space to only whats needed
    # determined by the max location used between vacuum or dirty spots
    # instance1 = Space((2,2), [(1,2),(2,4),(3,5)])
    # instance2 = Space((3,2), [(1,2),(2,1),(2,4),(3,3)])

    print("instance 1: uniform cost tree search")
    start = time.time()
    successNode, expanded, generated, first5nodes = uniform_cost_tree_search(copy.deepcopy(instance1))
    end = time.time()
    print(successNode)
    print("\tGenerated node count:", generated)
    print("\tFirst 5 nodes generated")
    for i in first5nodes:
        print(f"\t\tMovement: {i.actions}, State: ", end="")
        i.state.printFloorState()
    print("\tExpanded node count:", expanded)
    print(f"\tTook {end-start:.2f} seconds")



    print("\ninstance2: uniform cost tree search")
    start2 = time.time()
    successNode2, expanded2, generated2, first5nodes2 = uniform_cost_tree_search(copy.deepcopy(instance2))
    end2 = time.time()
    print(successNode2)
    print("\tGenerated node count:", generated2)
    print("\tFirst 5 nodes generated")
    for i in first5nodes2:
        print(f"\t\tMovement: {i.actions}, State: ", end="")
        i.state.printFloorState()
    print("\tExpanded node count:", expanded2)
    print(f"\tTook {end2-start2:.2f} seconds")

    print(f"\nBoth instances in total took {end2-start:.2f} seconds")


    # tstInstance.printFloorLayout()

if(__name__ == "__main__"):
    main()
