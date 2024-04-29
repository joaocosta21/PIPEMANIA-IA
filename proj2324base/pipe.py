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

PIECE_ROTATIONS = {
    "FC": {
            "UP": ["FB", "BB", "BE", "BD", "VB", "VE", "VD", "LV"],
            "DOWN": [],
            "LEFT": [],
            "RIGHT": []
        },
}

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
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
    
    def update_pos_in(self,state: PipeManiaState):
        board: Board = state.board
        for j in range(board.dim):
            for i in range(board.dim):
                piece = board.get_value(i,j)
                adjacent = [board.adjacent_vertical_values(i,j), board.adjacent_horizontal_values(i,j)] # 0 up 1 down 
                # if j == 0 and i == 0 and PIECE_ROTATIONS[piece]["UP"] and PIECE_ROTATIONS[piece]["LEFT"]:
                #         print("HI")
                # elif j == 0 and i == board.dim - 1 and PIECE_ROTATIONS[piece]["UP"] and PIECE_ROTATIONS[piece]["RIGHT"]:
                #         print("HI")
                # elif j == board.dim - 1 and i == 0 and PIECE_ROTATIONS[piece]["DOWN"] and PIECE_ROTATIONS[piece]["LEFT"]:
                #         print("HI")
                # elif j == board.dim - 1 and i == board.dim - 1 and PIECE_ROTATIONS[piece]["DOWN"] and PIECE_ROTATIONS[piece]["RIGHT"]:
                #         print("HI")
                # elif j == 0 and PIECE_ROTATIONS[piece]["UP"]:
                #         print("HI")
                # elif j == board.dim - 1 and PIECE_ROTATIONS[piece]["DOWN"]:
                #         print("HI")
                # elif i == 0 and PIECE_ROTATIONS[piece]["LEFT"]:
                #         print("HI")
                # elif i == board.dim - 1 and PIECE_ROTATIONS[piece]["RIGHT"]:
                #         print("HI")
        board.print()
        
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        action = (0,0,1)
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
        return statee.board

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    pipemania = PipeMania(board)
    initial_state = PipeManiaState(board)
    pipemania.update_pos_in(initial_state)
    pipemania.result(initial_state, (0,0,3))
    # Mostrar valor na posição (2, 2):
    print(initial_state.board.get_value(2, 2))