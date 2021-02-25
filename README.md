# Path finding and search assignment

---

This assignment requires us to implement three searching algorithms:

- Breadth-first search.
- Iterative deepening search.
- A\* search with Manhattan distance as heuristic.

For the three algorithms, it is required to implement a repeat-state checking to avoid revisiting states.

## Use

To use this code, you can either use the following command:
`python path_finding_search.py <-f/-d/-g> <file/directory> <-BFS/-IDS/-A*>`

For the data arguments, these are the options:
|arg|description|
|-|-|
|-f|specify the path to a file that contains the data|
|-d|specify a directory where there are files that contain the data|
|-g|generate random data to conduct 4 tests with sizes: 5x5, 10x10, 15x15, 20x20|

For the algorithm arguments, these are the options:
|arg|description|
|-|-|
|-BFS|use bredth-first search to process data|
|-IDS|use iterative deepening serach to process data|
|-A\*|use A\* with Manhattan heuristic to process data|

##### Example

Single File:
`python path_finding_search.py -f data.txt -A*`

Directory:
`python path_finding_search.py -d testfiles -A*`

Random data:
`python path_finding_search.py -g -A*`

**Note:** Python 3 is requiered as well as numpy. If you need to install numpy use the following command:

`pip3 install numpy`
