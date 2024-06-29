import math
import random

class Treenode():
    def __init__(self, board, parent):
        self.board = board

        if self.board.is_win() or self.board.is_draw(): self.is_terminal = True
        else :self.is_terminal = False
        self.is_fully_expanded = False
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = {}

class MCTS():
    def search(self, initial_state):
        self.root = Treenode(initial_state, None)
        for i in range(1000):
            # Selecting a node
            node = self.select(self.root) 
            # Simulation Phase
            score = self.rollout(node.board)
            # Back propogate
            self.backpropogate(node, score)
        try : 
            return self.get_best_move(self.root, 0)
        except:
            pass
    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
            else:
                return self.expand(node)
        return node
    
    def expand(self, node):
        for state in node.board.generate_states():
            if str(state.position) not in node.children:
                new_node = Treenode(board=state, parent=node)
                node.children[str(state.position)] = new_node
                if len(node.board.generate_states()) == len(node.children):
                    node.is_fully_expanded = True
                #return new node
                return new_node
        print("Should not get here")

        

    def rollout(self, board):
        while not board.is_win():
            try: 
            # make the move on board
                board = random.choice(board.generate_states())
            except:
            # return draw score, because a draw must have happened if there were no choices left and a win did not occur
                return 0
            
        if board.player2 == 'x' : return 1
        elif board.player2 == 'o' : return -1
    def backpropogate(self, node, score):
        while node is not None:
            node.visits = node.visits + 1
            node.score = node.score + score
            node = node.parent    # Oh the values will be given back to all the parent nodes of this node, got it, awesome makes sense
    def get_best_move(self, node, exploration_constant):
        best_score = float('-inf')
        best_moves = [] # there are going to be a list of the nodes
        for child_node in node.children.values():
            if child_node.board.player2 == 'x': current_player= 1
            elif child_node.board.player2 == 'o': current_player = -1
            move_score = (current_player * child_node.score / (child_node.visits + 1)) + exploration_constant * math.sqrt(math.log(node.visits + 1) / (child_node.visits + 1))
            if move_score > best_score: 
                best_score = move_score
                best_moves = [child_node]
            elif move_score == best_score: best_moves.append(child_node)
        return random.choice(best_moves)