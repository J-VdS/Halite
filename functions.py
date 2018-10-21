import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import logging


posdir = [Direction.North, Direction.South, Direction.East, Direction.West]

def max_halite(game_map, ship, move_queue):
    global posdir
    hal = []
    for i in ship.position.get_surrounding_cardinals()+[ship.position]:
        if game_map[i].is_occupied or i in move_queue:
            hal.append(0)
        else:
            hal.append(game_map[i].halite_amount)      
    move_queue.append(i)
    index = hal.index(max(hal))
    if index == 4:
        return ship.stay_still(), move_queue
    else:
        return ship.move(posdir[index]), move_queue
    