__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
initialization.py
File for setting up the hockey pool.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.nhl_teams import *
from lib.skaters import *
from lib.pool import *

db_create("jhpDB")
create_nhl_teams_table() #creates teams table with no rows
insert_nhl_teams()    #set status as DNQ

#  Call update_nhl_teams.py at this point to set the teams status with the latest info

create_skaters_table() # creates and initializes skaters with pts,etc  = 0, and sets player status as same as team table status
update_skaters_table() # updates skaters with latest api stats.
create_pool()
