import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from include.nhl_teams import *
from include.skaters import *
from include.pool import *

#db_create("jhpDB")
#create_nhl_teams_table()
#insert_nhl_teams()
#create_skaters_table()
update_skaters_table()
#create_pool()
