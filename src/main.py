import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.nhl_teams import *
from src.players import *
from src.pool import *

def main():
    print("main()")

if __name__ == "__main__":
    main()