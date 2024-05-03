# input_str = "FB\tVB\tVE\nBD\tBE\tLV\nFC\tFC\tFC\n"

# # Split the input string by '\n' to get each line
# lines = input_str.strip().split('\n')

# # Initialize an empty list to store the values
# values = []

# # Iterate over each line and split it by '\t' to get the individual values
# for line in lines:
#     values.extend(line.split('\t'))

# # Print the values
# print(values[0])

#double array
input_str = "FB\tVB\tVE\nBD\tBE\tLV\nFC\tFC\tFC\n"

# Split the input string by '\n' to get each line
lines = input_str.strip().split('\n')

# Initialize an empty list to store the values
double_array = []

# Iterate over each line and split it by '\t' to get the individual values
for line in lines:
    values = line.split('\t')
    double_array.append(values)

# Print the first line
print(double_array)


# def update_pos_in(self,state: PipeManiaState):
    #     board: Board = state.board
        # for j in range(board.dim):
        #     for i in range(board.dim):
        #         piece = board.get_value(i,j)
                
        #         vertical_tuple = board.adjacent_vertical_values(i, j)
        #         horizontal_tuple = board.adjacent_horizontal_values(i, j)
        #         if j == 0 and i == 0 and PIECE_ROTATIONS[piece]["UP"] and PIECE_ROTATIONS[piece]["LEFT"]:
        #             print("HI")
        #         elif j == 0 and i == board.dim - 1 and PIECE_ROTATIONS[piece]["UP"] and PIECE_ROTATIONS[piece]["RIGHT"]:
        #             print("HI")
        #         elif j == board.dim - 1 and i == 0 and PIECE_ROTATIONS[piece]["DOWN"] and PIECE_ROTATIONS[piece]["LEFT"]:
        #             print("HI")
        #         elif j == board.dim - 1 and i == board.dim - 1 and PIECE_ROTATIONS[piece]["DOWN"] and PIECE_ROTATIONS[piece]["RIGHT"]:
        #             print("HI")
        #         elif j == 0 and PIECE_ROTATIONS[piece]["UP"]:
        #             print("HI")
        #         elif j == board.dim - 1 and PIECE_ROTATIONS[piece]["DOWN"]:
        #             print("HI")
        #         elif i == 0 and PIECE_ROTATIONS[piece]["LEFT"]:
        #             print("HI")
        #         elif i == board.dim - 1 and PIECE_ROTATIONS[piece]["RIGHT"]:
        #             print("HI")
        #         elif vertical_tuple[0] not in PIECE_ROTATIONS[piece]["UP"]:
        #             print("HI")
        # board.print()