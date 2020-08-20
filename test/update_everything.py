__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
update_everything.py
Updates the pool and all stats related to it.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.players import *
from lib.pool import *

#set_prev_rank_to_curr_rank()
#update_player_statuses()
#update_players_table()
#update_active_player_count()
#update_points_change()
#update_dud_count()
update_all_pool_team_stats()
update_pool_points_table()
update_pool_points_rankings()
update_pool_rankings_table()