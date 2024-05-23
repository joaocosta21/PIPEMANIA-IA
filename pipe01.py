import time
import psutil
import numpy as np
import copy
import sys

start_time = time.time()
start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # Initialize start_memory using psutil

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

# Each piece is represented as an array of booleans: [top, right, bottom, left]
PIECE = {
    "FC": [True, False, False, False],
    "FD": [False, True, False, False],
    "FB": [False, False, True, False],
    "FE": [False, False, False, True],
    "BC": [True, True, False, True],
    "BD": [True, True, True, False],
    "BB": [False, True, True, True],
    "BE": [True, False, True, True],
    "VC": [True, False, False, True],
    "VD": [True, True, False, False],
    "VB": [False, True, True, False],
    "VE": [False, False, True, True],
    "LH": [False, True, False, True],
    "LV": [True, False, True, False],
}

final = ["FC", "FD", "FB", "FE"]
bif = ["BC", "BD", "BB", "BE"]
volta = ["VC", "VD", "VB", "VE"]
lig = ["LH", "LV"]

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.num_pieces = [i for i in range(1, board.dim**2 + 1)]
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, grid) -> None:
        self.grid = np.array(grid)
        self.dim = len(grid)  # dimensão do tabuleiro
        
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.grid[row, col]
    
    def set_value(self, row: int, col: int, value: str) -> None:
        """Atribui o valor na respetiva posição do tabuleiro."""
        self.grid[row, col] = value

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            return (None, self.grid[row+1, col])
        if row == self.dim - 1:
            return (self.grid[row-1, col], None)
        return (self.grid[row-1, col], self.grid[row+1, col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return (None, self.grid[row, col+1])
        if col == self.dim - 1:
            return (self.grid[row, col-1], None)
        return (self.grid[row, col-1], self.grid[row, col+1])
    
    def print(self):
        """ Imprime o estado atual da grelha interna """
        print(self.grid)

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        lines = sys.stdin.read().strip().split('\n')

        # Initialize an empty list to store the values
        values = []

        # Iterate over each line and split it by '\t' to get the individual values
        for line in lines:
            line = line.split()
            values.append(line)

        return Board(values)

    def correct_pos(self):
        count = 0
        for i in range(self.dim):
            for j in range(self.dim):
                piece = self.get_value(i, j)

                # Get adjacent pieces
                up, down = self.adjacent_vertical_values(i, j)
                left, right = self.adjacent_horizontal_values(i, j)

                # Check if the piece is correct
                if Board.is_piece_correct(piece, up, down, left, right):
                    count += 1
                else:
                    return count
        return count

    @staticmethod
    def is_piece_correct(piece, up, down, left, right):
        """
        Check if a single piece is correctly connected with its adjacent pieces.

        Args:
            piece: The value of the current piece.
            up: The value of the piece above the current piece.
            down: The value of the piece below the current piece.
            left: The value of the piece to the left of the current piece.
            right: The value of the piece to the right of the current piece.

        Returns:
            True if the piece is correctly connected, False otherwise.
        """
        # Check connection conditions
        up_condition = (up is None and not PIECE[piece][0]) or \
                       (up is not None and PIECE[piece][0] == PIECE[up][2])
        down_condition = (down is None and not PIECE[piece][2]) or \
                         (down is not None and PIECE[piece][2] == PIECE[down][0])
        left_condition = (left is None and not PIECE[piece][3]) or \
                         (left is not None and PIECE[piece][3] == PIECE[left][1])
        right_condition = (right is None and not PIECE[piece][1]) or \
                          (right is not None and PIECE[piece][1] == PIECE[right][3])

        # Check if all conditions are met
        return up_condition and down_condition and left_condition and right_condition

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)
        
    def correct_pos(self, board: Board, row: int, column: int, piece: str) -> bool:
        """Check if the piece at the given position is in a correct position."""
        # Get adjacent pieces for the current position
        up, down = board.adjacent_vertical_values(row, column)
        left, right = board.adjacent_horizontal_values(row, column)
        
        down_condition = True
        right_condition = True
        
        up_condition = (up is not None and PIECE[piece][0] == PIECE[up][2]) or (up is None and not PIECE[piece][0])
        if row == board.dim - 1:
            down_condition = not (PIECE[piece][2])
        left_condition = (left is not None and PIECE[piece][3] == PIECE[left][1]) or (left is None and not PIECE[piece][3])
        if column == board.dim - 1:
            right_condition = not (PIECE[piece][1])
            
        # Check if all conditions are met
        return up_condition and down_condition and left_condition and right_condition

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if state.num_pieces == []:
            return []
        
        piece = state.num_pieces.pop(0)
        row = (piece - 1) // state.board.dim
        column = (piece - 1) % state.board.dim
        
        valid_actions = []
        piece_on_board = state.board.get_value(row, column)
        for rotation in range(4):
            rotated_piece = self.rotate_piece(piece_on_board, rotation)
            if self.correct_pos(state.board, row, column, rotated_piece):
                valid_actions.append((row, column, rotation))
                
        return valid_actions

    def rotate_piece(self, piece: str, rotation: int) -> str:
        """Rotate a piece by the specified number of clockwise rotations."""
        if piece in final:
            return final[(final.index(piece) + rotation) % 4]
        elif piece in bif:
            return bif[(bif.index(piece) + rotation) % 4]
        elif piece in volta:
            return volta[(volta.index(piece) + rotation) % 4]
        elif piece in lig:
            return lig[(lig.index(piece) + rotation) % 2]
        else:
            return piece

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        new_board = copy.copy(state.board.grid)  # Only copy the board
        board = Board(new_board)
        pos_x, pos_y, rotation = action
        
        piece = board.get_value(pos_x, pos_y)
        new_piece = self.rotate_piece(piece, rotation)
        board.set_value(pos_x, pos_y, new_piece)
        
        new_state = PipeManiaState(board)
        new_state.num_pieces = state.num_pieces.copy()  # Copy the list of remaining pieces
        return new_state
    
    def is_connected(board: Board) -> bool:
        dim = board.dim
        visited = set()
        queue = [(0, 0)]  # Start BFS from the top-left corner

        while queue:
            x, y = queue.pop(0)
            if (x, y) in visited:
                continue

            visited.add((x, y))
            piece = board.get_value(x, y)

            if PIECE[piece][0] and x > 0:
                queue.append((x-1, y))
            if PIECE[piece][2] and x < dim - 1:
                queue.append((x+1, y))
            if PIECE[piece][3] and y > 0:
                queue.append((x, y-1))
            if PIECE[piece][1] and y < dim - 1:
                queue.append((x, y+1))

        # Check if all cells are visited
        return len(visited) == dim ** 2

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if state.num_pieces:
            return False
        # Check if all pieces are correctly placed
        if state.board.correct_pos() != state.board.dim**2:
            return False
        print(state.board.grid)
        print("ghghjghjghjbbbhj")
        
        if not PipeMania.is_connected(state.board):
            return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return node.state.board.correct_pos()

    def primeira_procura(self):
        dim = self.initial.board.dim
        for i in range(dim):
            for j in range(dim):
                piece = self.initial.board.get_value(i, j)
                # Set initial pieces based on their positions
                if i == 0:
                    if j == 0:
                        if piece[0] == "V":
                            self.initial.board.set_value(i, j, "VB")
                            self.initial.num_pieces.remove(1)
                    elif j == dim - 1:
                        if piece[0] == "V":
                            self.initial.board.set_value(i, j, "VE")
                            self.initial.num_pieces.remove(dim)
                    else:
                        if piece[0] == "B":
                            self.initial.board.set_value(i, j, "BB")
                            self.initial.num_pieces.remove(j + 1)
                        elif piece[0] == "L":
                            self.initial.board.set_value(i, j, "LH")
                            self.initial.num_pieces.remove(j + 1)
                elif i == dim - 1:
                    if j == 0:
                        if piece[0] == "V":
                            self.initial.board.set_value(i, j, "VD")
                            self.initial.num_pieces.remove(dim * (dim - 1) + 1)
                    elif j == dim - 1:
                        if piece[0] == "V":
                            self.initial.board.set_value(i, j, "VC")
                            self.initial.num_pieces.remove(dim * dim)
                    else:
                        if piece[0] == "B":
                            self.initial.board.set_value(i, j, "BC")
                            self.initial.num_pieces.remove(dim * (dim - 1) + j + 1)
                        elif piece[0] == "L":
                            self.initial.board.set_value(i, j, "LH")
                            self.initial.num_pieces.remove(dim * (dim - 1) + j + 1)
                else:
                    if j == 0:
                        if piece[0] == "B":
                            self.initial.board.set_value(i, j, "BD")
                            self.initial.num_pieces.remove(i * dim + 1)
                        elif piece[0] == "L":
                            self.initial.board.set_value(i, j, "LV")
                            self.initial.num_pieces.remove(i * dim + 1)
                    elif j == dim - 1:
                        if piece[0] == "B":
                            self.initial.board.set_value(i, j, "BE")
                            self.initial.num_pieces.remove(i * dim + dim)
                        elif piece[0] == "L":
                            self.initial.board.set_value(i, j, "LV")
                            self.initial.num_pieces.remove(i * dim + dim)
        return self

if __name__ == "__main__":
    initial_board = Board.parse_instance()
    
    # Create a PipeMania instance with the initial state and goal board
    pipemania = PipeMania(initial_board)
    
    # pipemania = pipemania.primeira_procura() #nao poupa quase tempo nenhum
    
    solution_node = depth_first_tree_search(pipemania)
    
    solution = solution_node.state.board.grid
    
    for row in solution:
        print('\t'.join(row))

    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # Retrieve end_memory using psutil
    # print(f"Execution time: {end_time - start_time} seconds")
    # print(f"Memory usage: {end_memory - start_memory} MB")

