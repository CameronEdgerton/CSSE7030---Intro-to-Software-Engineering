EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

SPECIAL_TILES = {
    "S": START_PIPE,
    "E": END_PIPE,
    "L": LOCKED_TILE
}

PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}

class Tile(object):
    """
    Representation of available space in the game board.
    """
    def __init__(self, name, selectable=True):
        """
        Constructs a tile.

        Parameters:
        name (str): Name of the tile
        selectable (bool): Returns True if tile can have pipes placed on it, False otherwise.
        """
        self._name = name
        self._selectable = selectable
        self._id = 'tile'

    def get_name(self):
        """ Returns tile name.

        Returns:
        (str): Name of tile."""
        return self._name

    def get_id(self):
        """ Returns class ID.

        Returns:
        (str): ID of tile class."""
        return self._id

    def set_select(self, select:bool):
        """ Sets the stats of the select swith to True or False.

        Returns:
        (bool): Returns True if tile can have pipes placed on it, False otherwise.
        """
        if self._name == 'locked':
            self._selectable == False
            return self._selectable
        else:
            self._selectable == True
            return self._selectable

    def can_select(self):
        """Returns True if the tile is selectable, or False if the tile is not
        selectable

        Returns:
        (bool): True if the tile is selectable, False otherwise.
        """
        if self._selectable is True:
            return True
        else:
            return False

    def __str__(self):
        """ Returns the string representation of the Tile.

        Returns:
        (str): String representation of the tile.
        """
        return f"Tile('{self._name}', {self._selectable})"

    def __repr__(self):
        """Returns official string representation of the Tile.

        Returns:
        (str): String representation of the tile.
        """
        return self.__str__()

class Pipe(Tile):
    """Representation of a pipe in the game."""
    def __init__(self, name, orientation=0, selectable=True):
        """ Constructs a pipe.

        Parameters:
        name (str): Name of the pipe.
        orientation (int): orientation of the pipe.
        selectable (bool): Returns True if not loaded into the game board. False otherwise.
        """
        self._name = name
        self._orientation = orientation
        self._selectable = selectable
        self._id ='pipe'               

    def get_connected(self, side:str):
        """ Returns a list of all sides that are connected to the given side. 
        i.e. return a list containing some combination of ‘N’, ‘S’, ‘E’, ‘W’ or
        an empty list.

        Parameters:
        side(str): A side of the pipe.

        Returns:
        (list(str)): A list of all sides connected to the given side.
        """
        if self._name == 'straight':
            return Straight.get_connected(self, side)
        elif self._name == 'corner':
            return Corner.get_connected(self, side)
        elif self._name == 'cross':
            return Cross.get_connected(self, side)
        elif self._name == 'junction-t':
            return Tjunction.get_connected(self, side)
        elif self._name == 'diagonals':
            return Diagonals.get_connected(self, side)
        elif self._name == 'over-under':
            return Overunder.get_connected(self, side)
        else:
            return        

    def rotate(self, direction: int):
        """ Rotates the pipe one turn. A positive direction implies
        clockwise rotation, and a negative direction implies counter-clockwise 
        rotation and 0 means no rotation.

        Parameters:
        direction(int): Direction to rotate a pipe.
        """
        if direction == 1:
            self._orientation += 1
            if self._orientation == 4: 
                self._orientation = 0
            else:
                self._orientation
        elif direction == -1:
            self._orientation -= 1
            if self._orientation == -4:
                self._orientation = 0
            else:
                self._orientation
        else:
            return

    def get_orientation(self):
        """ Returns the orientation of the pipe.

        Returns:
        (int): current orientation of the pipe.
        """
        if self._orientation in range(4):
            return self._orientation
        else:  #check with tutor if this is appropriate
            self._orientation = 0
            return self._orientation

    def __str__(self):
        """ Returns the string representation of the pipe.

        Returns:
        (str): String representation of the pipe.
        """
        return f"Pipe('{self._name}', {self._orientation})"

    def __repr__(self):
        """Returns official string representation of the pipe.

        Returns:
        (str): String representation of the pipe.
        """
        return self.__str__()

class Straight(Pipe):
    """Representation of a straight pipe in the game"""
    def __init__(self):
        """Initializes the straight pipe attributes."""
        super().__init__()

    def get_connected(self, side:str):
        """ Returns a list of sides connected to a straight pipe at a given
        orientation.

        Parameters:
        side(str): A side of the pipe.

        Returns:
        (list(str)): A list of all sides connected to the given side.
        """
        pipe_list = []
        if self._orientation == 0 or self._orientation == 2:
            if side == 'N':
                pipe_list.append('S')
                return pipe_list
            elif side == 'S':
                pipe_list.append('N')
                return pipe_list
            else:
                return pipe_list
        if self._orientation == 1 or self._orientation == 3:
            if side == 'E':
                pipe_list.append('W')
                return pipe_list
            elif side == 'W':
                pipe_list.append('E')
                return pipe_list
            else:
                return pipe_list
        else:
            return
            
