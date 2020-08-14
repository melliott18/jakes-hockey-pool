__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
update_everything.py
Updates the skater stats table by pulling from the NHL stats api.
Updates the pool team stats by pulling data from the skater and goalie tables.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.skaters import *
from lib.pool import *

update_skaters_table()
update_all_pool_team_stats()
update_pool_points_table()