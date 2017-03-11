# coding=utf-8

import sys

def printTree(parent, tree, indent=''):
    print(parent)

    if parent not in tree:
        return

    for child in tree[parent][:-1]:
        sys.stdout.write(indent + '|-')
        printTree(child, tree, indent + '| ')

    child = tree[parent][-1]
    sys.stdout.write(indent + '`-')
    printTree(child, tree, indent + '  ')

tree = {
  0       : [1, 4],
  4       : [360],
  272     : [3460],
  368     : [4184],
  472     : [504, 576, 7016],
  568     : [584, 640],
  576     : [664, 672],
  640     : [1048],
  664     : [368, 372, 512, 788],
  788     : [2120, 2720, 2976, 2996, 3956, 3980]
}

printTree(0, tree)