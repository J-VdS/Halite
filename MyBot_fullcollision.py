import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import functions

import random
#   (print statements) are reserved for the engine-bot communication.
import logging


""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()

dir_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("Testbot v7")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map
    
    if game.turn_number == 1:
        shipyard = me.shipyard.position
        gh = []
    
    command_queue = []
    choices = []
       
    for ship in me.get_ships():
        pos = ship.position.get_surrounding_cardinals() +[ship.position]
        
        
        #{(1,0):(44,10)}
        pos_dict = {dir_order[n]:i for n,i in enumerate(pos)}
        #{(1,0):205}
        halite_dict = {}
        
        
        for pos in pos_dict:
            if pos_dict[pos] in choices or game_map[pos_dict[pos]].is_occupied:
                continue
            halite_dict[pos] = game_map[pos_dict[pos]].halite_amount
            
        logging.info(pos_dict)
        logging.info(halite_dict)
        
        if ship.is_full or ship.id in gh:
            move = game_map.naive_navigate(ship, shipyard)
            if game_map.normalize(Position(move[0], move[1])+ ship.position) in choices:
                move = (0,0)
            choices.append(game_map.normalize(Position(move[0], move[1])+ ship.position))
                
            command_queue.append(ship.move(move))
            if ship.position == shipyard:
                gh.remove(ship.id)
            elif ship.id not in gh:
                gh.append(ship.id)
                        
        
        elif game_map[ship.position].halite_amount < constants.MAX_HALITE/8:
            move = max(halite_dict, key=halite_dict.get)
            command_queue.append(ship.move(move))
            choices.append(pos_dict[move])
        else:
            choices.append(pos_dict[(0,0)])
            command_queue.append(
                ship.stay_still())
       
    
    
    if game.turn_number <=200 and me.halite_amount > constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        if False in [game_map[i].is_occupied for i in shipyard.get_surrounding_cardinals()] and shipyard not in choices:
            command_queue.append(me.shipyard.spawn())
        

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
    

