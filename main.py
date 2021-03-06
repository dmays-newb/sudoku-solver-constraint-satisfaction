import sys, copy, time
import constants
from operator import itemgetter

# Parse Sudoku data file
def parse_file(puzzle):
    for arg in sys.argv[2:]:
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
    print("Here is your solved puzzle:")
    for i in range(0, 81):
        if i % 9 == 0:
            sys.stdout.write('\n')
        sys.stdout.write(puzzle[i])

# get blank spaces
# return integer array of indexes of blanks (0) in puzzle
def get_blanks(puzzle):
    temp_puzzle = copy.deepcopy(puzzle)
    blanks = []
    for i in range(0, 81):
        if temp_puzzle[i] == '0':
            blanks.append(i)
    return blanks

# get which box index is in
# return integer of box index
def get_box(index):
    box_index = 0
    for box in constants.BOXES:
        if index in box:
            break
        else:
            box_index = box_index + 1
    return box_index

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
    box_index = get_box(index)
    temp_array = copy.deepcopy(array)
    unavailable_numbs = []
    for space in constants.BOXES[box_index]:
        if space != index:
            if puzzle[space] != 0:
                unavailable_numbs.append(puzzle[space])
    for numb in unavailable_numbs:
        if int(numb) in temp_array:
            temp_array.remove(int(numb))
    return temp_array

# returns count of all other blanks in same local box as index
def blanks_in_box(puzzle, index, box_index):
    # start with neg one to account for blank at index
    count = -1
    for space in constants.BOXES[box_index]:
        if puzzle[space] == '0':
            count = count + 1
    return count

# returns count of all other blanks in row minus those in same local box as index
def blanks_in_row(puzzle, index, box_index):
    count = 0
    b = index % 9
    ignore_box = constants.BOXES[box_index]
    current = index - b  # get to front of row
    for i in range(0, 9):  # process entire row
        j = current + i
        if j not in ignore_box:
            if puzzle[j] == '0':
                count = count + 1
    return count

# returns count of all other blanks in column minus those in same local box as index
def blanks_in_column(puzzle, index, box_index):
    count = 0
    ignore_box = constants.BOXES[box_index]
    current = index % 9
    while current < 81:
        if current not in ignore_box:
            if puzzle[current] == '0':
                count = count + 1
        current = current + 9
    return count

# Get possible numbers for a given blank space
# Returns list of integers
def get_possible_numbers(puzzle, index):
    options = [i for i in range(1, 10)]
    # check column
    options = check_column(puzzle, index, options)
    # check row
    options = check_row(puzzle, index, options)
    # check box
    options = check_box(puzzle, index, options)
    return options

# naive backtrack algorithm
# works through variable and value choices in sequential order
# prints solved puzzle when number of blanks == 0
def naive_backtrack(input_puzzle, naive_time):
    blanks = []
    possible_actions = []

    blanks = get_blanks(input_puzzle)
    if len(blanks) == 0:
        solution_output(input_puzzle)
        print("\n\nNaive Backtrack -- Completion Time (seconds): ", time.time() - naive_time)
        return

    puzzle = copy.deepcopy(input_puzzle)

    temp_possible = get_possible_numbers(puzzle, blanks[0])
    for temp in temp_possible:
        possible_actions.append(temp)

    # ! if possible_actions is empty
    if len(possible_actions) != 0:
        for action in possible_actions:
            puzzle[blanks[0]] = str(action)
            naive_backtrack(puzzle, naive_time)

# Get degree of connectivity/constraints with other blanks
# Return integer
def get_degree(input_puzzle, index):
    count = 0
    box_index = get_box(index)
    count = count + blanks_in_box(input_puzzle, index, box_index)
    count = count + blanks_in_row(input_puzzle, index, box_index)
    count = count + blanks_in_column(input_puzzle, index, box_index)
    return count

# Take unsorted potential values and sort by least constraining first
# return sorted list
def least_constraining_sort(input_puzzle, index, potential_values):
    if len(potential_values) < 2:
        return potential_values

    sorted_list = copy.deepcopy(potential_values)
    sum_list = []
    # for each potential value @ INDEX
    # get a sum of the possible actions of all blanks
    for value in potential_values:
        temp_puzzle = copy.deepcopy(input_puzzle)
        temp_puzzle[index] = value
        new_blanks = get_blanks(temp_puzzle)
        temp_sum = 0
        for blank in new_blanks:
            temp_possible = get_possible_numbers(temp_puzzle, blank)
            temp_sum = temp_sum + len(temp_possible)
        sum_list.append(temp_sum)

    sorting_list = list(zip(sorted_list, sum_list))
    sorting_list.sort(key=itemgetter(1), reverse=True)
    sorted_list, sum_list = zip(*sorting_list)

    return sorted_list

# csp algorithm which incorporates: MRV and Degree Heuristic for variable selections,
# Chooses least constraining values for each variable
# Forward checks for no possible values for upcoming variables
# prints solved puzzle when number of blanks == 0
def csp_algorithm(input_puzzle, start_time):
    possible_actions = []
    numb_actions = []
    degrees = []

    blanks = get_blanks(input_puzzle)
    if len(blanks) == 0:
        solution_output(input_puzzle)
        print("\n\nCSP -- Completion Time (seconds): ", time.time() - start_time)
        return

    for blank in blanks:
        temp_possible = get_possible_numbers(input_puzzle, blank)
        # Forward Checking
        if len(temp_possible) == 0:
            return
        possible_actions.append(temp_possible)
        numb_actions.append(len(temp_possible))
        temp_degree = get_degree(input_puzzle, blank)
        degrees.append(temp_degree)

    # Zip all blank attributes together into one list
    # Sort by reversed degrees and then number of possible actions
    # MRV and Degree Heuristic Incorporated in this Sorting
    blanks_plus_data = list(zip(blanks, numb_actions, possible_actions, degrees))
    blanks_plus_data.sort(key=itemgetter(3), reverse=True)
    blanks_plus_data.sort(key=itemgetter(1))

    puzzle = copy.deepcopy(input_puzzle)

    if blanks_plus_data[0][1] != 0:
        temp_actions = least_constraining_sort(puzzle, blanks_plus_data[0][0], blanks_plus_data[0][2])
        for action in temp_actions:
            puzzle[blanks_plus_data[0][0]] = str(action)
            csp_algorithm(puzzle, start_time)

# Run program:
# Build puzzle
def main():
    original_puzzle = []
    parse_file(original_puzzle)

    alg_choice = sys.argv[1]
    if alg_choice == 'n':
        naive_start = time.time()
        naive_backtrack(original_puzzle, naive_start)
    elif alg_choice == 'c':
        csp_start = time.time()
        csp_algorithm(original_puzzle, csp_start)
    else:
        print("Unrecognized algorithm choice. Try again with either 'n' or 'c' as your first argument.")


main()
