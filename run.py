from findTheMusic import Compare
import sys
import os
import traceback

print("\n\n-------------------- SEARCH AND DESTROY...MUHAAHAA --------------------\n")

pathList = []

args = sys.argv
del args[0]

try:
    action = args[0].lower()
    del args[0]
    if action != 'kill' and action != 'find':
        print('Error: Enter `kill` to delete files or `find` to find them')
        sys.exit(0)
except Exception:
    print('Error: Enter `find` or `kill` followed by target directory path')
    traceback.print_exc()
    sys.exit(1)

try:
    if not os.path.isdir(args[0]):
        print('Error: Please enter a directory path as an argument to search...')
        sys.exit(0)
except IndexError:
    print('Error: Please enter a directory path as an argument to search...')
    sys.exit(0)

print('running finder in', action, 'mode...')

for dirPath in sys.argv:
    if os.path.isdir(dirPath):
        size = len(dirPath)
        if dirPath[size - 1] != "/":
            dirPath = dirPath + "/"
        pathList.append(dirPath)


comparison = Compare(pathList)
comparison.fillRootFiles()
comparison.fillTargetFiles()
comparison.compareFiles()
comparison.printEqualFiles()

if action == 'kill':
    comparison.removeRepeatFiles()
comparison.printRootSearch()
comparison.printTargetSearch()
