#Player class used for tracking individual player stats
class Player():
    def __init__(self, name, number):
         self.name = name
         self.number = number
         self.goalie = False
         self.time = 0
         self.shots = 0
         self.blocked_shots = 0
         self.hits = 0
         self.shots_on_target = 0
         self.goals = 0
         self.assists = 0
         self.points = 0
         self.plus_minus = 0
         self.shots_plus_minus = 0

