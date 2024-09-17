import numpy as np
# Class to represent a room in the space
class Room:

    def __init__(self, isDirty, hasVacuum):
        self.isDirty = isDirty
        self.hasVacuum = hasVacuum

def printFloorLayout(array):
    """
    Displays the layout of the space
    each sell has format (row, colum)
    * If the space contains the vacuum it will additionally display 'Vac'
    * If the space is dirty it will additionally display 'Dirty'
    """
    matrix = np.array(array)
    
    dimensions = matrix.shape
    rows, columns = dimensions

    for i in range(rows):
        for j in range(columns):
            text = "[({0}, {1}) {2:3} {3:5}]"
            print(text.format(i+1, j+1, ("", "Vac")[array[i][j].hasVacuum], ("", "Dirty")[array[i][j].isDirty]), end="")
            if j != columns - 1:
                print(", ", end="") 
        print("")

def printFloorState(array):
    """
    Displays which room has the vacuum and which rooms are dirty
    """
    matrix = np.array(array)
    
    dimensions = matrix.shape
    rows, columns = dimensions
    dirtyRooms = []
    for i in range(rows):
        for j in range(columns):
            if (array[i][j].hasVacuum):
                vacCords = (i+1,j+1)
            if (array[i][j].isDirty):
                dirtyRooms.append((i+1,j+1))


    print("[V", vacCords, end="")
    
    if(dirtyRooms):
        for pair in dirtyRooms:
            print(", d"+str(pair), end="")
    print("]")
            

def setSpace(rows: int, columns: int, vacuumStartLoc, dirty_squares):
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
    array = [[Room(False, False) for i in range(columns)] for j in range(rows)]
    array[vacuumStartLoc[0]-1][vacuumStartLoc[1]-1].hasVacuum = True

    for i in dirty_squares:
        array[i[0]-1][i[1]-1].isDirty = True

    return array

def main():
    instance1 = setSpace(4, 5, (2,2), [(1,2),(2,4),(3,5)])
    printFloorLayout(instance1)
    printFloorState(instance1)
     
    print("\n\n")

    instance2 = setSpace(4, 5, (3,2), [(1,2),(2,1),(2,4),(3,3)])
    printFloorLayout(instance2)
    printFloorState(instance2)

if(__name__ == "__main__"):
    main()
