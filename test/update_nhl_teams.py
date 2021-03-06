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

from src.nhl_teams import *
from src.constants import *

# Teams to be eliminated
# First parameter: team_id
# Second parameter: status_id

update_nhl_team_status(1, DNQ)      # New Jersey Devils
update_nhl_team_status(2, R3_ELIM)   # New York Islanders
update_nhl_team_status(3, DNQ)      # New York Rangers
update_nhl_team_status(4, R2_ELIM)   # Philedelphia Flyers
update_nhl_team_status(5, DNQ)      # Pittsburgh Penguins
update_nhl_team_status(6, R2_ELIM)   # Boston Bruins
update_nhl_team_status(7, DNQ)      # Buffalo Sabres
update_nhl_team_status(8, R1_ELIM)   # Montreal Canadiens
update_nhl_team_status(9, DNQ)      # Ottawa Senators
update_nhl_team_status(10, DNQ)     # Toronto Maple Leafs
update_nhl_team_status(12, R1_ELIM) # Carolina Hurricanes
update_nhl_team_status(13, DNQ)     # Florida Panthers
update_nhl_team_status(14, ACTIVE)  # Tampa Bay Lightning
update_nhl_team_status(15, R1_ELIM)  # Washington Capitals
update_nhl_team_status(16, R1_ELIM) # Chicago Blackhawks
update_nhl_team_status(17, DNQ)     # Detroit Red Wings
update_nhl_team_status(18, DNQ)     # Nashville Predators
update_nhl_team_status(19, R1_ELIM)  # St Louis Blues
update_nhl_team_status(20, R1_ELIM)  # Calgary Flames
update_nhl_team_status(21, R2_ELIM)  # Colorado Avalanche
update_nhl_team_status(22, DNQ)     # Edmonton Oilers
update_nhl_team_status(23, R2_ELIM)  # Vancouver Canucks
update_nhl_team_status(24, DNQ)     # Anaheim Ducks
update_nhl_team_status(25, ACTIVE)  # Dallas Stars
update_nhl_team_status(26, DNQ)     # Los Angeles Kings
update_nhl_team_status(28, DNQ)     # San Jose Sharks
update_nhl_team_status(29, R1_ELIM) # Columbus Blue Jackets
update_nhl_team_status(30, DNQ)     # Minnesota Wild
update_nhl_team_status(52, DNQ)     # Winnipeg Jets
update_nhl_team_status(53, R1_ELIM) # Arizona Coyotes
update_nhl_team_status(54, R3_ELIM)  # Las Vegas Knights
