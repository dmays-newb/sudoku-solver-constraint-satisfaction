import sys, copy

# Parse Sudoku data file
def parse_file(puzzle):
    for arg in sys.argv[1:]:
        try:
            puzzle_file = open(arg, 'r')
        except OSError:
            print('Cannot open file:', arg)
        else:
            file_to_array(puzzle_file, puzzle)
            puzzle_file.close()

# Convert character stream to array of ints
def file_to_array(file, puzzle):
    for line in file:
        for character in line:
            if character != '\n':
                puzzle.append(character)
    if len(puzzle) > 81:
        raise ValueError("Incorrect number of characters in puzzle")

# Provide solved puzzle via terminal output
def solution_output(puzzle):
    for i in range(0, 81):
        if i % 9 == 0:
            sys.stdout.write('\n')
        sys.stdout.write(puzzle[i])

# get blank spaces
def get_blanks(puzzle):
    temp_puzzle = copy.deepcopy(puzzle)
    blanks = []
    for i in range(0, 81):
        if temp_puzzle[i] == '0':
            blanks.append(i)
    return blanks

# Check column for matching number(s)
# Return list of numbers which do NOT appear in the column
def check_column(puzzle, index, array):
    temp_array = copy.deepcopy(array)
    unavailable_numbs = []
    current = index % 9
    while current < 81:
        if current != index:
            if puzzle[current] != 0:
                unavailable_numbs.append(puzzle[current])
        current = current + 9
    for numb in unavailable_numbs:
        if int(numb) in temp_array:
            temp_array.remove(int(numb))
    return temp_array

# Check horizontal
# Return list of numbers which do NOT appear in the row
def check_row(puzzle, index, array):
    temp_array = copy.deepcopy(array)
    unavailable_numbs = []
    b = index % 9
    current = index - b # get to front of row
    for i in range(0, 9): # process entire row
        j = current + i
        if j != index:
            if puzzle[j] != 0:
                unavailable_numbs.append(puzzle[j])
    for numb in unavailable_numbs:
        if int(numb) in temp_array:
            temp_array.remove(int(numb))
    return temp_array

# Check local 3x3 box
# Return list of numbers which are NOT in the same local 3x3 box
def check_box(puzzle, index, array):
    boxes = [
        [0, 1, 2, 9, 10, 11, 18, 19, 20],
        [3, 4, 5, 12, 13, 14, 21, 22, 23],
        [6, 7, 8, 15, 16, 17, 24, 25, 26],
        [27, 28, 29, 36, 37, 38, 45, 46, 47],
        [30, 31, 32, 39, 40, 41, 48, 49, 50],
        [33, 34, 35, 42, 43, 44, 51, 52, 53],
        [54, 55, 56, 63, 64, 65, 72, 73, 74],
        [57, 58, 59, 66, 67, 68, 75, 76, 77],
        [60, 61, 62, 69, 70, 71, 78, 79, 80]
             ]
    box_index = 0
    for box in boxes:
        if index in box:
            break
        else:
            box_index = box_index + 1

    temp_array = copy.deepcopy(array)
    unavailable_numbs = []
    for space in boxes[box_index]:
        if space != index:
            if puzzle[space] != 0:
                unavailable_numbs.append(puzzle[space])
    for numb in unavailable_numbs:
        if int(numb) in temp_array:
            temp_array.remove(int(numb))
    return temp_array

# Get possible numbers for a given blank space
def get_possible_numbers(puzzle, index):
    options = [i for i in range(1, 10)]
    # check column
    options = check_column(puzzle, index, options)
    # check row
    options = check_row(puzzle, index, options)
    # check box
    options = check_box(puzzle, index, options)
    return options

# Run program:
# Get original in an array for comparison
# Get list of blank tiles
# For each blank generate a list of available numbers
def main():
    original_puzzle = []
    possible_actions = [] # Arrays of possible states for a each blank space
    blanks = []
    parse_file(original_puzzle)
    blanks = get_blanks(original_puzzle)
    for space in blanks:
        possible_actions.append(get_possible_numbers(original_puzzle, space))

# Naive backtracking algorithm - Starting with first available blank and working in linear fashion

main()