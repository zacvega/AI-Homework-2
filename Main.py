from enum import Enum
import copy
import time

# class syntax
class Actions(Enum): #All of the actions the vacuum can do
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

    return list(sorted(successors))

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
IDS_First_5_Nodes = list()
def Depth_Limited_Search(node,limit):
    return Recursive_DLS(node, limit, 0, 0)#(start node, level limit, expanded nodes, generated nodes)

def Recursive_DLS(node, limit, Exp_CT, Gen_CT):
    if len(IDS_First_5_Nodes)< 5: #collect only the first 5 nodes.
        IDS_First_5_Nodes.append(node) #add node to list
    cutoffOccurred = False #assume 
    if goal_test(node): # node has been reached where all rooms are clean
        return node,Exp_CT,Gen_CT
    elif node.depth == limit: # level limit has been reached, after this the level limit will increase by 1 until the final node has been found.
        return -1,Exp_CT,Gen_CT # -1 means not found
    Exp_CT += 1 # Expanded count increases 
    ExpandedNodes = expand(node) # expand to the next level
    Gen_CT += len(ExpandedNodes) #generated count increases
    for successor in ExpandedNodes: #for each expanded node
        result, Exp_CT, Gen_CT = Recursive_DLS(successor, limit, Exp_CT, Gen_CT) # recursive call
        if result == -1: #level limit was reached
            cutoffOccurred = True
        elif result != -2: #error
            return result, Exp_CT, Gen_CT
    if cutoffOccurred:#level limit was reached
        return -1,Exp_CT, Gen_CT
    else:#error
        return -2,Exp_CT, Gen_CT

def Iterative_Deepening_Search(Problem):
    IDS_First_5_Nodes.clear() #list of the first 5 nodes searched in the graph
    depth = 0 # limit inital depth to 0
    Exp_Ct = 0
    Gen_Ct = 0
    while True: #For each level 0->1->...->n
        result, tempExp_Ct, tempGen_Ct = Depth_Limited_Search(Node(Problem),depth)
        Exp_Ct += tempExp_Ct # number of expanded nodes
        Gen_Ct += tempGen_Ct # generated of expanded nodes
        if result != -1: # No error
            return result, Exp_Ct, Gen_Ct
        depth+=1 #Next level max depth
        

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

def uniform_cost_graph_search(problem): #uniform_graph_search
    fringe = [Node(problem)]#get the first node for fringe
    closed = set()#create an empty set called close
    first5nodes = list()#make a list for the first 5 nodes
    expandedCount = 0#var for expanded nodes
    while True: #run loop
        if (len(fringe) == 0): #if the fringe is empty return false, the count, and the first 5 nodes, and end function
            node.result = False
            return False, expandedCount, len(fringe), first5nodes
        node = fringe.pop()#remove a node from fringe
        if goal_test(node):#check to see if that node is the goal if yes, return true, the count, and the expanded nodes
            node.result = True
            return node, expandedCount, len(fringe), first5nodes
        



        if node.state not in closed: #if the state of the node is NOT in set closed, add it, then get 5 new nodes for fringe and update count
            closed.add(node.state)
            expandedCount +=1
            newNodes = expand(node)
            if (len(first5nodes) < 5):
                for i in newNodes:
                    if (len(first5nodes) >= 5):
                        break
                    else:    
                        first5nodes.append(i)
            fringe = fringe + newNodes
            fringe.sort(reverse=True)#rearrange fringe to have lowest cost node at the top, this is what makes this uniform cost

        
        
        
        
        




    return 


def main():
    instance1 = Space((2,2), [(1,2),(2,4),(3,5)], 4, 5)
    instance2 = Space((3,2), [(1,2),(2,1),(2,4),(3,3)], 4, 5)

    #the following 2 instances set up by limiting the space to only whats needed
    #determined by the max location used between vacuum or dirty spots
    #instance1 = Space((2,2), [(1,2),(2,4),(3,5)])
    #instance2 = Space((3,2), [(1,2),(2,1),(2,4),(3,3)])
#################################################################################################################################################
    print("***************uniform cost tree search**********************")
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


    #tstInstance.printFloorLayout()
    print("***************************************************************")
##################################################################################################################################################
    print("***************uniform cost graph search**********************")
    print("instance 1: uniform cost graph search")
    start = time.time()
    successNode, expanded, generated, first5nodes = uniform_cost_graph_search(copy.deepcopy(instance1))
    end = time.time()
    print(successNode)
    print("\tGenerated node count:", generated)
    print("\tFirst 5 nodes generated")
    for i in first5nodes:
         print(f"\t\tMovement: {i.actions}, State: ", end="")
         i.state.printFloorState()
    print("\tExpanded node count:", expanded)
    print(f"\tTook {end-start:.2f} seconds")

    print("\ninstance2: uniform cost graph search")
    start2 = time.time()
    successNode2, expanded2, generated2, first5nodes2 = uniform_cost_graph_search(copy.deepcopy(instance2))
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


    
    
















    print("***************************************************************")
##################################################################################################################################################
    print("***************Iterative Deepening Search**********************")

    print("instance 1: Iterative Deepening Search")
    start = time.time()
    node, expanded, generated = Iterative_Deepening_Search(copy.deepcopy(instance1))
    end = time.time()
    print(node)
    print("\tGenerated node count:", generated)
    print("\tFirst 5 nodes generated")
    for i in IDS_First_5_Nodes:
        print(f"\t\tMovement: {i.actions}, State: ", end="")
        i.state.printFloorState()
    print("\tExpanded node count:", expanded)
    print(f"\tTook {end-start:.2f} seconds")

    print("instance 2: Iterative Deepening Search")
    start = time.time()
    node, expanded, generated = Iterative_Deepening_Search(copy.deepcopy(instance2))
    end = time.time()
    print(node)
    print("\tGenerated node count:", generated)
    print("\tFirst 5 nodes generated")
    for i in IDS_First_5_Nodes:
        print(f"\t\tMovement: {i.actions}, State: ", end="")
        i.state.printFloorState()
    print("\tExpanded node count:", expanded)
    print(f"\tTook {end-start:.2f} seconds")


    print("***************************************************************")

if(__name__ == "__main__"):
    main()
