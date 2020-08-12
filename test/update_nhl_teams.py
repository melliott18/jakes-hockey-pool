__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
update_nhl_teams.py
Updates the playoff statuses of various NHL teams.
(0 = DNQ, 1 = Eliminated in the 1st Round, 2 = Eliminated in the 2nd Round,
3 = Eliminated in the 3rd Round, 4 = Eliminated in the 4th (Final) Round,
5 = Currently in the playoffs/Cup Winner)
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from include.nhl_teams import *

# Teams to be eliminated
# First parameter: team_id
# Second parameter: status_id
update_nhl_team_status(1, 0)
update_nhl_team_status(3, 0)
update_nhl_team_status(5, 0)
update_nhl_team_status(7, 0)
update_nhl_team_status(9, 0)
update_nhl_team_status(10, 0)
update_nhl_team_status(13, 0)
update_nhl_team_status(17, 0)
update_nhl_team_status(18, 0)
update_nhl_team_status(22, 0)
update_nhl_team_status(24, 0)
update_nhl_team_status(26, 0)
update_nhl_team_status(28, 0)
update_nhl_team_status(30, 0)
update_nhl_team_status(52, 0)