class Corner(Pipe):
    """Representation of a corner pipe in the game"""
    def __init__(self):
        """Initializes the corner pipe attributes."""
        super().__init__()

    def get_connected(self, side:str):
        """ Returns a list of sides connected to a corner pipe at a given
        orientation.

        Parameters:
        side(str): A side of the pipe.

        Returns:
        (list(str)): A list of all sides connected to the given side.
        """
        pipe_list = []
        if self._orientation == 0: 
            if side == 'N':
                pipe_list.append('E')
                return pipe_list
            elif side == 'E':
                pipe_list.append('N')
                return pipe_list
            else:
                return pipe_list
        if self._orientation == 1: 
            if side == 'E':
                pipe_list.append('S')
                return pipe_list
            elif side == 'S':
                pipe_list.append('E')
                return pipe_list
            else:
                return pipe_list
        if self._orientation == 2: 
            if side == 'S':
                pipe_list.append('W')
                return pipe_list
            elif side == 'W':
                pipe_list.append('S')
                return pipe_list
            else:
                return pipe_list
        if self._orientation == 3:
            if side == 'W':
                pipe_list.append('N')
                return pipe_list
            elif side == 'N':
                pipe_list.append('W')
                return pipe_list
            else:
                return pipe_list
        else:
            return

class Cross(Pipe):
    """Representation of a cross pipe in the game"""
    def __init__(self):
        """Initializes the cross pipe attributes."""
        super().__init__()

    def get_connected(self, side:str):
        """ Returns a list of sides connected to a cross pipe at a given
        orientation.

        Parameters:
        side(str): A side of the pipe.

        Returns:
        (list(str)): A list of all sides connected to the given side.
        """
        pipe_list = ['N', 'E', 'S', 'W']
        if side in pipe_list:
            pipe_list.remove(side)
            return pipe_list
        else:
            return

class Tjunction(Pipe):
    """Representation of a junction-t pipe in the game"""
    def __init__(self):
        """Initializes the junction-t pipe attributes."""
        super().__init__()

    def get_connected(self, side:str):
        """ Returns a list of sides connected to a junction-t pipe at a given
        orientation.

        Parameters:
        side(str): A side of the pipe.

        Returns:
        (list(str)): A list of all sides connected to the given side.
        """
        pipe_list = ['N', 'E', 'S', 'W']
        if self._orientation == 0:
            if side == 'E' or side == 'S' or side == 'W':
                pipe_list.remove(side)
                pipe_list.remove('N')
                return pipe_list
            else:
                return []
        if self._orientation == 1:
            if side == 'N' or side == 'S' or side == 'W':
                pipe_list.remove(side)
                pipe_list.remove('E')
                return pipe_list
            else:
                return []
        if self._orientation == 2:
            if side == 'N' or side == 'E' or side == 'W':
                pipe_list.remove(side)
                pipe_list.remove('S')
                return pipe_list
            else:
                return []
        if self._orientation == 3:
            if side == 'N' or side == 'S' or side == 'E':
                pipe_list.remove(side)
                pipe_list.remove('W')
                return pipe_list
            else:
                return []
        else:
            return

class Diagonals(Pipe):
    """Representation of a diagonals pipe in the game"""
    def __init__(self):
        """Initializes the diagonals pipe attributes."""
        super().__init__()

    def get_connected(self, side:str):
        """ Returns a list of sides connected to a diagonals pipe at a given
        orientation.

        Parameters:
        side(str): A side of the pipe.

        Returns:
        (list(str)): A list of all sides connected to the given side.
        """
        pipe_list = []
        if self._orientation == 0 or self._orientation == 2:
            if side == 'N':
                pipe_list.append('E')
                return pipe_list
            elif side == 'E':
                pipe_list.append('N')
                return pipe_list
            elif side == 'S':
                pipe_list.append('W')
                return pipe_list
            elif side == 'W':
                pipe_list.append('S')
                return pipe_list
            else:
                return pipe_list
        if self._orientation == 1 or self._orientation == 3:
            if side == 'S':
                pipe_list.append('E')
                return pipe_list
            elif side == 'E':
                pipe_list.append('S')
                return pipe_list
            elif side == 'N':
                pipe_list.append('W')
                return pipe_list
            elif side == 'W':
                pipe_list.append('N')
                return pipe_list
            else:
                return pipe_list
        else:
            return

