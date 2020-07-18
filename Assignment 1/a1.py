from a1_support import *


def main():
    """
    This function takes player inputs to build the game and allow it to run.

    It initially requests you to input the size of the game and number of pokemon
    in the game.

    It then requests continued input until either all the Pokemon have been located
    or the game has been lost.

    If the player inputs 'h' it will print help text.

    If the player enters 'q' it will prompt whether you want to quit the game.

    If the player enters ':)' it will restart the game.

    A cell can be flagged by inputting an action preceded by 'f ' (eg 'f A1').
    
    """
    game_over = False
    #request size of the game
    grid_size = int(input("Please input the size of the grid: "))
    while grid_size <= 0 or grid_size > 26:
        grid_size = int(input("Please input the size of the grid: "))
    #request number of Pokemon
    number_of_pokemons = int(input("Please input the number of pokemons: "))
    while number_of_pokemons <= 0 or number_of_pokemons > grid_size**2:
        number_of_pokemons = int(input("Please input the number of pokemons: "))
     
    my_pokemon = generate_pokemons(grid_size, number_of_pokemons)
    game = UNEXPOSED * grid_size**2

    while game_over == False:
        display_game(game, grid_size)
        action = str(input("\nPlease input action: "))
        # Player asks for help
        if action == 'h': 
            print(HELP_TEXT)
            
        # Players asks to quit
        elif action == 'q':
            quit_action = str(input("You sure about that buddy? (y/n): "))
            if quit_action == "y":
                print("Catch you on the flip side.")
                return
            elif quit_action == "n":
                print("Let's keep going.")
                game_over = False                
            else: 
                print(INVALID)
                game_over = False

        # Player asks to reset    
        elif action == ':)':
            print("It's rewind time.")
            game = UNEXPOSED * grid_size**2
            my_pokemon = generate_pokemons(grid_size, number_of_pokemons)

        # Player asks to flag / unflag a cell
        elif action[0:2] == 'f ':
            flag_position = parse_position(action[2:], grid_size)
            if flag_position is not None:
                flag_index = position_to_index(flag_position, grid_size)
                game = flag_cell(game, flag_index)
                # check if won
                if check_win(game, my_pokemon):
                    game_over = True
                    display_game(game, grid_size)
                    print("You win.")
                    return
                # If not won, repeat asking for an action
                else:
                    game_over = False
            else:
                print(INVALID)
                game_over = False
                
        # Player asks to expose a cell
        elif action != "" and parse_position(action, grid_size) is not None:
            position_entered = parse_position(action, grid_size) 
            position_index = position_to_index(position_entered, grid_size) 
            # If the position index is flagged, do nothing
            if game[position_index] == FLAG:
                game_over = False
            # If position index is a Pokemon - game lost and expose pokemon
            elif position_index in my_pokemon:
                for pokemon_index in my_pokemon: 
                        game = replace_character_at_index(game, pokemon_index, POKEMON)
                display_game(game, grid_size)
                print("You have scared away all the pokemons.")
                game_over = True
                return
            # Build list of index and neighbours to expose
            cells_to_expose = big_fun_search(game, grid_size, my_pokemon, position_index) 
            # If the big_fun_search returned list didn't include our cell, add it in
            if position_index not in cells_to_expose:
                cells_to_expose.append(position_index)
            # Loop through list and expose all cells 
            for cell_index in cells_to_expose:
                char_to_expose = number_at_cell(game, my_pokemon, grid_size, cell_index)
                # If it's a pokemon, replace the cell index with the pokemon character
                if cell_index in my_pokemon: 
                    char_to_expose = POKEMON
                # If the cell isn't exposed yet, expose it; otherwise, move on
                if game[cell_index] == "~": 
                    game = replace_character_at_index(game, cell_index, char_to_expose)
                if check_win(game, my_pokemon):
                    game_over = True
                    display_game(game, grid_size)
                    print("You win.")
                    return               
                else:
                    game_over = False
        else:            
            print(INVALID)
    return
  

