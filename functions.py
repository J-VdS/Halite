import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import logging


posdir = [Direction.North, Direction.South, Direction.East, Direction.West]

def max_halite(game_map, ship):
    global posdir
    hal = []
    for i in ship.position.get_surrounding_cardinals()+[ship.position]:
        if game_map[i].is_occupied:
            hal.append(0)
        else:
            hal.append(game_map[i].halite_amount)
    
    index = hal.index(max(hal))
    logging.info(ship)
    logging.info(index)
    if index == 4:
        return ship.stay_still()
    else:
        return ship.move(posdir[index])