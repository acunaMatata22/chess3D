# generally helpful functions used throughout the application

def squarePos(num):
    # returns the XY coordinates of the squares for initialization render
    # NOTE: for drawing only, not for indexing
    return (num % 8 - 3.5, (num % 64) // 8, (num // 64) * 1.13)

def indexToTuple(num):
    # used to reference the coordinate of a specific 0-127 indexed square
    return (num // 64, num % 8, num // 8)

def tupleToIndex(coordinates):
    # used to get square index from a coordinate tuple
    total = 0
    total += coordinates[0] * 64
    total += coordinates[1] * 8
    total += coordinates[2]
    return total