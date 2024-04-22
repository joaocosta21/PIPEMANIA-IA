from sys import stdin
#python3 base.py < inst.txt
class PipeManiaState:
    state_id = 0
    
    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
    
    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id
    

class Board:
    """ Representação interna de uma grelha de PipeMania. """
    
    def __init__(self, grid) -> None:
        self.grid = grid
        self.dim = len(grid) 

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        if row == 0:
            return ("W", self.grid[row+1][col])
        if row == self.dim - 1:
            return (self.grid[row-1][col], "W")
        return (self.grid[row-1][col], self.grid[row+1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        if col == 0:
            return ("W", self.grid[row][col+1])
        if col == self.dim - 1:
            return (self.grid[row][col-1], "W")
        return (self.grid[row][col-1], self.grid[row][col+1])

    def get_value(self, row:int, col:int) -> (str):
        """ Devolve o valor atual"""
        return self.grid[row][col] 

    def print(self):
        """ Imprime o estado atual da grelha interna """
        print(self.grid)

    # TODO: outros metodos da classe


@staticmethod
def parse_instance():
    """Lê a instância do problema do standard input (stdin)
    e retorna uma instância da classe Board.
    Por exemplo:
    $ python3 pipe_mania.py < input_T01
    > from sys import stdin
    > line = stdin.readline().split()
    """

    lines = stdin.read().strip().split('\n')

    # Initialize an empty list to store the values
    values = []

    # Iterate over each line and split it by '\t' to get the individual values
    for line in lines:
        line = line.split()
        values.append(line)

    return Board(values)
    
'''
class PipeMania(Problem):
    def __init__(self, initial_state: Board, goal_state: Board):
        """ O construtor especifica o estado inicial. """
        # TODO
        pass
    
    def actions(self, state: State):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass
    
    def result(self, state: State, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # TODO
        pass
    
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
'''


board = parse_instance()
board.print()
print(board.get_value(2,2))
print(board.adjacent_vertical_values(1,1))