def big_fun_search(game, grid_size, pokemon_locations, index):
    """Searching adjacent cells to see if there are any Pokemon"s present.

    Using some sick algorithms.

    Find all cells which should be revealed when a cell is selected.

    For cells which have a zero value (i.e. no neighbouring pokemons) all
    the cell"s neighbours are revealed. If one of the neighbouring cells is
    also zero then all of that cell"s neighbours are also revealed. This repeats
    until no zero value neighbours exist.

    For cells which have a non-zero value (i.e. cells with neightbour pokemons),
    only the cell itself is revealed.

    Parameters:
            game (str): Game string.
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.

    Returns:
            (list<int>): List of cells to turn visible.
    """
    queue = [index]
    discovered = [index]
    visible = []

    if game[index] == FLAG:
            return queue

    number = number_at_cell(game, pokemon_locations, grid_size, index)
    if number != 0:
            return queue

    while queue:
            node = queue.pop()
            for neighbour in neighbour_directions(node, grid_size):
                    if neighbour in discovered or neighbour is None:
                            continue

                    discovered.append(neighbour)
                    if game[neighbour] != FLAG:
                            number = number_at_cell(game, pokemon_locations, grid_size, neighbour)
                            if number == 0:
                                    queue.append(neighbour)
                    visible.append(neighbour)
    return visible


def display_game(game, grid_size):
    """
    Prints out a grid-shaped representation of the game, given the game string
    and the grid size as arguments.

    For row 0 it prints the ordered numbers (starting from 1) which will form
    the column identifiers of the grid.

    For all subsequent rows, it prints a capital letter as a row identifier
    (starting with A for row 1 and continuing in alphabetical order). Following
    the row identifier, it prints the characters in the game string which fall
    within that row (with respect to the grid size).

    Parameters:
        game (str): Game string.
        grid_size (int): Size of game.
    """
    for row in range(grid_size+1):
        if row == 0:
            print(" ", end="")
            for col in range(grid_size):
                if col < 10:
                    print(' | ' + str(col+1), end="")
                else:
                    print('| ' + str(col+1), end="")
            if col < 10:
                print(' |\n', end="")
            else:
                print('|\n', end="")
            print("-" *((4*grid_size)+4))
        else:
            print(ALPHA[row-1], end="")
            for index in range(grid_size):
                print(" | "  + game[grid_size * (row-1) + index], end="")
            print(" |\n", end="")
            print("-" *((4*grid_size)+4))


def parse_position(action, grid_size):
    """
    Checks if the input action is in a valid format. If an invalid action is entered, 
    nothing is returned. If the action is valid, it then produces a tuple with the
    position of the cell.

    Parameters:
        action (str): Input to be actioned
        grid_size (int): Size of game.

    Returns:
        (tuple(int, int)): position (tuple(int, int)): Tuple of the row and column
                           position of a cell within the game grid.
    """
    grid_alpha = ALPHA[:grid_size] 
    if(action == ""):
        return

    action_row = action[0] 
    action_col = action[1:] 
    if action_row in grid_alpha and action_col.isdigit() and 0 < int(action_col) <= grid_size:
        return((grid_alpha.index(action_row),int(action_col) - 1))
    else: 
        return
 

def position_to_index(position, grid_size):
    """
    Converts the position tuple representative of the row and column co-ordinate
    within the game grid into an index within the game.

    It returns an integer which represents the index of the cell in the game string.

    Parameters:
        position (tuple(int, int)): Tuple of the row and column position of a cell within
                                    the game grid.
        grid_size (int): Size of game.

    Returns:
        (int): Index of cell in the game string.
    """
    index = position[0] * grid_size + position[1]
    return index


def replace_character_at_index(game, index, character):
    """
    Returns an updated game string with a specified character at a specified index of
    the game string.

    Parameters:
        game (str): Game string.
        index (int): Index of cell in the game string.
        character (str): Character which replaces another in the game string.

    Returns:
        (str): A game string which has been updated for the new character.
    """
    game_before_index = game[:index] 
    game_after_index = game[index+1:] 
    game = game_before_index + str(character) + game_after_index 
    return game


