'''
    constants.py - This file defines cross module constants used in JHP.
'''

DNQ = 0    # team/player did not qualify for the playoffs
R1_ELIM = 1 # team/player was eliminated from the 1st round of the playoffs
R2_ELIM = 2 # team/player was eliminated from the 2nd round of the playoffs
R3_ELIM = 3 # team/player was eliminated from the conference finals
R4_ELIM = 4 # team/player was eliminated from the SC finals
ACTIVE  = 5   # team/player is potential or actively qualified for playoff participation
ACT_INJ = 6   # player is actively qualified to participate but is injured

'''
    Note, in the weeks leading up to the playoffs, all teams (16+) that have
    the potential of making the playoffs will be marked as ACTIVE.  Only the
    teams which statistically can't make the playoffs wil be marked as DNQ.

    During the playoffs, any team that is not eliminated is ACTIVE.
'''

