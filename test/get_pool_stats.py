__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
get_pool_stats.py
Retrieves the pool team stats from the pool database
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.pool import *

#print_pool_stats("points", "DESC")
print_all_pool_team_stats()
