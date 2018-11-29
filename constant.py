# Contains all constants used throughout the program
from panda3d.core import Vec4

# Colors
### Checkerboard colors
VANILLA = Vec4(0.953, 0.898, 0.671, 1)
WALNUT = Vec4(.416, 0.263, .177, 1)
### Pieces colors
# NOTE: pieces have alpha value that is used for moving pieces
WHITEP = Vec4(0.941, 0.871, 0.584, 0.5)
BLACKP = Vec4(0.1, 0.1, 0.1, 0.5)
### Colors used for highlighting squares
SELECT = Vec4(0, 0.573, 0.741, 1)
HIGHLIGHT = Vec4(0.224, 0.428, 0.518, 1)