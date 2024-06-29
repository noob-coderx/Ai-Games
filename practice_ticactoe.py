from copy import deepcopy
from practice_mcts import MCTS, Treenode

class Board():
    def __init__(self, board=None):
        self.player1 = 'x'
        self.player2 = 'o'
        self.empty_square = '.'

        self.position = {}

        self.init_board()
        
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def init_board(self):
        for row in range(3):
            for col in range(3):
                # set every board square to '.'
                self.position[row,col] = self.empty_square


    def make_move(self, row, col):
        # make a new board instance
        new_board = Board(self)
        new_board.position[row, col] = self.player1
        new_board.player1, new_board.player2 = new_board.player2, new_board.player1
        return new_board
    
    def is_draw(self):
        # loop over board squares
        for row, col in self.position:
            # empty square is available
            if self.position[row, col] == self.empty_square:
                # this is not a draw
                return False
        
        # by default we return a draw
        return True
    
    # get whether the game is won 
    def is_win(self):
        ##################################
        # vertical sequence detection
        ##################################
        
        # loop over board columns
        for col in range(3):
            winning_sequence = []
            for row in range(3):
                if self.position[row, col] == self.player2:
                    winning_sequence.append((row, col))
                if len(winning_sequence) == 3:
                    return True
        
        ##################################
        # horizontal sequence detection
        ##################################
        
        # loop over board columns
        for row in range(3):
            # define winning sequence list
            winning_sequence = []
            
            # loop over board rows
            for col in range(3):
                # if found same next element in the row
                if self.position[row, col] == self.player2:
                    # update winning sequence
                    winning_sequence.append((row, col))
                    
                # if we have 3 elements in the row
                if len(winning_sequence) == 3:
                    # return the game is won state
                    return True
    
        ##################################
        # 1st diagonal sequence detection
        ##################################
        
        # define winning sequence list
        winning_sequence = []
        
        # loop over board rows
        for row in range(3):
            # init column
            col = row
        
            # if found same next element in the row
            if self.position[row, col] == self.player2:
                # update winning sequence
                winning_sequence.append((row, col))
                
            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                # return the game is won state
                return True
        
        ##################################
        # 2nd diagonal sequence detection
        ##################################
        
        # define winning sequence list
        winning_sequence = []
        
        # loop over board rows
        for row in range(3):
            # init column
            col = 3 - row - 1
        
            # if found same next element in the row
            if self.position[row, col] == self.player2:
                # update winning sequence
                winning_sequence.append((row, col))
                
            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                # return the game is won state
                return True
        
        # by default return non winning state
        return False
    
    def game_loop(self):
        print("Tic Tac Toe, to understand Monte Carlo Tree Search")
        print("\n\n")
        print("Enter moves like 1,1 where the format is x,y")
        print("\n\n")
        print("Type exit to quit the game")
        print("\n\n")
        print(self)
        mcts = MCTS()

        while True:
            user_input = input(" >")
            if user_input == 'exit': break
            if user_input == '': continue
            # print(user_input.split(','))
            try:
                list = user_input.split(',')
                row, col = int(list[-1]) -1, int(list[0])-1
                if self.position[row, col] != self.empty_square:
                    print("Illegal Move!")
                    continue
                # print(row, col)
                self = self.make_move(row,col)
                print(self)
                if self.is_win():
                    print("Player1", self.player1)
                    print("Player2", self.player2)
                    print(f"player with {self.player2} has won the game")
                    break

                if self.is_draw():
                    print("DRAW")
                    break



                best_board_from_ai = mcts.search(self)
                self = best_board_from_ai.board
                print(self)

                if self.is_win():
                    print("Player1", self.player1)
                    print("Player2", self.player2)
                    print(f"player with {self.player2} has won the game")
                    break

                if self.is_draw():
                    print("DRAW")
                    break


                # AI that player 
            except Exception as e:
                print("error", e)
                print('Illegal command')


    def generate_states(self):
        actions=[]
        for row in range(3):
            for col in range(3):
                if self.position[row, col] == self.empty_square:
                    actions.append(self.make_move(row, col))
        return actions

    

    def __str__(self):  # __str__ method is just for convenience, now it we can directly write print(board)
        board_string = ""
        for row in range(3):
            for col in range(3):
                board_string += self.position[row, col] + " "
            board_string += '\n'
        board_string = '\n------------\n' +  f"{self.player1} to move" + '\n------------\n' + board_string
        
        return board_string
    


        


# main driver
if __name__ == '__main__':
    board = Board()  
    board.game_loop()
    # root = Treenode(board, None)
    # ai = MCTS()
    # print(root.children)
    # ai_move = ai.get_best_move(root, 0)
    # # ai_move is of class type of Treenode
    # print(ai_move.board) # Nice this gives a perfect random choice, that was to be expected here, noice


    # root = Treenode(board, None)
    # root.children['child1'] = Treenode(board=board.make_move(1,1), parent=root) 
    # print(root.__dict__)

    # AI vs AI
    # while True:
    #     best_move = mcts.search(board)
    #     board = best_move.board
    #     print(board)
    #     input()
    
    # here we will have to implement the human vs Ai mode, maybe even have inputs to switch from one to another 

    
    

    
    
    