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

gh = {}

# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("Testbot v5")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    if game.turn_number == 1:
        shipyard = me.shipyard.position
        '''logging.info(str(me.shipyard))
        logging.info(type(me.shipyard))
        try:
            logging.info(type(me.shipyard.position))
            logging.info(str(me.shipyard.position))
        except:
            pass'''
    game_map = game.game_map

    command_queue = []
    move_queue = []

    for ship in me.get_ships():            
        if ship.position == shipyard:
            gh[ship.id] = False          
            com, move_queue = functions.max_halite(game_map, ship, move_queue)
            command_queue.append(com)
        
        elif gh[ship.id] or ship.halite_amount >700:
            move = game_map.naive_navigate(ship, shipyard)
            if move != Direction.Still:
                pos = Position(move[0], move[1])+ship.position
                if pos in move_queue:
                    move = Direction.Still
                else:
                    move_queue.append(pos)
            command_queue.append(ship.move(move))
                
            
            #game_map.naive_navigate(ship, shipyard)))
            gh[ship.id] = True
            
        
        elif game_map[ship.position].halite_amount >= constants.MAX_HALITE / 10:
            command_queue.append(ship.stay_still())
    
        else:
            com, move_queue = functions.max_halite(game_map, ship, move_queue)
            command_queue.append(com)
        
        '''
        if ship.halite_amount>400:
            command_queue.append(
                ship.move(
                    game_map.naive_navigate(ship, shipyard)))
        
        
        elif game_map[ship.position].halite_amount < constants.MAX_HALITE / 10:
            command_queue.append(
                ship.move(
                    random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))
        else:
            command_queue.append(ship.stay_still())
        '''
    if game.turn_number<200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

