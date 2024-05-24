# 99985 João Costa
# 106022 João Fernandes

'''
import time
import psutil

start_time = time.time()
start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # Initialize start_memory using psutil
#'''

import numpy as np
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
        self.grid = np.array(grid)
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
        self.dim = board.dim
        self.domains = {}
        self.arcs = set() # pares únicos de peças vizinhas, para verificar constraints
        
        directions = [(1,0),(-1,0),(0,1),(0,-1)] #direções de vizinhos aceites (as diagonais não contam)

        # inicializar os domínios para cada posição do tabuleiro e criar arcos
        for row in range(board.dim):
            for col in range(board.dim):

                for d_row, d_col in directions:
                    if 0 <= d_row + row < self.dim and 0 <= d_col + col < self.dim:
                        if ((d_row+row,d_col+col),(row,col)) not in self.arcs:
                            self.arcs.add(((row,col),(d_row+row,d_col+col)))

                piece_value = board.get_value(row,col)

                if piece_value in final:
                    self.domains[row*self.dim + col] = final
                elif piece_value in bif:
                    self.domains[row*self.dim + col] = bif
                elif piece_value in volta:
                    self.domains[row*self.dim + col] = volta
                elif piece_value in lig:
                    self.domains[row*self.dim + col] = lig

        self.arcs = list(self.arcs)
        
        
    def correct_pos(self, board: Board, row: int, column: int, piece: str) -> bool:
        """Check if the piece at the given position is in a correct position."""
        # Get adjacent pieces for the current position
        
        # up, down = board.adjacent_vertical_values(row, column)
        # left, right = board.adjacent_horizontal_values(row, column)
        
        # up_condition = True
        # left_condition = True
        
        # down_condition = (down is not None and PIECE[piece].connections['bottom'] == PIECE[down].connections['top']) or (down is None and not PIECE[piece].connections['bottom'])
        # if row == 0:
        #     up_condition = not (PIECE[piece].connections['top'])
        # right_condition = (right is not None and PIECE[piece].connections['right'] == PIECE[right].connections['left']) or (right is None and not PIECE[piece].connections['right'])
        # if column == 0:
        #     left_condition = not (PIECE[piece].connections['left'])
            
        # # Check if all conditions are met
        # if up_condition and down_condition and left_condition and right_condition:
        #     return True
        # else:
        #     return False
        
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
        
        piece_on_board = state.board.get_value(row, column)

        valid_actions = []
        #valid_actions = self.domains[(row,column)].remove(piece_on_board) # USAR APENAS QUANDO PROCURA E INFERÊNCIA FOREM IMPLEMENTADOS

        #Continuar a usar se AC-3 não reduzir tempo o suficiente
        
        for rotation in range(4):
            # rotation += 1 # demora muito depois
            rotated_piece = self.rotate_piece(piece_on_board,row,column, rotation)

            '''
            if rotated_piece not in self.domains[(row,column)]:
                continue
            '''

            if self.correct_pos(state.board, row, column, rotated_piece):
                valid_actions.append((row, column, rotation))
                
        return valid_actions

    '''
    # Continuar a usar se AC-3 não tempo o suficiente
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
    '''

    def rotate_piece(self, piece: str, row, col, rotation: int) -> str:
        return self.domains[row*self.dim + col][(self.domains[row*self.dim + col].index(piece) + rotation) % len(self.domains[row*self.dim + col])]

    # TO-DO: MUDAR SE PROCURA E INFERÊNCIA FOREM IMPLEMENTADOS
    def result(self, state: PipeManiaState, action):
        new_state = copy.deepcopy(state)
        row, col, rotation = action
        piece = new_state.board.get_value(row, col)
        new_state.board.set_value(row, col, self.rotate_piece(piece,row,col,rotation))
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
        
        if state.board.correct_pos() != state.board.dim**2:
            return False
        
        state.board.print()
        print("hgcvgjh")
        if not PipeMania.is_connected(state.board):
            return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return 20 - node.state.board.correct_pos()
            
    def primeira_procura(self):
        dim = self.initial.board.dim
        for i in range(dim):
            for j in range(dim):
                piece = self.initial.board.get_value(i, j)
                if i == 0:
                    if j == 0 and piece[0] == "F":
                        self.domains[i*dim + j] = ["FD","FB"]
                    elif j == 0 and piece[0] == "V":
                        self.initial.board.set_value(i, j, "VB")
                        self.domains[i*dim + j] = ["VB"]
                        self.initial.num_pieces.remove(1)
                    elif j == dim - 1 and piece[0] == "F":
                        self.domains[i*dim + j] = ["FB","FE"]
                    elif j == dim - 1 and piece[0] == "V":
                        self.initial.board.set_value(i, j, "VE")
                        self.domains[i*dim + j] = ["VE"]
                        self.initial.num_pieces.remove(dim)
                    elif piece[0] == "F":
                        self.domains[i*dim + j] = ["FD","FB","FE"]
                    elif piece[0] == "V":
                        self.domains[i*dim + j] = ["VB","VE"]
                    elif piece[0] == "B":
                        self.initial.board.set_value(i, j, "BB")
                        self.domains[i*dim + j] = ["BB"]
                        self.initial.num_pieces.remove(j + 1)
                    elif piece[0] == "L":
                        self.initial.board.set_value(i, j, "LH")
                        self.domains[i*dim + j] = ["LH"]
                        self.initial.num_pieces.remove(j + 1)
                elif i == dim - 1:
                    if j == 0  and piece[0] == "F":
                        self.domains[i*dim + j] = ["FC","FD"]
                    elif j == 0 and piece[0] == "V":
                        self.initial.board.set_value(i, j, "VD")
                        self.domains[i*dim + j] = ["VD"]
                        self.initial.num_pieces.remove(dim * (dim - 1) + 1)
                    elif j == dim - 1 and piece[0] == "F":
                        self.domains[i*dim + j] = ["FC","FE"]
                    elif j == dim - 1 and piece[0] == "V":
                        self.initial.board.set_value(i, j, "VC")
                        self.domains[i*dim + j] = ["VC"]
                        self.initial.num_pieces.remove(dim * dim)
                    elif piece[0] == "F":
                        self.domains[i*dim + j] = ["FC","FD","FE"]
                    elif piece[0] == "V":
                        self.domains[i*dim + j] = ["VC","VD"]
                    elif piece[0] == "B":
                        self.initial.board.set_value(i, j, "BC")
                        self.domains[i*dim + j] = ["BC"]
                        self.initial.num_pieces.remove(dim * (dim - 1) + j + 1)
                    elif piece[0] == "L":
                        self.initial.board.set_value(i, j, "LH")
                        self.domains[i*dim + j] = ["LH"]
                        self.initial.num_pieces.remove(dim * (dim - 1) + j + 1)
                elif j == 0:
                    if piece[0] == "F":
                        self.domains[i*dim + j] = ["FC","FD","FB"]
                    elif piece[0] == "V":
                        self.domains[i*dim + j] = ["VD","VB"]
                    elif piece[0] == "B":
                        self.initial.board.set_value(i, j, "BD")
                        self.domains[i*dim + j] = ["BD"]
                        self.initial.num_pieces.remove(i * dim + 1)
                    elif piece[0] == "L":
                        self.initial.board.set_value(i, j, "LV")
                        self.domains[i*dim + j] = ["LV"]
                        self.initial.num_pieces.remove(i * dim + 1)
                elif j == dim - 1:
                    if piece[0] == "F":
                        self.domains[i*dim + j] = ["FC","FB","FE"]
                    elif piece[0] == "V":
                        self.domains[i*dim + j] = ["VC","VE"]
                    elif piece[0] == "B":
                        self.initial.board.set_value(i, j, "BE")
                        self.domains[i*dim + j] = ["BE"]
                        self.initial.num_pieces.remove(i * dim + dim)
                    elif piece[0] == "L":
                        self.initial.board.set_value(i, j, "LV")
                        self.domains[i*dim + j] = ["LV"]
                        self.initial.num_pieces.remove(i * dim + dim)

                if piece not in self.domains[i*dim + j]:
                    self.initial.board.set_value(i,j,self.domains[i*dim + j][0])
                    if len(self.domains[i*dim + j]) == 1 and i*dim+j+1 in self.initial.num_pieces:
                        self.initial.num_pieces.remove(i*dim + j + 1)

        if self.initial.board.get_value(dim-1,dim-1) not in self.domains[(dim-1)*dim + (dim-1)]:
            self.initial.board.set_value(dim-1,dim-1,self.domains[(dim-1)*dim + (dim-1)][0])
            if len(self.domains[(dim-1)*dim + (dim-1)]) == 1 and (dim-1)*dim + dim in self.initial.num_pieces:
                self.initial.num_pieces.remove((dim-1)*dim + dim)

        return self

    # Performs ac3 algorithm and deletes inconsistent piece values across the board
    def ac3(self):
        #breakpoint()
        # queue -> a queue of arcs between each positions
        queue = self.arcs

        while queue:
            #breakpoint()
            constraint = queue.pop(0)
            if self.revise(constraint):

                # is never false because a solution exists
                if len(self.domains[constraint[0][0]*self.dim+constraint[0][1]]) == 0:
                    return False
                
                if(self.initial.board.get_value(constraint[0][0],constraint[0][1]) not in self.domains[constraint[0][0]*self.dim+constraint[0][1]]):
                    self.initial.board.set_value(constraint[0][0],constraint[0][1],self.domains[constraint[0][0]*self.dim+constraint[0][1]][0])
                    if len(self.domains[constraint[0][0]*self.dim+constraint[0][1]]) == 1 and constraint[0][0]*self.dim+constraint[0][1] + 1 in self.initial.num_pieces:
                        self.initial.num_pieces.remove(constraint[0][0]*self.dim + constraint[0][1] + 1)

                directions = [(1,0),(-1,0),(0,1),(0,-1)] #direções de vizinhos aceites (as diagonais não contam)

                for d_row, d_col in directions:
                    if d_row + constraint[0][0] != constraint[1][0] or d_col + constraint[0][1] != constraint[1][1]:
                        if 0 <= d_row + constraint[0][0] < self.dim and 0 <= d_col + constraint[0][1] < self.dim:
                            queue.append(((d_row+constraint[0][0],d_col+constraint[0][1]), constraint[0]))
                
        return True
                
    # Revises a constraint between two pieces, deleting values from the pieces domain's which do not satisfy the constraint
    def revise(self, constraint: tuple):

        revised = False
        piece1_pos,piece2_pos = self.find_piece_pair_positions(constraint)

        #breakpoint()
        for possible_piece1 in self.domains[constraint[0][0]*self.dim+constraint[0][1]]:
            does_x_satisfy_any = False
            for possible_piece2 in self.domains[constraint[1][0]*self.dim+constraint[1][1]]:
                if(self.are_pieces_valid(possible_piece1,possible_piece2,piece1_pos,piece2_pos)):
                    does_x_satisfy_any = True
                    break
            if not does_x_satisfy_any:
                new_domain = []
                for value in self.domains[constraint[0][0]*self.dim+constraint[0][1]]:
                    if value != possible_piece1:
                        new_domain.append(value)
                self.domains[constraint[0][0]*self.dim+constraint[0][1]] = new_domain
                revised = True
        
        return revised

    # Find the relation between two neighbour pieces on a board, example: (top,bottom), (left,right), (bottom, top), (right,left)
    def find_piece_pair_positions(self, constraint: tuple):
        if constraint[0][0] == constraint[1][0] - 1 and constraint[0][1] == constraint[1][1]:
            return (0,2)
        elif constraint[0][0] == constraint[1][0] + 1 and constraint[0][1] == constraint[1][1]:
            return (2,0)
        elif constraint[0][0] == constraint[1][0] and constraint[0][1] == constraint[1][1] - 1:
            return (3,1)
        elif constraint[0][0] == constraint[1][0] and constraint[0][1] == constraint[1][1] + 1:
            return (1,3)
        else:
            return (None,None)

    def are_pieces_valid(self,possible_piece1,possible_piece2,piece1_pos,piece2_pos):

        if(possible_piece1[0] == 'F' and possible_piece2[0] == 'F'): #Se forem ambas de fecho, apenas se não tiverem ligação à outra são válidas
            return (not PIECE[possible_piece1][piece2_pos]) and (not PIECE[possible_piece2][piece1_pos])
        else:
            if(PIECE[possible_piece1][piece2_pos]):
                return PIECE[possible_piece2][piece1_pos]
            else:
                return not PIECE[possible_piece2][piece1_pos]   



if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    initial_board = Board.parse_instance()
    
    # Create a PipeMania instance with the initial state and goal board
    pipemania = PipeMania(initial_board)
    
    #breakpoint()
    pipemania = pipemania.primeira_procura() #nao poupa quase tempo nenhum

    #breakpoint()

    pipemania.ac3()

    #breakpoint()
    solution_node = depth_first_tree_search(pipemania)
    #solution_node = recursive_best_first_search(pipemania, pipemania.h)
    #solution_node = best_first_graph_search(pipemania, pipemania.h)
    #solution_node = greedy_search(pipemania, pipemania.h)

    solution = solution_node.state.board.grid
    
    for row in solution:
        print('\t'.join(row))

    '''
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # Retrieve end_memory using psutil
    print(f"Execution time: {end_time - start_time} seconds")
    print(f"Memory usage: {end_memory - start_memory} MB")
    #'''