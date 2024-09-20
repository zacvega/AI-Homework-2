from enum import Enum
# class syntax
class Actions(Enum):
    LEFT = 1
    RIGHT = .9
    UP = .8
    DOWN = .7
    SUCK = .6

class Node:
    def __init__(self, state, actions = [],pathCost = 0, depth = 0,  parent = None,):
        self.state = state
        self.pathCost = pathCost
        self.depth = depth
        self.actions = actions
        self.parent = parent
        self.result = None

def expand(node, state):
    successors = set()
    for move in Actions:
        s = Node(state, s.actions + move, s.pathCost + move.value, s.depth+1)
        successors.add(s)

    # print(successors)
    return successors

class Space:
    def __init__(self, rows, columns, vacuumStartLoc, dirty_squares):
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
        self.rows = rows
        self.columns = columns
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
        print("] with g = " + str(self.goalCost))

    def performAction(self, action: Actions):
        # print(action.name, action.value)
        self.goalCost -= action.value

        match action.name:
            case 'LEFT':
                if(self.vacLoc[1] != 1):
                    self.vacLoc = (self.vacLoc[0], self.vacLoc[1] - 1)
                    print("Moved "+action.name+" to " + str(self.vacLoc))
                else:
                    print("Didn't perform action " + action.name)

            case 'RIGHT':
                if(self.vacLoc[1] != self.columns):
                    self.vacLoc = (self.vacLoc[0], self.vacLoc[1] + 1)
                    print("Moved "+action.name+" to " + str(self.vacLoc))
                else:
                    print("Didn't perform action " + action.name)

            case 'UP':
                if(self.vacLoc[0] != 1 ):
                    self.vacLoc = (self.vacLoc[0] - 1, self.vacLoc[1])
                    print("Moved "+action.name+" to " + str(self.vacLoc))
                else:
                    print("Didn't perform action " + action.name)


            case 'DOWN':
                if(self.vacLoc[0] != self.rows):
                    self.vacLoc = (self.vacLoc[0]+1, self.vacLoc[1]) 
                    print("Moved "+action.name+" to " + str(self.vacLoc))
                else:
                    print("Didn't perform action " + action.name)


            case 'SUCK':
                if(self.vacLoc in self.dirtLocs):
                    self.dirtLocs.remove(self.vacLoc)
                    print("Cleaned " + str(self.vacLoc))
                else:
                    print("Didn't perform action " + action.name)
        


def main():
    instance1 = Space(4, 5, (2,2), [(1,2),(2,4),(3,5)])
    instance1.printFloorLayout()
    instance1.printFloorState()
    instance1.performAction(Actions.UP)

    print("\n\n")

    instance2 = Space(4, 5, (3,2), [(1,2),(2,1),(2,4),(3,3)])
    instance2.printFloorLayout()
    instance2.printFloorState()

if(__name__ == "__main__"):
    main()