def flag_cell(game, index):
    """
    Toggles a flag character on / off at a specified index within the game string.
    The game string is updated for the toggled flag.

    Parameters:
        game (str): Game string.
        index (int): Index of cell in the game string.

    Returns:
        (str): A game string which has been updated for a toggled flag.
    """
    #Toggles flag on at unexposed index
    if game[index] == '~':
        game_before_index = game[:index] 
        game_after_index = game[index:] 
        game_after_index = game_after_index.replace('~', FLAG, 1) 
        game = game_before_index + game_after_index
        return game
    #Toggles flag off at already flagged index
    elif game[index] == FLAG:
        game_before_index = game[:index]
        game_after_index = game[index:] 
        game_after_index = game_after_index.replace(FLAG, '~', 1)  
        game = game_before_index + game_after_index
        return game
    #If trying to flag invalid index (eg already exposed cell)
    else:
        return game


def index_in_direction(index, grid_size, direction):  
    """
    Uses the index of a cell in the game string to generate a new index which
    corresponds to an adjacent cell in a specified direction.

    If an invalid direction is entered, nothing is returned.

    Parameters:
        index (int): Index of cell in the game string.
        grid_size (int): Size of game.
        direction (str): Direction relative to the cell.

    Returns:
        (int): Index of the adjacent cell.
    """
    if direction == LEFT:
        if index % grid_size == 0:
            return None
        else:
            return index - 1
    elif direction == RIGHT:
        if index % grid_size == grid_size - 1:
            return None
        else:
            return index + 1
    elif direction == UP:
        if index < grid_size:
            return None
        else:
            return index - grid_size
    elif direction == DOWN:
        if index >= grid_size**2 - grid_size:
            return None
        else:
            return index + grid_size
    elif direction == f"{UP}-{LEFT}":
        if index < grid_size or index % grid_size == 0:
            return None
        else:
            return index - grid_size - 1
    elif direction == f"{UP}-{RIGHT}":
        if index < grid_size or index % grid_size == grid_size - 1:
            return None
        else:
            return index - grid_size + 1
    elif direction == f"{DOWN}-{LEFT}":
        if index >= grid_size**2 - grid_size or index % grid_size == 0:
            return None
        else:
            return index + grid_size - 1
    elif direction == f"{DOWN}-{RIGHT}":
        if index >= grid_size**2 - grid_size or index % grid_size == grid_size - 1:
            return None
        else:
            return index + grid_size + 1


def neighbour_directions(index, grid_size):
    """
    Returns the list of indexes for the neighbouring cells of a specified cell.

    Parameters:
        index (int): Index of cell in the game string.
        grid_size (int): Size of game.

    Returns:
        (list[int, ...]): List of indexes which neighbour a specified cell.
        """
    index_list = []
    for i in DIRECTIONS:
        neighbour = index_in_direction(index, grid_size, i) 
        if neighbour != None: 
            index_list.append(neighbour) 
    return index_list


def number_at_cell(game, pokemon_locations, grid_size, index):
    """
    Returns the number of Pokemon in neighbouring cells.

    Parameters:
        game (str): Game string.
        pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
        grid_size (int): Size of game.
        index (int): Index of cell in the game string.

    Returns:
        (int): Number of Pokemon in neighbouring cells.
    """
    neighbours = neighbour_directions(index, grid_size)
    counter = 0
    for i in neighbours:
        if i in pokemon_locations:  
            counter += 1
    return counter


def check_win(game, pokemon_locations):
    """
    Returns True if the game has been won, and False if the game has not yet been won.

    First it creates a list of indexes of all the flags in the game string.

    Second it checks if there are still exposed cells in the game - if so it returns that
    the game has not yet been won. If there are no exposed cells remaining, it continues
    in the loop.

    Third it checks that if the number of flagged cells matches the number of Pokemon in the
    game, if the indexes for the flags and Pokemon locations are the same, the game is won.
    If not, it exits the loop.
    
    Parameters:
        game (str): Game string.
        pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.                                          

    Returns:
        (bool): True if game is won, False if not yet won.    
    """
    flag_list = []
    # Get indexes of flag chars only and add them to a list
    for index, char in enumerate(game): 
        if char == FLAG: 
            flag_list.append(index)
    #check if there are unexposed cells        
    if UNEXPOSED in game:
        return False 
    #check if flags and Pokemon are at the same index
    elif len(flag_list) == len(pokemon_locations):
        if all(indexes in flag_list for indexes in pokemon_locations):
            return True # All flags are pokemon
        else:
            return False # Flags aren't all pokemon
    else:
        return False # Flag list is too big or small 

if __name__ == "__main__":
    main()




