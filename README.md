# CS 480 - Assignment 3: Constraint Satisfaction Problem
Dustin Mays

## Instructions

### Contents

The root folder of this assignment should contain two .py files: main and constants as well as a test-cases subdirectory. Several test puzzles used in the development and testing of this program are in this directory.

### Running the Program

- cd into the root folder of this assignment
- run the program via this command `python main.py <algorithm-character> <input-puzzle>`
	- replace the `<algorithm-character>` with either 'n' or 'c'
		- n: will provide solution determined via naive backtracking
		- c: will provide solution determined via constraint satisfaction
	- replace `<input-puzzle>` with the input sudoku puzzle of your choice
- program will output solved puzzle with completion time

### Example Run

- input: `python main.py c .\test-cases\test5-evil`
- output: 
Here is your solved puzzle:

294673518
683152974
571984632
362598147
749321856
815467329
456239781
137846295
928715463

CSP -- Completion Time (seconds):  0.09401273727416992

## Methods (Algorithm Description)

The naive backtracking algorithm derives a solution by recursively processing an incrementally completed puzzle. All blank spaces (spaces with '0') are processed in their sequential order from top-left to bottom-right, and all potential values for each variable are processed from lowest to highest. A path will be abandoned and the algorithm will backtrack to the last variable if the current blank has no available values. This will continue until there are no more blank spaces, and then the solution is printed to the console. The naive backtracking function is supported by several functions to check for blanks and possible values for a given variable.

The CSP algorithm also derives a solution by recursively processing a partially completed puzzle, but it incorporates several CSP strategies to improve performance. At the start of each recursion, the blanks are updated, and degree heuristics and possible values for each blank are determined. Forward checking is implemented at this point via abandoning a current path and backtracking if there exists a blank without a possible solution(s).

Afthe forward checking, the blanks are then sorted by the count of available values and then by their degree heuristic values. This is how minimum remaining value and degree heuristics are used to select the next variable to process. The variable with the least remaining potential values and that impacts the most other blanks will be the processed. The values for this variable are chosen via sorting according to what is the least constraining. The function outputs a solution once there are no blanks remaining.

There are several supporting functions for the CSP algorithm. A degree heuristic value for each blank based on how many other blanks "contact" the current blank by being in the same column, row, or local (3x3) box. Potential values for a given variable/blank are sorted by the function least_constraining_sort. This function calculates the sum of available actions of all blanks for each potential value choice for the current variable and sorts by those that offer the most "options" for future variables.

## Analysis

My CSP algorithm incorporates all of the strategies listed in class for selecting variables and values and provides a significant improvement over naive backtracking.

### Comparisons of three evil puzzles:

Compared to the naive backtracking algorith, my CSP algorithm completes a puzzle in much less time.

Each of these puzzles are within /test-cases

test4-evil
Naive: 0.35 seconds
CSP: 0.30 seconds

test5-evil
Naive: 2.61 seconds
CSP: 0.09 seconds

test6-evil
Naive: 19.49 seconds
CSP: 0.37 seconds

test4-evil is an outlier compared to other evil puzzles in that naive backtracking works surprisingly quickly. There is something about the structure of this particular puzzle that allows for quick processing. I expect that its solution tree has a solution relatively far to the left side so that the naive backtracking algorithm, which acts like a depth-first search, reaches a solution without having to laterally explore the solution tree to much extent. I think that, had I implemented the naive backtracking with a reverse sequential variable and value choice, then the performance on test4-evil would be much slower.