class Overunder(Pipe):
    """Representation of an overunder pipe in the game"""
    def __init__(self):
        """Initializes the overunder pipe attributes."""
        super().__init__()

    def get_connected(self, side:str):
        """ Returns a list of sides connected to a overunder pipe at a given
        orientation.

        Parameters:
        side(str): A side of the pipe.

        Returns:
        (list(str)): A list of all sides connected to the given side.
        """
        pipe_list = []
        if side == 'N':
            pipe_list.append('S')
            return pipe_list
        elif side == 'S':
            pipe_list.append('N')
            return pipe_list
        elif side == 'E':
            pipe_list.append('W')
            return pipe_list
        elif side == 'W':
            pipe_list.append('E')
            return pipe_list
        else:
            return pipe_list
      
class SpecialPipe(Pipe):
    """ An abstract class representing a special type of pipe in the game."""
    def __init__(self, name = "", orientation = 0, selectable=False):
        """Constructs a special pipe.

        Parameters:
        name (str): Name of the special pipe.
        orientation (int): orientation of the pipe.
        selectable (bool): Returns True if not loaded into the game board. False otherwise.
        """
        super().__init__(name=name)
        self._id = 'special_pipe'
        self._class_name = 'SpecialPipe'
        self._name = name
        self._orientation = orientation
        self._selectable = selectable       
                   
    def __str__(self):
        """ Returns the string representation of the special pipe.

        Returns:
        (str): String representation of the special pipe.
        """
        return f"{self._class_name}({self._orientation})"

    def __repr__(self):
        """Returns official string representation of the special pipe.

        Returns:
        (str): String representation of the special pipe.
        """
        return self.__str__()

class StartPipe(SpecialPipe):
    """ Represents the start pipe in the game."""
    def __init__(self, orientation = 0):
        """Initializes the start pipe attributes.

        Parameters:
        orientation (int): orientation of the pipe.
        """
        super().__init__()
        self._class_name = 'StartPipe'
        self._name = 'start'
        self._orientation = orientation

    def get_connected(self, side=None):
        """ Returns the direction the start pipe is facing.

        Parameters:
        side(str): A side of the pipe. Set to None.

        Returns:
        (list(str)): A list of all sides connected to the given side.
        """
        pipe_list = [['N'], ['E'], ['S'], ['W']]
        if self._orientation in range(4):
            return pipe_list[self._orientation]
        else:
            return
                
class EndPipe(SpecialPipe):
    """ Represents the end pipe in the game."""
    def __init__(self, orientation = 0):
        """Initializes the end pipe attributes.

        Parameters:
        orientation (int): orientation of the pipe.
        """
        super().__init__()
        self._class_name = 'EndPipe'
        self._name = 'end'
        self._orientation = orientation
        
    def get_connected(self, side=None):
        """ Returns the opposite direction the end pipe is facing.

        Parameters:
        side(str): A side of the pipe. Set to None by default.

        Returns:
        (list(str)): A list of all sides connected to the given side.
        """
        pipe_list = [['S'], ['W'], ['N'], ['E']]
        if self._orientation in range(4):
            return pipe_list[self._orientation]
        else:
            return

