from position import Position

SPRITE_SIZE = 32

DOWN_LEFT  = Position(-1,-1)
UP_LEFT    = Position(-1,1)
UP_RIGHT   = Position(1,1)
DOWN_RIGHT = Position(1,-1)

UP         = Position(0,1)
RIGHT      = Position(1,0)
DOWN       = Position(0,-1)
LEFT       = Position(-1,0)

WINDOW_W, WINDOW_H = 1024, 768
VIEWPORT_W, VIEWPORT_H = 25, 20

MAP_W, MAP_H = VIEWPORT_W * SPRITE_SIZE, VIEWPORT_H * SPRITE_SIZE
DEFAULT_MAP_CELLS_X, DEFAULT_MAP_CELLS_Y = 300, 300

MSGBOX_W, MSGBOX_H = MAP_W, WINDOW_H - MAP_H
MSGBOX_X, MSGBOX_Y = 0, MAP_H

OUTLINE_W, OUTLINE_H = 224, 400
OUTLINE_X, OUTLINE_Y = MAP_W, MAP_H - OUTLINE_H

MSGBOX_LINES = 7

DUNGEON_WALL = 0
DUNGEON_FLOOR = 1
DUNGEON_DOOR = 2
OUT_OF_BOUNDS = 3
OPEN_DOOR = 4

CLOSE_TO_EDGE = 164

#MAP GENERATION STUFF
MINIMUM_ROOM_SIZE = 4
BSP_RECURSION_DEPTH = 12
MAX_DOORS_PER_TUNNEL = 2

DEFAULT_MSGSTYLE = dict(font_name='Arial', font_size=10, color=(255,255,255,255))

bonus = {
         "1": -6,
         "2": -5,
         "3": -5,
         "4": -4,
         "5": -4,
         "6": -3,
         "7": -3,
         "8": -2,
         "9": -2,
         "10": -1,
         "11": 0,
         "12": 0,
         "13": 0,
         "14": 1,
         "15": 2,
         "16": 4,
         "17": 5,
         "18": 6
         }
