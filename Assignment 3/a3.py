import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from time import time
import random, os
from PIL import Image, ImageTk
import sys
from tkinter import filedialog



TASK_ONE = "t1"
TASK_TWO = "t2"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")
POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"

class BoardModel(object):
    """
    Stores and manages the internal game state. Represents the model class.
    """
    def __init__(self, grid_size, num_pokemon):
        """Initializes the BoardModel.
        
        Parameters:
        grid_size(int): The grid size of the game.
        num_pokemon(int): The number of pokemon in the game.
        """
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._game = UNEXPOSED * grid_size ** 2 
        self._num_pokeballs = 15   
        self._pokemon_locations = self.generate_pokemons()
       
    def generate_pokemons(self):
        """Pokemons will be generated and given a random index within the game.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = self._grid_size ** 2
        pokemon_locations = ()

        for _ in range(self._num_pokemon):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count-1)
            while index in pokemon_locations:
                index = random.randint(0, cell_count-1)
            pokemon_locations += (index,)
        return pokemon_locations
    
    def get_game(self):
        """Returns the current representation of the game string.
        
        Returns:
        (str): The string representation of the game.
        """
        return self._game

    def get_pokemon_locations(self):
        """Returns the index or indices of where pokemon are located relative to the game string.
        
        Returns:
        (tuple<int>): index or indicies of pokemon locations.
        """
        return self._pokemon_locations
    
    def num_pokeballs_left(self): 
        """Returns the number of pokepalls available to use.
        
        Returns:
        (int): number of pokeballs left.
        """
        count = self.get_num_attempted_catches()
        left = self._num_pokeballs - count
        return left 

    def get_num_attempted_catches(self):
        """Returns the number of pokeballs that have been placed in the game string.
        
        Returns:
        (int): Number of pokeballs placed.
        """
        count =  self._game.count(FLAG)
        if count <= self._num_pokeballs:
            return count
        else:
            return self._num_pokeballs      
    
    def get_num_pokemon(self):
        """Returns the number of pokemon that are loaded and hidden in the game.
        
        Returns:
        (int): Number of hidden pokemon loaded in the game.
        """
        return self._num_pokemon

    def position_to_index(self, position):
        """Convert the row, column coordinate in the game board to the game strings index.
        
        Returns:
        (int): The index of the cell in the game string.
        """
        x, y = position
        return x * self._grid_size + y

    def replace_character_at_index(self, index, character):
        """A specified index in the game string at the specified index is replaced by
        a new character.
        
        Returns:
        (str): The updated game string.
        """
        self._game = self._game[:index] + character + self._game[index + 1:]

    def neighbour_directions(self, index, grid_size):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, direction)
            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours    

    def index_in_direction(self, index, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        Parameters:
            index (int): The index in the game string.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
        # convert index to row, col coordinate
        col = index % self._grid_size
        row = index // self._grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1
        if not (0 <= col < self._grid_size and 0 <= row < self._grid_size):
            return None
        return self.position_to_index((row, col))

    def number_at_cell(self, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
        if self._game[index] != UNEXPOSED:
            return int(self._game[index]) 
        number = 0
        for neighbour in self.neighbour_directions(index, self._grid_size):
            if neighbour in self._pokemon_locations:
                number += 1
        return number    

    def big_fun_search(self, index):
        """Searching adjacent cells to see if there are any Pokemon present.
        
        Parameters:
            index (int): Index of the currently selected cell.

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []
            
        if self._game[index] == FLAG:
            return queue

        number = self.number_at_cell(index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node, self._grid_size):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if self._game[neighbour] != FLAG:
                    number = self.number_at_cell(neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def flag_cell(self, index):
        """Toggle Flag on or off at selected index. If the selected index is already
        revealed, the game would return with no changes.
        
        Returns:
        (str): The updated game string.
        """
        if self._game[index] == FLAG:
            self._game = self._game[:index] + UNEXPOSED + self._game[index + 1:]

        elif self._game[index] == UNEXPOSED:
            self._game = self._game[:index] + FLAG + self._game[index + 1:]

    def check_win(self):
        """Checks if the player has won the game.
        
        Returns:
        (bool): True if the player has won the game, false if not.
        """
        return UNEXPOSED not in self._game and self._game.count(FLAG) == len(self._pokemon_locations)
    
    def check_loss(self, index):
        """Checks if the player has lost the game and updates the game string accordingly.
        
        Returns:
        (bool): True if the player has lost the game, false if not.        
        """
        if index in self._pokemon_locations:
            for i in self._pokemon_locations:
                self.replace_character_at_index(i, POKEMON)
            return True            
        
    def reveal_cells(self, index):
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (str): The updated game string
        """

        number = self.number_at_cell(index)
        self.replace_character_at_index(index, str(number))
        clear = self.big_fun_search(index)
        
        for i in clear:
            if self._game[i] in self._pokemon_locations:
                self.check_loss(index)
            if self._game[i] != FLAG:
                number = self.number_at_cell(i)
                self.replace_character_at_index(i, str(number))
                    
        return self._game
    
    def reset(self, new):
        """Resets the game string to its original form.
        
        Returns:
        (str): The original game string.
        """
        self._game = new

    def ball_reset(self, ball):
        """Resets the number of pokeballs to be placed.
        
        Returns:
        (int): Number of pokeballs to be placed.
        """
        self._num_pokeballs = ball

    def loc_reset(self, pokemon):
        """Resets the index or indices of where pokemon are located relative to the game string.
        
        Returns:
        (tuple<int>): index or indicies of pokemon locations.
        """
        self._pokemon_locations = eval(pokemon)
    
  
class PokemonGame:
    """Manages the communication between the model and view classes. Represents the controller class.
    """
    def __init__(self, master, grid_size = 10, num_pokemon = 15, task = TASK_ONE):
        """Initializes PokemonGame.
        
        Parameters:
        master(tk.Tk): Master window.
        grid_size(int): Size of game. Set to 10.
        num_pokemon(int): The number of pokemon in the game. Set to 15.
        task(str): String constant to allow different modes of the game to be run. Set to TASK_ONE.
        """
        self._master = master
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._model = BoardModel(self._grid_size, self._num_pokemon)
        self._game = self._model.get_game()
        self._task = task
        #Initialize task one attributes
        if self._task == TASK_ONE:
            self._board = BoardView(self._master, self._grid_size, select_left = self.select_left, select_right = self.select_right) 
            self._board.pack(side = tk.TOP)
            self._board.draw_board(self._game)
        #Initialize task two attributes    
        elif self._task == TASK_TWO:
            self._image_view = ImageBoardView(self._master, self._grid_size, select_left = self.select_left, select_right = self.select_right)
            self._image_view.pack(side = tk.TOP)
            self._image_view.draw_board(self._game)
            self._status = StatusBar(self._master, self.restart_game, self.new_game)
            self._status.update_ball_info(self._model._num_pokeballs)
            self.menu()
             
        self._filename = None

    def menu(self):
        """Creates the file menu which is displayed in TASK_TWO mode.
        """
        #File menu
        self._menubar = tk.Menu(self._master)
        #Tell master what it's menu is
        self._master.config(menu = self._menubar)
        self._filemenu = tk.Menu(self._menubar)
        self._menubar.add_cascade(label = "File", menu = self._filemenu)
        self._filemenu.add_command(label = "High scores", command = self.high_scores)
        self._filemenu.add_command(label = "Save game", command = self.save_game)
        self._filemenu.add_command(label = "Load game", command = self.load_game)
        self._filemenu.add_command(label = "Restart game", command = self.restart_game)
        self._filemenu.add_command(label = "New game", command = self.new_game)
        self._filemenu.add_command(label = "Quit", command = self._master.destroy)

    def high_scores(self):
        """Creates and populates the high scores window which is displayed in TASK_TWO mode.
        
        Reads the high scores file to retrieve the high score information.
        
        Updates the labels with the relevant high score information.
        
        Creates an exception if less than 3 scores have been recorded and displays only those.
        """
        #Create the window and its labels and button
        self._window = tk.Toplevel(self._master)
        self._window.title("Top 3")
        
        self._window_label = tk.Label(self._window, text = "High Scores", font = ("Courier New", 24, "bold"), fg = "white", bg = "indian red", relief = "raised")
        self._window_label.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        self._window_frame = tk.Frame(self._window, height = 30, bg = "white")
        self._window_frame.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)
        
        self._first = tk.Label(self._window, bg = "white")
        self._first.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        self._second = tk.Label(self._window, bg = "white")
        self._second.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        self._third = tk.Label(self._window, bg = "white")
        self._third.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        self._button = tk.Button(self._window_frame, text = "Done", command = self._window.destroy)
        self._button.place(relx = 0.5, rely = 0.1, anchor = "n")
        
        #set file name and interpret file data
        self._scores = "highscores.txt"
        if os.path.isfile(self._scores):
            try:
                fd = open(self._scores, "r")
                self._l = fd.readlines()
                self._var = [i.rstrip("\n") for i in self._l]
                #Puts every second line of the file into a list. These lines hold the seconds values.
                #The other lines hold the names.
                self._new_list = self._var[0::2]
                #Sort them in ascending numerical order
                self._new_list.sort(key = int)
                
                #Find top score
                self._1st_line_num = self.find_line_num(self._new_list[0], self._scores)
                self._1st_name_num = self._1st_line_num +1
                #Convert the string values from the text file
                self._1st_time = int(self._var[self._1st_line_num])
                self._1st_name = self._var[self._1st_name_num]
                #Update the label with the data
                self.config_label(self._1st_time, self._first, self._1st_name) 

                #Find 2nd score
                self._2nd_line_num = self.find_line_num(self._new_list[1], self._scores)
                #If the time is the same as first place, keep searching list for 2nd occurence of time.
                if self._2nd_line_num == self._1st_line_num:
                    line = self._var.index(self._new_list[1], self._1st_line_num+1)
                    self._2nd_line_num = line
                self._2nd_name_num = self._2nd_line_num +1
                self._2nd_time = int(self._var[self._2nd_line_num])
                self._2nd_name = self._var[self._2nd_name_num]
                self.config_label(self._2nd_time, self._second, self._2nd_name)
        
                #Find 3rd score
                self._3rd_line_num = self.find_line_num(self._new_list[2], self._scores)
                #If time is the same as first or second, keep searching for correct occurrence by line.
                if self._3rd_line_num == self._1st_line_num:
                    line = self._var.index(self._new_list[1], self._1st_line_num+1)
                    self._3rd_line_num = line
                if self._3rd_line_num == self._2nd_line_num:
                    line = self._var.index(self._new_list[2], self._2nd_line_num+1)
                    self._3rd_line_num = line
                self._3rd_name_num = self._3rd_line_num +1
                self._3rd_time = int(self._var[self._3rd_line_num])
                self._3rd_name = self._var[self._3rd_name_num]
                self.config_label(self._3rd_time, self._third, self._3rd_name)
            #Handle exceptions if the highscores file is not populated enough to generate 3 scores.
            except IndexError:
                return

    def win_entry(self):
        """Creates a window which is displayed if the game is won in TASK_TWO mode. 
        """
        self._window = tk.Toplevel(self._master)
        self._window.title("You win!")
        
        self._window_frame = tk.Frame(self._window, height = 100, bg = "white")
        self._window_frame.pack(fill = tk.BOTH, expand = True)
        
        self._window_label = tk.Label(self._window_frame, bg = "white", text = "You won in {0}m and {1}s! Enter your name:".format(self._status._minutes, self._status._seconds))
        self._window_label.pack()
        
        self._window_entry = tk.Entry(self._window_frame)
        self._window_entry.pack()
        
        self._enter_button = tk.Button(self._window_frame, text = "Enter", command = self.button_click)
        self._enter_button.pack(side = tk.BOTTOM)


    def button_click(self):
        """Writes to or creates a highscores file (if one doesn't already exist) when a player
        wins the game in TASK_TWO mode.
        """
        self._scores = "highscores.txt"
        #Convert the timer score to seconds to enable simpler score comparison when read.
        total_seconds = self._status._minutes*60 + self._status._seconds
        #Retrieve the name of the player
        name = self._window_entry.get()
        #Set name to unknown if player doesn't enter a name.
        if name == "":
            name = "Unknown"
        fd = open(self._scores, "a+")
        fd.write(str(total_seconds)+"\n")
        fd.write(str(name)+"\n")
        fd.close()
        self._window.destroy()
        #Once score recorded, trigger the win (play again) messagebox to appear.
        self.show_message("win")

    def config_label(self, seconds, label_name, player):
        """Updates the high scores labels with the players names and their time of completion.
        
        Parameters:
        seconds(int): Number of seconds the game was completed in.
        label_name(tk.Widget): Name of the label to update.
        player(str): Name of player.
        """
        if seconds <= 59:
            label_name.config(text = "{0}: {1}s".format(player, seconds))
        else:
            self._mins = divmod(seconds, 60)
            label_name.config(text = "{0}: {1}m {2}s".format(player, self._mins[0], self._mins[1]))
        
        
    def find_line_num(self, item, filename):
        """Finds the line number in the highscores file for a specific item.
        
        Parameters:
        item(str): The content of a line in the text file.
        filename(str): The name of the file to read.
        
        Returns:
        (int): Line number of item in the file. 
        """
        with open(filename, "r") as f:
            for i, line in enumerate(f): 
                line = line.rstrip()
                if item == line:
                    return i       

    def save_game(self):
        """Saves the current game state to a text file in TASK_TWO mode.
        """
        #Pause the timer upon selecting to save game.
        self._status.pause_timer()
        #Ask for a file name and write the parameters to file
        if self._filename is None:
            filename = filedialog.asksaveasfilename()
            if filename:
                self._filename = filename
        if self._filename:
            fd = open(self._filename + ".txt", "w", encoding = "utf-8")
            fd.write(self._game+"\n")
            fd.write(str(self._grid_size)+"\n")
            fd.write(str(self._num_pokemon)+"\n")
            fd.write(str(self._model._num_pokeballs)+"\n")
            fd.write(str(self._model._pokemon_locations)+"\n")
            fd.write(str(self._status._minutes)+"\n")
            fd.write(str(self._status._seconds)+"\n")
            fd.close()
        #If the player exits the menu without saving, unpause and resume timer.
        self._status.pause_timer()
        self._status.start_timer()

    def load_game(self):
        """Loads a saved game in TASK_TWO mode.
        
        Prints an error message if the user attempts to load an incompatible file.
        """
        #Pause the timer upon selecting to load a game.
        self._status.pause_timer()
        try:
            #Request a save file to load and update the game for its parameters.
            filename = filedialog.askopenfilename()
            if filename:
                self._filename = filename
                fd = open(filename, "r", encoding = "utf-8")
                var = fd.readlines()
                self._game = self._model.reset(var[0])
                self._model.ball_reset(int(var[3]))
                self._grid_size = int(var[1])
                self._model._grid_size = self._grid_size
                self._image_view._grid_size = self._grid_size
                self._num_pokemon = int(var[2])
                self._model.loc_reset(var[4])
                self._status.load_time((int(var[5])),(int(var[6])))
                self.reset_dynamic_labels()
                self.redraw()
                fd.close()
        #Handle exceptions when the file is of incorrect file type or contains unreadable formatting.
        except (IOError, ValueError, UnicodeDecodeError):
            print("There is something wrong with the file you selected")
        #If the player exits the menu without saving, unpause and resume timer.
        self._status.pause_timer()
        self._status.start_timer()
           
    def select_left(self, position):
        """Handles the left clicking functionality of the game.
        
        Parameters:
        position(tuple<int>): x,y coordinates of the click on the game board.
        """
        index = self.get_index(position[1], position[0])
        if self._game[index] == FLAG:
            return
        #If the game is not over, reveal cells and redraw.
        elif self.check_game_over(index) == False:
            self._model.reveal_cells(index)
            self.redraw()
            self.check_game_over(index)            
    
    def select_right(self, position):
        """Handles the right clicking functionality of the game.
        
        Parameters:
        position(tuple<int>): x,y coordinates of the click on the game board.
        """
        index = self.get_index(position[1], position[0])
        #Handle flagging for different game modes.
        if self._task == TASK_ONE:
            self._model.flag_cell(index)
        if self._task == TASK_TWO:
            if self._game.count(FLAG) < self._model._num_pokeballs or self._game[index] == FLAG:
                self._model.flag_cell(index)
                self.reset_dynamic_labels()
            else:
                return
        self.redraw()
        #Determine the win message to display depending on game mode
        if self._model.check_win():
            if self._task == TASK_ONE:
                self.show_message("win")
            if self._task == TASK_TWO:
                self._status.pause_timer()
                self.win_entry()
       
    def get_index(self, coord_x, coord_y):
        """Takes the x and y coordinates of a cell tag click and converts it to the game string index.
        
        Parameters:
        coord_x(str): String representation of the x coordinate of a cell tag click.
        coord_y(str): String representation of the y coordinate of a cell tag click.
        
        Returns:
        (int): Index of position in the game string.
        """
        index = self._model.position_to_index((int(coord_x[0]), int(coord_y[1])))
        return index
                                                
    def draw(self):
        """Draws the game board based on the game string.
        """
        if self._task == TASK_ONE:
            self._board.draw_board(self._game) 
        else:
            self._image_view.draw_board(self._game) 
                
    def redraw(self):
        """Redraws the board from the updated game string.
        """
        self._game = self._model.get_game()
        self.draw()
           
    def check_game_over(self, index):
        """Checks if the game has been won or lost.
        
        Parameters:
        index(int): Index of the position in the game string.
        
        Returns:
        (bool): False if the game is not over.
        """
        #Check game won and handle messages to display
        if self._model.check_win():
            if self._task == TASK_ONE:
                self.show_message("win")
            if self._task == TASK_TWO:
                self._status.pause_timer()
                self.win_entry()
        #Check game lost and handle messages to display
        elif self._model.check_loss(index):
            if self._task == TASK_TWO:
                self._status.pause_timer()
            self.redraw()
            self.show_message("lose")
        else: 
            return False
    
    def reset_dynamic_labels(self):
        """Updates the labels in the StatusBar.
        """
        self._status.update_attempt_info(self._model.get_num_attempted_catches())
        self._status.update_ball_info(self._model.num_pokeballs_left())
        self._status.update_ball_img(self._model.num_pokeballs_left())
        
    def restart_game(self):
        """Resets the game so the same board can be played again.
        """
        game = UNEXPOSED * self._grid_size ** 2 
        self._model.reset(game)
        self._game = self._model.get_game()
        self.redraw()  
        self.reset_dynamic_labels()
        self._status.reset_timer()
    
    def new_game(self):
        """Resets and creates a new game with different pokemon locations.
        """
        self.restart_game()
        self._model.__init__(self._grid_size, self._num_pokemon)
        
    def show_message(self, outcome):
        """Creates the win / lose messages to display based on the game mode.
        
        Parameters:
        outcome(str): Outcome of the game.
        """
        if self._task == TASK_ONE:
            if outcome == "win":
                messagebox.showinfo("Game Over", "You won!")
                self._master.destroy()
            else:
                messagebox.showinfo("Game Over", "You lost!")
                self._master.destroy()
            sys.exit(0)
        #Task two messages
        elif outcome == "win":
            popup = messagebox.askquestion("Game Over", "You won! Would you like to play again?")
            self.handle_popup(popup)          
        else:
            popup = messagebox.askquestion("Game Over", "You lost! Would you like to play again?")
            self.handle_popup(popup)
    
    def handle_popup(self, popup):
        """Handles the Yes / No options of the win and lose messages in TASK_TWO mode.
        
        popup(str): Yes or no options of the messagebox.
        """
        if popup == "yes":
            self.new_game()
            self._status.set_running()
            self._status.reset_timer()
        else:
            self._master.destroy()

        
class BoardView(tk.Canvas):
    """Represents the GUI for the board and the view class.
    """
    def __init__(self, master, grid_size, board_width = 600, select_left = None, select_right = None, *args, **kwargs):
        """Initializes BoardView.
        
        Parameters:
        master(tk.Widget): Widget within which the game is held.
        grid_size(int): Size of game.
        board_width(int): Width of the board. Set to 600 pixels.
        select_left(callable): Function or method to call when a cell is selected with left click.
        select_right(callable): Function or method to call when a cell is selected with right click.
        """
        super().__init__(master, width = board_width, height = board_width, bg = "white", borderwidth = 1, highlightthickness = 0, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self.select_left = select_left
        self.select_right = select_right
        
        self._label = tk.Label(self._master, text = "Pokemon: Got 2 Find Them All!", font = ("Courier New", 24, "bold"), fg = "white", bg = "indian red", relief = "raised")
        self._label.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

              
    def draw_board(self, board): 
        """Draws the game board in BoardView using coloured rectangles.
        
        Parameters:
        board(str): The current game board (game string).
        """
        #Set the cell width
        self._cell_width = self._board_width//self._grid_size
        #Set the cell coordinates for drawing rectangles
        rec_top_left_x = 0
        rec_top_left_y = 0
        rec_bottom_right_x = self._cell_width
        rec_bottom_right_y = self._cell_width
        #Set index
        index = 0
        
        for j in range(0, self._grid_size, 1):
            for i in range(0, self._grid_size, 1):
                #Create cell tags
                cell_tag = str((i, j))
                coord_i = i + self._cell_width
                coord_j = j + self._cell_width
                #Revealed cells
                if board[index].isdigit():
                    tag = self.create_rectangle([rec_top_left_x, rec_top_left_y], [rec_bottom_right_x, rec_bottom_right_y], fill = "light green", tags = cell_tag)
                    self.create_text((rec_top_left_x + 0.5 * self._cell_width, rec_top_left_y + 0.5 * self._cell_width), text = board[index])
                #Flagged cells
                elif board[index] == FLAG:
                    tag = self.create_rectangle([rec_top_left_x, rec_top_left_y], [rec_bottom_right_x, rec_bottom_right_y], fill = "red", tags = cell_tag)
                #Pokemon cells
                elif board[index] == POKEMON:
                    tag = self.create_rectangle([rec_top_left_x, rec_top_left_y], [rec_bottom_right_x, rec_bottom_right_y], fill = "yellow", tags = cell_tag)
                #Unrevealed cells
                else:
                    tag = self.create_rectangle([rec_top_left_x, rec_top_left_y], [rec_bottom_right_x, rec_bottom_right_y], fill = "green", tags = cell_tag)
                #Set bindings to cell tags
                self.tag_bind(tag, "<ButtonPress-1>", self.left_event)
                self.tag_bind(tag, "<ButtonPress-2>", self.right_event)
                self.tag_bind(tag, "<ButtonPress-3>", self.right_event)
                self.tag_bind(tag, "<Enter>",  lambda event, border = tag:self.border_event(event, border))
                self.tag_bind(tag, "<Leave>", lambda event, border = tag:self.border_event(event, border))
                #Increment index and position for next column of rectangles
                index += 1  
                rec_top_left_x += self._cell_width
                rec_bottom_right_x += self._cell_width
            #Increment position for next row of rectangles
            rec_top_left_x = 0
            rec_top_left_y += self._cell_width
            rec_bottom_right_x = self._cell_width
            rec_bottom_right_y += self._cell_width                       
                
    def left_event(self, event): 
        """Links the left click bindings to the cell tags and left click functionality.
        
        Parameters:
        event(tk.Event): The event occurring on the board.
        """
        #Find closest cell
        loc = self.find_closest(event.x, event.y)[0]
        #Get tag
        cell_tags = self.gettags(loc)
        #Utilize left click functionality
        self.select_left(cell_tags)       
    
    def right_event(self, event):
        """Links the right click bindings to the cell tags.
        
        Parameters:
        event(tk.Event): The event occurring on the board.
        """
        #Find closest cell
        loc = self.find_closest(event.x, event.y)[0]
        #Get tag
        cell_tags = self.gettags(loc)
        #Utilize right click functionality
        self.select_right(cell_tags)

    def border_event(self, event, border):
        """Changes the colour of a cell when hovered and changes it back when unhovered.
        
        Parameters:
        event(tk.Event): The event occurring on the board.
        border(tk.Widget): The rectangle being changed.
        """
        #Set event values
        HOVER = '7'
        UNHOVER = '8'
        #Change border colour
        if event.type == HOVER:
            self.itemconfig(border, outline = "yellow", width = 2)
        elif event.type == UNHOVER:
            self.itemconfig(border, outline = "black", width = 1)


class ImageBoardView(BoardView):
    """Uses images to display the game. Extends the BoardView class.
    """ 
    def __init__(self, master, grid_size, select_left = None, select_right = None, *args, **kwargs):
        """Initializes the ImageBoardView.
        """
        BoardView.__init__(self, master, grid_size)
        self._master = master
        self._grid_size = grid_size
        self.select_left = select_left
        self.select_right = select_right
        
    def draw_board(self, board):
        """Draws the game board in ImageBoardView using images.
        
        Parameters:
        board(str): The current game board (game string).
        """ 
        #Set cell width and image resize constants
        self._cell_width = self._board_width//self._grid_size
        self._resized = (self._cell_width, self._cell_width)
        #Set the cell coordinates for drawing images
        rec_top_left_x = 0
        rec_top_left_y = 0
        rec_bottom_right_x = self._cell_width
        rec_bottom_right_y = self._cell_width
        #Set index
        index = 0
        #Create image list to store images
        self._images = []  
        self._unrevealed = self.get_resized_image("unrevealed") 
        self._pokeball = self.get_resized_image("pokeball")
        #Create revealed cell image dictionary           
        self._num_dict = self.generate_dict()
               
        for j in range(0, self._grid_size, 1):
            for i in range(0, self._grid_size, 1):
                cell_tag = str((i, j))
                #Set centre of cell coordinate for placing images 
                self._centre_x = rec_top_left_x + 0.5 * self._cell_width
                self._centre_y = rec_top_left_y + 0.5 * self._cell_width
                #Revealed images
                if board[index] in self._num_dict.keys():
                    #Get corresponding image for index (ie. index of 1 gets image for 1 neighbour).
                    num_image = self._num_dict[board[index]]
                    #Store images
                    self._images.append(num_image)
                    num_image.image = num_image
                    tag = self.create_image(self._centre_x, self._centre_y, image = num_image, tags = cell_tag)
                #Flagged images
                elif board[index] == FLAG:
                    tag = self.create_image(self._centre_x, self._centre_y, image = self._pokeball, tags = cell_tag)
                #Pokemon images
                elif board[index] == POKEMON:
                    #Generate random pokemon and store their images
                    pokemon = self.gen_rand_pokemon()
                    pokemon_image = self.get_resized_image(pokemon)
                    self._images.append(pokemon_image)
                    pokemon_image.image = pokemon_image
                    tag = self.create_image(self._centre_x, self._centre_y, image = pokemon_image, tags = cell_tag)
                #Unrevealed images
                else:
                    tag = self.create_image(self._centre_x, self._centre_y, image = self._unrevealed, tags = cell_tag)
                #Set bindings to cell tags
                self.tag_bind(tag, "<ButtonPress-1>", self.left_event)
                self.tag_bind(tag, "<ButtonPress-2>", self.right_event)
                self.tag_bind(tag, "<ButtonPress-3>", self.right_event)
                if board[index] == UNEXPOSED:
                    self.tag_bind(tag, "<Enter>",  lambda event, img = tag:self.image_event(event, img))
                    self.tag_bind(tag, "<Leave>", lambda event, img = tag:self.image_event(event, img))
                #Increment index and position for next column of images
                index += 1  
                rec_top_left_x += self._cell_width
                rec_bottom_right_x += self._cell_width
            #Increment position for next row of images
            rec_top_left_x = 0
            rec_top_left_y += self._cell_width
            rec_bottom_right_x = self._cell_width          
            rec_bottom_right_y += self._cell_width


    def image_event(self, event, img):
        """Changes the image of a cell when hovered and changes it back when unhovered.
        
        Parameters:
        event(tk.Event): The event occurring on the board.
        img(tk.Widget): The image being changed.
        """
        #Set event values
        HOVER = '7'
        UNHOVER = '8'
        #Change image
        if event.type == HOVER:
            unrevealed_moved = self.get_resized_image("unrevealed_moved")
            self._images.append(unrevealed_moved)
            unrevealed_moved.image = unrevealed_moved
            self.itemconfig(img, image = unrevealed_moved)
        elif event.type == UNHOVER:
            unrevealed = self.get_resized_image("unrevealed")
            self._images.append(unrevealed)
            unrevealed.image = unrevealed
            self.itemconfig(img, image = unrevealed)
    
    def gen_rand_pokemon(self):
        """Generates a random pokemon from the pokemon sprites subfolder.
        
        Returns:
        (str): file name for the random pokemon.
        """
        folder = "pokemon_sprites/"
        p_list = ["charizard", "cyndaquil", "pikachu", "psyduck", "togepi", "umbreon"]
        ran_img = random.choice(p_list)
        file = folder + ran_img
        return  file
    
    def get_resized_image(self, image_name):
        """Retrieves images from the images subfolder and resizes them to fit the game board.
        
        Paramaters:
        image_name(str): name of the image to retrieve.
        
        Returns:
        (ImageTk.PhotoImage): Image to display.
        """
        try:
            image = ImageTk.PhotoImage((Image.open("images/" + image_name + ".png")).resize(self._resized, Image.ANTIALIAS))
        except tk.TclError:
            image = ImageTk.PhotoImage((Image.open("images/" + image_name +  ".gif")).resize(self._resized, Image.ANTIALIAS))
        return image
    
    def generate_dict(self):
        """Generates a dictionary of the different revealed cell images.
        
        Returns:
        img_dict(dictionary): dictionary of image files.
        """
        img_dict = {}
        num_list = ["zero_adjacent", "one_adjacent", "two_adjacent", "three_adjacent", "four_adjacent", "five_adjacent", "six_adjacent", "seven_adjacent", "eight_adjacent"]
        keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        values = []
        for i in num_list:
            #Create images and add them to a list
            img = self.get_resized_image(i) 
            values.append(img)
        #Create the image dictionary 
        img_dict = dict(zip(keys, values)) 
        return img_dict
   
        
class StatusBar(tk.Frame):
    """Frame for widgets displaying the current status of the game.
    """
    def __init__(self, master, restart_game = None, new_game = None):
        """Initializes StatusBar.
        
        Parameters:
        master(tk.Widget): Widget within which the StatusBar widgets are held.
        restart_game(callable): Function or method to call when a game is restarted.
        new_game(callable): Function or method to call when a new game is made.
        """
        super().__init__(master)
        self._master = master
        self.restart_game = restart_game
        self.new_game = new_game
        
        self._frame = tk.Frame(self._master, height = 100, width = 600, bg = "white")
        self._frame.pack(side=tk.BOTTOM)
        
        pokeball_img = get_image("full_pokeball")
        self._pokeball_label = tk.Label(self._frame, image = pokeball_img, borderwidth = 0, highlightthickness = 0)
        self._pokeball_label.image = pokeball_img
        self._pokeball_label.place(relx = 0.1, rely = 0.3)
        
        self._num_attempted = tk.Label(self._frame, text = "0 attempted catches", bg = "white")
        self._num_attempted.place(relx = 0.2, rely = 0.4, anchor = "w")
        
        self._pokeballs_left = tk.Label(self._frame, bg = "white")
        self._pokeballs_left.place(relx = 0.2, rely = 0.65, anchor = "w")
        
        clock_img = get_image("clock")
        self._clock_label = tk.Label(self._frame, image = clock_img, borderwidth = 0, highlightthickness = 0)
        self._clock_label.image = clock_img
        self._clock_label.place(relx = 0.5, rely = 0.3)
        
        self._elapsed = tk.Label(self._frame, text = "Time elapsed", bg = "white")
        self._elapsed.place(relx = 0.65, rely = 0.5, anchor = "s")
        
        self._timer = tk.Label(self._frame, text = "0m 0s", bg = "white")
        self._timer.place(relx = 0.65, rely = 0.75, anchor = "s")
        self._timer_tick = self._timer.after(1000, self.start_timer)

        self._new_game_button = tk.Button(self._frame, text = "New game", command = self.new_game_func)
        self._new_game_button.place(relx = 0.85, rely = 0.2, anchor = "n")
        
        self._restart_button = tk.Button(self._frame, text = "Restart game", command = self.restart_func)
        self._restart_button.place(relx = 0.85, rely = 0.8, anchor = "s")
        
        self._running = True
        self._clear = True
        self._seconds = 0
        self._minutes = 0
        
    def new_game_func(self):
        """Calls the new_game function.
        """
        self.new_game()
    
    def restart_func(self):
        """Calls the restart_game function.
        """
        self.restart_game()
    
    def update_attempt_info(self, count):
        """Updates the num_attempted label with the number of pokeballs placed.
        
        Parameters:
        count(int): Number of pokeballs placed.
        """
        self._num_attempted.config(text = str(count) + " attempted catches")
        
    def update_ball_info(self, count):
        """Updates the pokeballs_left label with the number of pokeballs left.
        
        Parameters:
        count(int): Number of pokeballs left.
        """
        self._pokeballs_left.config(text = str(count) + " pokeballs left")
    
    def update_ball_img(self, count):
        """Changes the pokeball_label image based on the number of pokeballs left.
        
        Parameters:
        count(int): Number of pokeballs left.
        """
        self._images = []
        if count >= 1:
            img = get_image("full_pokeball")
            self._images.append(img)
            img.image = img
            self._pokeball_label.config(image = img)
        else:
            img = get_image("empty_pokeball")
            self._images.append(img)
            img.image = img
            self._pokeball_label.config(image = img)
                
    def start_timer(self):
        """Starts the game timer
        """
        if self._running == True:
            self._seconds += 1
            if self._seconds == 60:
                self._minutes += 1
                self._seconds = 0
            self._timer.configure(text="{0}m {1}s".format(self._minutes, self._seconds))
            self._timer_tick = self._timer.after(1000, self.start_timer)
                                           
    def pause_timer(self):
        """Toggles the game timer to pause.
        """
        self._running = not self._running
    
    def reset_timer(self):
        """Resets the game timer to zero.
        """
        self._timer.after_cancel(self._timer_tick)
        self.start_timer()
        if self._minutes != 0:
            self._minutes = 0
        if self._seconds != 0:
            self._seconds = 0
            self._timer.configure(text="{0}m {1}s".format(self._minutes, self._seconds))
                
    def load_time(self, minutes, seconds):
        """Sets the minutes and seconds of the game.
        
        Parameters:
        minutes(int): Number of minutes.
        seconds(int): Number of seconds.
        """
        self._minutes = minutes
        self._seconds = seconds

    def set_running(self):
        """Allows the clock to start running.
        """
        self._running = True
        
            
def get_image(image_name):
    """Retrieves an image in its original size.
    
    Parameters:
    image_name(str): Name of the image.
    
    Returns:
    image(ImageTk.PhotoImage): Image to be displayed.
    """
    try:
        image = ImageTk.PhotoImage((Image.open("images/" + image_name + ".png")))
    except tk.TclError:
        image = ImageTk.PhotoImage((Image.open("images/" + image_name +  ".gif")))
    return image
        

def main():
    """Runs the main game.
    """
    root = tk.Tk()
    root.title("Pokemon: Got 2 Find Them All!")

    PokemonGame(root)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    main()

      