class PipeGame:
    """
    A game of Pipes.
    """
    def __init__(self, game_file='game_1.csv'):
        """
        Construct a game of Pipes from a file name.

        Parameters:
            game_file (str): name of the game file.
        """
        
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self._board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], \
        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), \
        Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)]]

        self._playable_pipes = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self.end_pipe_positions()
        
    def get_board_layout(self):
        """Returns the playable board layout.

        Returns:
        (list(list(Tile,...))): A list of lists where each element is
                                an instance of a tile.
        """
        return self._board_layout 

    def get_playable_pipes(self):
        """Returns a dictionary of all the playable pipes (the pipe types)
        and number of times each pipe can be played.

        Returns:
        (dict(str:int)): dictionary with types of pipes and number able to be played
        """
        return self._playable_pipes

    def change_playable_amount(self, pipe_name: str, number: int):
        """Add the quantity of playable pipes of type specified by
        pipe_name to number (in the selection panel).

        Parameters:
        pipe_name(str): name of the pipe
        number(int): quantity of pipe
        """
        if pipe_name in self._playable_pipes:
            self._playable_pipes[pipe_name] += number

    def get_pipe(self, position: (int, int)):
        """Returns the Pipe at the position or the
        tile if there is no pipe at that position.

        Parameters:
        position(tuple(int,int)): row and column position in the board layout.

        Returns:
        (instance): Class instance in position of board layout.
        """
        return self._board_layout[position[0]][position[1]]      

    def set_pipe(self, pipe: Pipe, position: (int, int)):
        """
        Place the specified pipe at the given position in the game board.
        The number of available pipes of the relevant type is also updated.

        Parameters:
        pipe(instance): Instance of the pipe class.
        position(tuple(int,int)): row and column position in the board layout.
        """
        target = self.get_pipe(position) 
        check_special = isinstance(target, SpecialPipe)#checks if special pipe
        check_not_locked = target.can_select() #checks if tile is selectable
        if check_special == False:
            if check_not_locked == True:
                if self._playable_pipes[pipe.get_name()] > 0:
                    self._board_layout[position[0]][position[1]] = pipe 
                    self._playable_pipes[pipe.get_name()] -= 1 
        else:
            None
          
    def pipe_in_position(self, position: (int, int)):
        """
        Returns the pipe in the given position of the game board if there is
        a Pipe in the given position. Returns None if the position
        given is None or if the object in the given position is not a Pipe.

        Parameters:
        position(tuple(int,int)): row and column position in the board layout.

        Returns:
        (instance): Class instance in position of board layout.
        """
        target = self._board_layout[position[0]][position[1]] 
        is_pipe = isinstance(target, Pipe) #checks if target position is Pipe
        if is_pipe == True:
            return target
        else:
            return  

    def remove_pipe(self, position: (int, int)):
        """Removes the pipe at the given position from the board.

        Parameters:
        position(tuple(int,int)): row and column position in the board layout.
        """
        target = self.get_pipe(position) 
        check_special = isinstance(target, SpecialPipe)
        if self.pipe_in_position(position) is not None:
            if check_special == False:  
                self._playable_pipes[target.get_name()] += 1
                self._board_layout[position[0]][position[1]] = Tile('tile')
        else:
            None
                  
    def position_in_direction(self, direction:str, position: (int, int)):
        """ Returns the direction and position in the given direction
        from the given position, if the resulting position is within 
        the game grid. Returns None if the position would be invalid.

        Parameters:
        direction(str): direction (either N, S, E or W).
        position(tuple(int,int)): row and column position in the board layout.

        Returns:
        (tuple(str,(int, int))): direction and position from given direction and position 
        """
        if position[0] in range(6) and position[1] in range(6):
            if direction == 'N':
                if position[0] == 0:
                    return 
                else:
                    return ('S', (position[0]-1,position[1]))
            elif direction == 'S':
                if position[0] == 5:
                    return 
                else:
                    return ('N', (position[0]+1,position[1]))
            elif direction == 'E':
                if position[1] == 5:
                    return 
                else:
                    return ('W', (position[0],position[1]+1))
            elif direction == 'W':
                if position[1] == 0:
                    return 
                else:
                    return ('E', (position[0],position[1]-1))
        else:
            return 
                           
    def end_pipe_positions(self):
        """Find and save the start and end pipe positions from the
        game board.
        """
        for i, lst in enumerate(self._board_layout):
            for j, target in enumerate(lst):
                if type(target) == StartPipe:
                    self._starting_pos = (i,j)
                if type(target) == EndPipe:
                    self._ending_pos = (i,j)

    def get_starting_position(self):
        """Returns the position of the start pipe.

        Returns:
        (tuple(int, int): row and column position in the board layout.
        """
        return self._starting_pos
                    
    def get_ending_position(self):
        """Returns the position of the end pipe.

        Returns:
        (tuple(int, int): row and column position in the board layout.
        """
        return self._ending_pos
        
    def check_win(self):
        """
        (bool) Returns True  if the player has won the game False otherwise.
        """
        position = self.get_starting_position()
        pipe = self.pipe_in_position(position)
        queue = [(pipe, None, position)]
        discovered = [(pipe, None)]
        while queue:
            pipe, direction, position = queue.pop()
            for direction in pipe.get_connected(direction):
            
                if self.position_in_direction(direction, position) is None:
                    new_direction = None 
                    new_position = None
                else:
                    new_direction, new_position = self.position_in_direction(direction, position)
                if new_position == self.get_ending_position() and direction == self.pipe_in_position(
                        new_position).get_connected()[0]:
                    return True

                pipe = self.pipe_in_position(new_position)
                if pipe is None or (pipe, new_direction) in discovered:
                    continue
                discovered.append((pipe, new_direction))
                queue.append((pipe, new_direction, new_position))
        return False



    
def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()
