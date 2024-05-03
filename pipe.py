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
final = ["FC","FD","FB","FE"]
bif = ["BC","BD","BB","BE"]
volta = ["VC","VD","VB","VE"]
lig = ["LH","LV"]

# PIECE_ROTATIONS = {
#     "FC": {
#             "UP": ["FB", "BB", "BE", "BD", "VB", "VE", "VD", "LV"],
#             "DOWN": [],
#             "LEFT": [],
#             "RIGHT": []
#         },
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

    # TODO: outros metodos da classe

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
        
        piece = statee.board.get_value(action[0],action[1])
        if piece in final:
            position = final.index(piece)
            statee.board.set_value(action[0],action[1],final[(position + action[2]) % 4])
        if piece in bif:
            position = bif.index(piece)
            statee.board.set_value(action[0],action[1],bif[(position + action[2]) % 4])
        if piece in volta:
            position = volta.index(piece)
            statee.board.set_value(action[0],action[1],volta[(position + action[2]) % 4])
        if piece in lig:
            position = lig.index(piece)
            statee.board.set_value(action[0],action[1],lig[(position + action[2]) % 2])
        statee.board.print()
        return statee

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        problem = Problem(self.initial, goal_board)
        if problem.goal_test(self, state):
            return True
        else:
            return False

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
    
    file_path = "testpipe 1-9/test-04.out"  # Replace this with the actual file path
    goal_board = parse_instance2(file_path)
        
    goal_board = goal_board
    
    
    initial_board = Board.parse_instance()
    
    # Create a PipeMania instance with the initial state and goal board
    pipemania = PipeMania(initial_board)
    
    action = pipemania.actions(pipemania.initial)  # Pass pipemania.initial instead of board
    
    new_board = pipemania.result(pipemania.initial, action)
    
    solution_node = depth_first_tree_search(pipemania)
    # Mostrar valor na posição (2, 2):
    print(pipemania.initial.board.get_value(2, 2))
    
#a criar o problem como e que dou o estado final sendo que eu nao sei
# como e que faco a arvore de pesquisa