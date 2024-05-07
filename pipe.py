# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

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

# PIECE = {
#     "final": {
#         "FC": Pipe(top = True),
#         "FD": Pipe(right = True),
#         "FB": Pipe(bottom = True),
#         "FE": Pipe(left = True)
#     },
#     "bif": {
#         "BC": Pipe(left = True, top = True, right = True),
#         "BD": Pipe(right = True, bottom = True, top = True),
#         "BB": Pipe(bottom = True, left = True, right = True),
#         "BE": Pipe(left = True, top = True, bottom = True)
#     },
#     "volta": {
#         "VC": Pipe(left = True, top = True),
#         "VD": Pipe(right = True, top = True),
#         "VB": Pipe(bottom = True, right = True),
#         "VE": Pipe(left = True, bottom = True)
#     },
#     "lig": {
#         "LH": Pipe(left = True, right = True),
#         "LV": Pipe(top = True, bottom = True)
#     }
# }

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.num_pieces = [ i for i in range(1, board.dim**2+1)]
        print(self.num_pieces)
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
        for i in range(self.dim):
            for j in range(self.dim):
                piece = self.get_value(i, j)
                print(piece)
                if piece is None:  # Skip if the current position is empty
                    continue
                
                # Get adjacent pieces
                up, down = self.adjacent_vertical_values(i, j)
                left, right = self.adjacent_horizontal_values(i, j)
                
                 # Check if the piece connections match its adjacent pieces
                up_condition = (up is None and not PIECE[piece].connections['top']) or \
                            (up is not None and PIECE[piece].connections['top'] == PIECE[up].connections['bottom'])
                down_condition = (down is None and not PIECE[piece].connections['bottom']) or \
                                (down is not None and PIECE[piece].connections['bottom'] == PIECE[down].connections['top'])
                left_condition = (left is None and not PIECE[piece].connections['left']) or \
                                (left is not None and PIECE[piece].connections['left'] == PIECE[left].connections['right'])
                right_condition = (right is None and not PIECE[piece].connections['right']) or \
                                (right is not None and PIECE[piece].connections['right'] == PIECE[right].connections['left'])
                
                if up_condition and down_condition and left_condition and right_condition:
                    count += 1
                    print(count)
        return count


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)
        
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        piece = state.num_pieces.pop(0)
        row = (piece - 1) // state.board.dim
        column = (piece - 1) % state.board.dim
        
        action = [(row,column,0), (row,column,1), (row,column,2), (row,column,3)]
        return action

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
            statee.board.set_value(pos_x,pos_y,final[(position + rotation) % 4])
        elif piece in bif:
            position = bif.index(piece)
            statee.board.set_value(pos_x,pos_y,bif[(position + rotation) % 4])
        elif piece in volta:
            position = volta.index(piece)
            statee.board.set_value(pos_x,pos_y,volta[(position + rotation) % 4])
        elif piece in lig:
            position = lig.index(piece)
            statee.board.set_value(pos_x,pos_y,lig[(position + rotation) % 2])
        statee.board.print()
        return statee

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        return state.board.correct_pos() == state.board.dim**2

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


def parse_instance2(file_path: str):
    with open(file_path, 'r') as file:
        # Read the contents of the file and split it into lines
        lines = file.read().strip().split('\n')

    # Initialize an empty list to store the values
    values = []

    # Iterate over each line and split it by '\t' to get the individual values
    for line in lines:
        line = line.split()
        values.append(line)
    print(values)

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    initial_board = Board.parse_instance()
    
    
    # Create a PipeMania instance with the initial state and goal board
    pipemania = PipeMania(initial_board)
    
    correct = pipemania.goal_test(pipemania.initial)
    print(correct)
    
    action = pipemania.actions(pipemania.initial)  # Pass pipemania.initial instead of board
    
    new_board = pipemania.result(pipemania.initial, action)
    
    solution_node = depth_first_tree_search(pipemania)
    # Mostrar valor na posição (2, 2):
    print(pipemania.initial.board.get_value(2, 2))
    
#a criar o problem como e que dou o estado final sendo que eu nao sei
# como e que faco a arvore de pesquisa