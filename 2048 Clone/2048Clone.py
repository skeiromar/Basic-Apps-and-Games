
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


import math, random

# Tile Images
TILE_SIZE = 100
HALF_TILE_SIZE = TILE_SIZE / 2
BORDER_SIZE = 45

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


class GUI:
    """
    Class to run game GUI.
    """

    def __init__(self, game):
        self._rows = game.get_grid_height()
        self._cols = game.get_grid_width()
        self._frame = simplegui.create_frame('2048',
                        self._cols * TILE_SIZE + 2 * BORDER_SIZE,
                        self._rows * TILE_SIZE + 2 * BORDER_SIZE)
        self._frame.add_button('New Game', self.start)
        self._frame.set_keydown_handler(self.keydown)
        self._frame.set_draw_handler(self.draw)
        self._frame.set_canvas_background("#BCADA1")
        self._frame.start()
        self._game = game
        url = "http://codeskulptor-assets.commondatastorage.googleapis.com/assets_2048.png"
        self._tiles = simplegui.load_image(url)
        self._directions = {"up": UP, "down": DOWN,
                            "left": LEFT, "right": RIGHT}

    def keydown(self, key):
        """
        Keydown handler
        """
        for dirstr, dirval in self._directions.items():
            if key == simplegui.KEY_MAP[dirstr]:
                self._game.move(dirval)
                break

    def draw(self, canvas):
        """
        Draw handler
        """
        for row in range(self._rows):
            for col in range(self._cols):
                tile = self._game.get_tile(row, col)
                if tile == 0:
                    val = 0
                else:
                    val = int(math.log(tile, 2))
                canvas.draw_image(self._tiles,
                    [HALF_TILE_SIZE + val * TILE_SIZE, HALF_TILE_SIZE],
                    [TILE_SIZE, TILE_SIZE],
                    [col * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE,
                     row * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE],
                    [TILE_SIZE, TILE_SIZE])

    def start(self):
        """
        Start the game.
        """
        self._game.reset()


def run_gui(game):
    """
    Instantiate and run the GUI.
    """
    gui = GUI(game)
    gui.start()


"""
Clone of 2048 game.
"""


def merge(line1):
    """
    Helper function that merges a single row or column in 2048
    """
    line = [i for i in line1 if i != 0]
    for index in line1:
        if index == 0:
            line.append(index)
    for index in range(len(line) - 1):
        if line[index] == line[index + 1]:
            line[index] += line[index + 1]
            line.pop(index + 1)
            line.append(0)

    return line


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        Creates initial 2048 Board
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._is_moved = False
        self._grid = []
        self._width_height_max = max(self._grid_width, self._grid_height)
        self._init_tiles = {UP: [(0, i) for i in range(self._grid_width)],
                            DOWN: [(self._grid_height - 1, i) for i in range(self._grid_width)],
                            LEFT: [(i, 0) for i in range(self._grid_height)],
                            RIGHT: [(i, self._grid_width - 1) for i in range(self._grid_height)]}
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_num in range(self._grid_width)]
                      for dummy_num in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ""
        for line in self._grid:
            string += str(line) + "\n"
        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def remove_offsets(self, offsets_list):
        """
        Finds identical offsets and removes them from the list
        """
        for offset in range(len(offsets_list) - 1, 0, -1):
            if offsets_list[offset] == offsets_list[offset - 1]:
                offsets_list.pop(offset)

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        for key in self._init_tiles:
            if direction == key:
                for each_tile in self._init_tiles[key]:
                    offsets = []
                    temp_list = []
                    column = 0
                    row = 0
                    for tile in range(self._width_height_max):

                        offsets.append((each_tile[0] + OFFSETS[key][0] * column,
                                        each_tile[1] + OFFSETS[key][1] * row))
                        if tile < self._grid_height - 1:
                            column += 1
                        if tile < self._grid_width - 1:
                            row += 1
                    self.remove_offsets(offsets)
                    for offset in offsets:
                        temp_list.append(self._grid[offset[0]][offset[1]])

                    temp_list = merge(temp_list)

                    for index, offset in enumerate(offsets):
                        if self._grid[offset[0]][offset[1]] != temp_list[index]:
                            self._is_moved = True
                        self._grid[offset[0]][offset[1]] = temp_list[index]

        if self._is_moved:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # set to initial arbitrary value
        elem = 42
        zero_ind = 42
        weighted_list = [2] * 90 + [4] * 10

        while elem != 0:
            zero_ind = [random.randrange(0, self._grid_height),
                        random.randrange(0, self._grid_width)]
            elem = self._grid[zero_ind[0]][zero_ind[1]]
        self._grid[zero_ind[0]][zero_ind[1]] = random.choice(weighted_list)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


run_gui(TwentyFortyEight(4, 4))
