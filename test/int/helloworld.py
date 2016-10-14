from strangerboard import StrangerBoard
import sys

board = StrangerBoard(port="/dev/cu.usbmodem1411", timeout=5)
board.begin()

print(board._connection, file=sys.stderr)

print(board._read(), file=sys.stderr)
print(board.write("hello world"))