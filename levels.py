"""Tile-grid level definitions for the platformer.

Legend:
  ' ' empty space
  '#' solid ground
  'C' coin
  '^' spike (hazard)
  'E' enemy spawn point
  'F' flag (goal)
  'P' player spawn point
"""

LEVEL_1 = [
    "                                                                      ",
    "                                                                      ",
    "                                                                      ",
    "                                                                      ",
    "                                                                      ",
    "                                                                      ",
    "                           CCCC                    CC                 ",
    "                           ####                     ##                ",
    "              CCCCC                       CCC      ###                ",
    " P                 ^            E       ^^        ####    E         F ",
    "##########  #########   ###########  #########   ############  #######",
    "##########  #########   ###########  #########   ############  #######",
]

LEVEL_2 = [
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                        CCC                                                     ",
    "                        ###                         CCC                         ",
    "                                                    ###                         ",
    "              CCC                                                     CCC       ",
    " P          ^^          ^^ E       E ^          ^ E         E ^^             F  ",
    "########  #######  ##  #######   #######   ##  ########   ########   ###########",
    "########  #######  ##  #######   #######   ##  ########   ########   ###########",
]


def _normalize(level):
    width = max(len(row) for row in level)
    return [row.ljust(width) for row in level]


LEVEL_1 = _normalize(LEVEL_1)
LEVEL_2 = _normalize(LEVEL_2)
