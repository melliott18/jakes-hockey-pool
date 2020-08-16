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

from lib.nhl_teams import *
from lib.constants import *

# Teams to be eliminated
# First parameter: team_id
# Second parameter: status_id

update_nhl_team_status(54, ACTIVE) # Las Vegas Knights
update_nhl_team_status(16, ACTIVE) # Chicago Blackhawks
update_nhl_team_status(21, ACTIVE) # Colorado Avalanche
update_nhl_team_status(53, ACTIVE) # Arizona Coyotes
update_nhl_team_status(25, ACTIVE) # Dallas Stars
update_nhl_team_status(20, ACTIVE) # Calgary Flames
update_nhl_team_status(19, ACTIVE) # St Louis Blues
update_nhl_team_status(23, ACTIVE) # Vancouver Canucks
update_nhl_team_status(4, ACTIVE)  # Philedelphia Flyers
update_nhl_team_status(8, ACTIVE)  # Montreal Canadiens
update_nhl_team_status(14, ACTIVE) # Tampa Bay Lightning
update_nhl_team_status(29, ACTIVE) # Columbus Blue Jackets
update_nhl_team_status(15, ACTIVE) # Washington Capitals
update_nhl_team_status(2, ACTIVE)  # New York Islanders
update_nhl_team_status(6, ACTIVE)  # Boston Bruins
update_nhl_team_status(12, ACTIVE) # Carolina Hurricanes