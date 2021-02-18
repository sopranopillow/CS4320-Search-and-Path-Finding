# Path finding and search assignment

This assignment requires us to implement three searching algorithms:

- Breadth-first search.
- Iterative deepening search.
- A\* search with Manhattan distance as heuristic.

For the three algorithms, it is required to implement a repeat-state checking to avoid revisiting states.

## Use

To use this code, you can either use the following command:
`./path_finding_search.py -p <path> <algorithm>`

For the algorithm parameter, these are the options:
|arg|description|
|-|-|
|-B|use bredth-first search to process data|
|-I|use iterative deepening serach to process data|
|-A|use A\* with Manhattan heuristic to process data|

##### Example

`./path_finding_search.py -p data.txt -A`
