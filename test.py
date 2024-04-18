input_str = "FB\tVB\tVE\nBD\tBE\tLV\nFC\tFC\tFC\n"

# Split the input string by '\n' to get each line
lines = input_str.strip().split('\n')

# Initialize an empty list to store the values
values = []

# Iterate over each line and split it by '\t' to get the individual values
for line in lines:
    values.extend(line.split('\t'))

# Print the values
print(values[0])
values[0] = values[0][0]+ "E"
print(values[0])