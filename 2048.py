# 2048 will have a board class, that will have all the features to print and move around it's component parts
from copy import deepcopy
import random


class Board():
    def __init__(self, board = None):
        # What things do we need for a 2048 board, we will need a data_store that wilk keep track of all numbers at each location
        self.blank = '.'
        self.game_over = False # just an initialisation for the game over attribute
        self.position = {}
        if board == None:
            self.board_init()
        else:
            self.__dict__ = deepcopy(board.__dict__)
        
    def board_init(self):
        # every board must be randomly started with 2 2's somewhere on the board
        for i in range(4):
            for j in range(4):
                self.position[i, j] = self.blank
        # Now let's choose what squares to put the numbers at
        numbers = random.sample(range(16),2)
        row1 = int(int(numbers[0])/int(4))
        column1 = numbers[0] % int(4)
        row2 = int(int(numbers[1])/int(4))
        column2 = numbers[1] % int(4)
        # Update position
        self.position[row1, column1] = 2
        self.position[row2, column2] = 2
        self.game_over = False
    
    def __str__(self):  
        # Let Chatgpt handle the presentation part, it did way better presentation then i did
        # I just implemented same spaced numbers that looked bad when double and triple digit number came in
        max_num_length = max(len(str(num)) for num in self.position.values())
        cell_width = max_num_length + 2

        line = ""
        for i in range(4):
            for j in range(4):
                cell_value = str(self.position[(i, j)]) if self.position[(i, j)] != 0 else "."
                line += cell_value.center(cell_width)
            line += "\n"
        line += "-" * (cell_width * 4)
        return line
        
    def up_gravity(self): # up gravity checked, working
        #Here we will push all the block as much as possible to the corners
        #For different key presses will have to have different gravity
        for i in range(3, 0, -1): # this range(3, -1, 0) is basically giving a list of 3, 2, 1
            for j in range(3, -1, -1): # we want to have gravity over all the columns here
                if self.position[i-1, j] == '.':
                    self.position[i-1, j], self.position[i, j] = self.position[i, j], self.position[i-1, j]
        for i in range(3, 0, -1): # this range(3, -1, 0) is basically giving a list of 3, 2, 1
            for j in range(3, -1, -1): # we want to have gravity over all the columns here
                if self.position[i-1, j] == '.':
                    self.position[i-1, j], self.position[i, j] = self.position[i, j], self.position[i-1, j]
        board = Board(self)
        return board # we return a board even though we can update the previous board
        # this is because we want to possibly feed these boards into our mcts algorithm

    def down_gravity(self): # down gravity, kinda like up_gravity
        for i in range(3):
            for j in range(4):
                if self.position[i+1, j] == '.':
                    self.position[i+1, j], self.position[i, j] = self.position[i, j], self.position[i+1, j]
        for i in range(3):
            for j in range(4):
                if self.position[i+1, j] == '.':
                    self.position[i+1, j], self.position[i, j] = self.position[i, j], self.position[i+1, j]
        board = Board(self)
        return board
    
    def left_gravity(self): # left gravity is kinda like up_gravity also
        for j in range(3, 0, -1): 
            for i in range(3, -1, -1): 
                if self.position[i, j-1] == '.':
                    self.position[i, j-1], self.position[i, j] = self.position[i, j], self.position[i, j-1]
        for j in range(3, 0, -1): 
            for i in range(3, -1, -1): 
                if self.position[i, j-1] == '.':
                    self.position[i, j-1], self.position[i, j] = self.position[i, j], self.position[i, j-1]
        board = Board(self)
        return board 
    
    def right_gravity(self): # right gravity is kinda like up_gravity also
        for j in range(3): 
            for i in range(4): 
                if self.position[i, j+1] == '.':
                    self.position[i, j+1], self.position[i, j] = self.position[i, j], self.position[i, j+1]
        for j in range(3): 
            for i in range(4): 
                if self.position[i, j+1] == '.':
                    self.position[i, j+1], self.position[i, j] = self.position[i, j], self.position[i, j+1]
        board = Board(self)
        return board 
    
    # alright we have to compress the blocks if they are adjacent
    # We must make sure that we compress the block in the direction of the key press
    def merge_up(self):
        for i in range(1, 4):
            for j in range(4):
                if self.position[i-1, j] == self.position[i, j] and self.position[i, j] != self.blank:
                    self.position[i-1, j] = self.position[i-1, j] * 2
                    self.position[i,j] = self.blank
        board = Board(self)
        return board
    
    def merge_down(self):
        for i in range(2, -1, -1):
            for j in range(4):
                if self.position[i+1, j] == self.position[i, j] and self.position[i, j] != self.blank:
                    self.position[i+1, j] = self.position[i+1, j] * 2
                    self.position[i,j] = self.blank
        board = Board(self)
        return board
    
    def merge_left(self):
        for j in range(1,4):
            for i in range(4):
                if self.position[i, j-1] == self.position[i, j] and self.position[i, j] != self.blank:
                    self.position[i, j-1] = self.position[i, j-1] * 2
                    self.position[i,j] = self.blank
        board = Board(self)
        return board

    def merge_right(self):
        for j in range(2, -1, -1):
            for i in range(4):
                if self.position[i, j+1] == self.position[i, j] and self.position[i, j] != self.blank:
                    self.position[i, j+1] = self.position[i, j+1] * 2
                    self.position[i, j] = self.blank
        board = Board(self)
        return board
    
    def up_sequence(self):
         self = Board(self.up_gravity())
         self = Board(self.merge_up())
         self = Board(self.up_gravity())
         return self
    
    def down_sequence(self):
         self = Board(self.down_gravity())
         self = Board(self.merge_down())
         self = Board(self.down_gravity())
         return self
    
    def left_sequence(self):
        self = Board(self.left_gravity())
        self = Board(self.merge_left())
        self = Board(self.left_gravity())
        return self
    
    def right_sequence(self):
        self = Board(self.right_gravity())
        self = Board(self.merge_right())
        self = Board(self.right_gravity())
        return self
    
    def spawn_a_number(self):
        list_of_empty_spots = []
        for i in range(4):
            for j in range(4):
                if self.position[i, j] == self.blank:
                    list_of_empty_spots.append((i, j)) # append the tuple in the list
        number = random.sample(range(len(list_of_empty_spots)), 1)
        spot_chosen = list_of_empty_spots[number[0]]
        row = spot_chosen[0]
        column = spot_chosen[1]
        choices = [2, 4]
        probabilities = [0.9, 0.1]
        picked_number = random.choices(choices, probabilities)[0]
        self.position[row, column] = picked_number
        board = Board(self)
        return board
    
    def is_gameover(self):
        original_board = Board(self)
        b1 = Board(self.up_sequence())
        b2 = Board(self.down_sequence())
        b3 = Board(self.right_sequence())
        b4 = Board(self.left_sequence())

        if b1.__dict__ == original_board.__dict__ and b2.__dict__ == original_board.__dict__ and b3.__dict__ == original_board.__dict__ and b4.__dict__ == original_board.__dict__ : 
            return True
        return False

    def game_loop(self):
        print("###### Welcome to the Game of 2048 ######")
        print("Your task is to apply Monte Carlo Tree saerch to this game")
        print("To play along a little bit, the instruction set is as follows")
        print("w -> up, a -> left, s -> down, d -> right")
        print("Write exit to get out of the game")
        print(self)
        while True:
            key = input(">")
            board = Board(self)
            if self.is_gameover() == True : 
                self.game_over = True
                break
            self = Board(board)

            if key == 'w':
                board = Board(self)
                self = Board(self.up_sequence())
                if board.__dict__ == self.__dict__:
                    print("Illegal move")
                    self = Board(board)
                    continue
            elif key == 'a':
                board = Board(self)
                self = Board(self.left_sequence())
                if board.__dict__ == self.__dict__:
                    print("Illegal move")
                    self = Board(board)
                    continue
            elif key == 's':
                board = Board(self)
                self = Board(self.down_sequence())
                if board.__dict__ == self.__dict__:
                    print("Illegal move")
                    self = Board(board)
                    continue
            elif key == 'd':
                board = Board(self)
                self = Board(self.right_sequence())
                if board.__dict__ == self.__dict__:
                    print("Illegal move")
                    self = Board(board)
                    continue
            elif key == 'exit':
                break
                    
            else : 
                print("Not a move")
                continue

            self = Board(self.spawn_a_number())

            print(self)

        if self.game_over : print("Game Over")
        return 


if __name__ == '__main__':
    board = Board()
    board.game_loop()

        