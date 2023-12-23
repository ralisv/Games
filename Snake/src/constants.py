Position = tuple[int, int]


class EDGES:
    WALL_HORIZONTAL = "──"
    WALL_VERTICAL = "│"
    WALL_TOP_LEFT = "┌──"
    WALL_TOP_RIGHT = "──┐"
    WALL_BOTTOM_LEFT = "└──"
    WALL_BOTTOM_RIGHT = "──┘"


class CELLS:
    WALL = "⬜"
    SNAKE = "⚫"
    HEAD = "⚪"
    EMPTY = "  "
    FRUIT = "🍎"


class DIRECTIONS:
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)
