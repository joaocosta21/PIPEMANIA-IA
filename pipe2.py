# 00000 Nome1
# 00000 Nome2

import time
import psutil

start_time = time.time()
start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # Initialize start_memory using psutil

import copy as copy
import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class Pipe:
    def __init__(self, top=False, right=False, bottom=False, left=False):
        self.connections = {'top': top, 'right': right, 'bottom': bottom, 'left': left}

    def __str__(self):
        return str(self.connections)


final = ["FC","FD","FB","FE"]
bif = ["BC","BD","BB","BE"]
volta = ["VC","VD","VB","VE"]
lig = ["LH","LV"]

PIECE = {
    "FC": Pipe(top = True),
    "FD": Pipe(right = True),
    "FB": Pipe(bottom = True),
    "FE": Pipe(left = True),
    "BC": Pipe(left = True, top = True, right = True),
    "BD": Pipe(right = True, bottom = True, top = True),
    "BB": Pipe(bottom = True, left = True, right = True),
    "BE": Pipe(left = True, top = True, bottom = True),
    "VC": Pipe(left = True, top = True),
    "VD": Pipe(right = True, top = True),
    "VB": Pipe(bottom = True, right = True),
    "VE": Pipe(left = True, bottom = True),
    "LH": Pipe(left = True, right = True),
    "LV": Pipe(top = True, bottom = True)
}


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.num_pieces = [ i for i in range(1, board.dim**2+1)]
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, grid) -> None:
        self.grid = grid
        self.dim = len(grid) # dimensão do tabuleiro
        
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.grid[row][col] 
    
    def set_value(self, row: int, col: int, value: str) -> None:
        """Atribui o valor na respetiva posição do tabuleiro."""
        self.grid[row][col] = value

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            return (None, self.grid[row+1][col])
        if row == self.dim - 1:
            return (self.grid[row-1][col], None)
        return (self.grid[row-1][col], self.grid[row+1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return (None, self.grid[row][col+1])
        if col == self.dim - 1:
            return (self.grid[row][col-1], None)
        return (self.grid[row][col-1], self.grid[row][col+1])
    
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
        # break_flag = False
        for i in range(self.dim):
            for j in range(self.dim):
                piece = self.get_value(i, j)

                # Get adjacent pieces
                up, down = self.adjacent_vertical_values(i, j)
                left, right = self.adjacent_horizontal_values(i, j)

                # Check if the piece is correct
                if Board.is_piece_correct(piece, up, down, left, right):
                    count += 1
            #     else:
            #         break_flag = True
            #         break  # Break out of inner loop
            # if break_flag:
            #     break
        return count

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
        up_condition = (up is None and not PIECE[piece].connections['top']) or \
                    (up is not None and PIECE[piece].connections['top'] == PIECE[up].connections['bottom'])
        down_condition = (down is None and not PIECE[piece].connections['bottom']) or \
                        (down is not None and PIECE[piece].connections['bottom'] == PIECE[down].connections['top'])
        left_condition = (left is None and not PIECE[piece].connections['left']) or \
                        (left is not None and PIECE[piece].connections['left'] == PIECE[left].connections['right'])
        right_condition = (right is None and not PIECE[piece].connections['right']) or \
                        (right is not None and PIECE[piece].connections['right'] == PIECE[right].connections['left'])

        # Check if all conditions are met
        if up_condition and down_condition and left_condition and right_condition:
            return True
        else:
            return False



class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)
        
    def correct_pos(self, board: Board, row: int, column: int, piece: str) -> bool:
        """Check if the piece at the given position is in a correct position."""
        # Get adjacent pieces for the current position
        up, down = board.adjacent_vertical_values(row, column)
        left, right = board.adjacent_horizontal_values(row, column)
        
        up_condition = True
        left_condition = True
        
        down_condition = (down is not None and PIECE[piece].connections['bottom'] == PIECE[down].connections['top']) or (down is None and not PIECE[piece].connections['bottom'])
        if row == 0:
            up_condition = not (PIECE[piece].connections['top'])
        right_condition = (right is not None and PIECE[piece].connections['right'] == PIECE[right].connections['left']) or (right is None and not PIECE[piece].connections['right'])
        if column == 0:
            left_condition = not (PIECE[piece].connections['left'])
            
        # Check if all conditions are met
        if up_condition and down_condition and left_condition and right_condition:
            return True
        else:
            return False
        
        # down_condition = True
        # right_condition = True
        
        # up_condition = (up is not None and PIECE[piece].connections['top'] == PIECE[up].connections['bottom']) or (up is None and not PIECE[piece].connections['top'])
        # if row == board.dim - 1:
        #     down_condition = not (PIECE[piece].connections['bottom'])
        # left_condition = (left is not None and PIECE[piece].connections['left'] == PIECE[left].connections['right']) or (left is None and not PIECE[piece].connections['left'])
        # if column == board.dim - 1:
        #     right_condition = not (PIECE[piece].connections['right'])
            
        # # Check if all conditions are met
        # if up_condition and down_condition and left_condition and right_condition:
        #     return True
        # else:
        #     return False
        

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if state.num_pieces == []:
            return []
        
        #TODO: ver pq e que 225 nao da
        
        piece = state.num_pieces.pop(-1)
        row = (piece - 1) // state.board.dim
        column = (piece - 1) % state.board.dim
        
        valid_actions = []
        piece_on_board = state.board.get_value(row, column)
        for rotation in range(4):
            rotation += 2 # demora muito depois
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
        
        statee = copy.deepcopy(state)
        
        pos_x, pos_y, rotation = action
        
        piece = statee.board.get_value(pos_x,pos_y)
        if piece in final:
            position = final.index(piece)
            statee.board.set_value(pos_x,pos_y,final[(position + rotation ) % 4])
        elif piece in bif:
            position = bif.index(piece)
            statee.board.set_value(pos_x,pos_y,bif[(position + rotation) % 4])
        elif piece in volta:
            position = volta.index(piece)
            statee.board.set_value(pos_x,pos_y,volta[(position + rotation) % 4])
        elif piece in lig:
            position = lig.index(piece)
            statee.board.set_value(pos_x,pos_y,lig[(position + rotation) % 2])
        return statee
    
    def search(self, state: PipeManiaState):
        board = state.board
        dim = board.dim
        visited_positions = set()

        # Perform depth-first traversal starting from the first piece
        frontier = [(0, 0)]  # Start from the top-left corner
        while frontier:
            row, col = frontier.pop()
            piece = board.get_value(row, col)
            if (row, col) in visited_positions:
                continue  # Skip if the position has been visited already
            visited_positions.add((row, col))
            
            # Add adjacent positions to the frontier based on connections
            connections = PIECE[piece].connections
            if connections['top'] and row > 0:
                frontier.append((row - 1, col))
            if connections['right'] and col < dim - 1:
                frontier.append((row, col + 1))
            if connections['bottom'] and row < dim - 1:
                frontier.append((row + 1, col))
            if connections['left'] and col > 0:
                frontier.append((row, col - 1))

        # Check if all positions on the board are visited
        return len(visited_positions) == dim**2

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if state.num_pieces != []:
            return False
        # if state.board.correct_pos() == state.board.dim**2:
        #     return self.search(state)
        return state.board.correct_pos() == state.board.dim**2
            

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return node.state.board.correct_pos()

    def primeira_procura(self):
        #TODO: pop se mexer
        dim = self.initial.board.dim
        for i in range(dim):
            for j in range(dim):
                piece = self.initial.board.get_value(i, j)
                # Set initial pieces based on their positions
                if i == 0:
                    if j == 0:
                        if piece[0] == "V":
                            self.initial.board.set_value(i, j, "VB")
                    elif j == dim - 1:
                        if piece[0] == "V":
                            self.initial.board.set_value(i, j, "VE")
                    else:
                        if piece[0] == "B":
                            self.initial.board.set_value(i, j, "BB")
                        elif piece[0] == "L":
                            self.initial.board.set_value(i, j, "LH")
                elif i == dim - 1:
                    if j == 0:
                        if piece[0] == "V":
                            self.initial.board.set_value(i, j, "VD")
                    elif j == dim - 1:
                        if piece[0] == "V":
                            self.initial.board.set_value(i, j, "VC")
                    else:
                        if piece[0] == "B":
                            self.initial.board.set_value(i, j, "BC")
                        elif piece[0] == "L":
                            self.initial.board.set_value(i, j, "LH")
                else:
                    if j == 0:
                        if piece[0] == "B":
                            self.initial.board.set_value(i, j, "BD")
                        elif piece[0] == "L":
                            self.initial.board.set_value(i, j, "LV")
                    elif j == dim - 1:
                        if piece[0] == "B":
                            self.initial.board.set_value(i, j, "BE")
                        elif piece[0] == "L":
                            self.initial.board.set_value(i, j, "LV")
        return self

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    initial_board = Board.parse_instance()
    
    # Create a PipeMania instance with the initial state and goal board
    pipemania = PipeMania(initial_board)
    
    pipemania = pipemania.primeira_procura() #nao poupa quase tempo nenhum
    
    solution_node = depth_first_tree_search(pipemania)
    
    solution = solution_node.state.board.grid
    
    for row in solution:
        print('\t'.join(row))

    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # Retrieve end_memory using psutil
    # print(f"Execution time: {end_time - start_time} seconds")
    # print(f"Memory usage: {end_memory - start_memory} MB")