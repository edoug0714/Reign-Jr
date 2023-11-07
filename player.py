import pandas as pd

class Player():
    def __init__(self, name, team, number):
         self.name = name
         self.number = number
         self.team = team
         self.time = 0
         self.shots = 0
         self.blocked_shots = 0
         self.shots_on_target = 0
         self.goals = 0
         self.assists = 0
         self.points = 0
         self.plus_minus = 0
         self.shots_plus_minus = 0


class Game():
    def __init__(self):
        self.reign_started = False
        self.opp_started = False
        self.reign_last_time = 0
        self.opp_last_time = 0
        self.reign = []
        self.opp = []
        self.reign_curr = []
        self.opp_curr = []
        self.reign_on_ice = []
        self.opp_on_ice = []

    def player(self, name, team, number):
        if team == 'r':
            self.reign.append(Player(name, team, number))
        else:
            self.opp.append(Player(name, team, number))
    
    #P1 is being subbed on, P2 is being subbed off
    def sub(self, team, num1, num2, period, minutes, seconds):
        time = (period - 1) * 20 + (minutes * 60) + (seconds)
        p1 = self.find_index(team, num1)
        p2 = self.find_index(team, num2)

        if p1 == -1 or p2 == -1:
            print('SUB OPERATION FAILED - At least one player number DNE.')
            return

        #Reign substitution
        if team == 'r':
            if p1 in self.reign_curr:
                print('SUB OPERATION FAILED - Attempting to sub on player currently playing.')
                return
            if p2 not in self.reign_curr:
                print('SUB OPERATION FAILED - Attempting to sub off player not currently playing.')
                return
            if self.reign_started == False:
                print('SUB OPERATION FAILED - Reign starting 5 never declared.')
                return
            if p2 == self.reign_curr[0]:
                x = input('You are attempting to sub out the goalie. Type \'y\' to continue, type another character to go back:')
                if x != 'y':
                    return

            if self.reign_last_time != time:
                for i in range(self.reign_last_time, time):
                    self.reign_on_ice.append(list(self.reign_curr))

            self.reign_curr.remove(p2)
            self.reign_curr.append(p1)
            self.reign_last_time = time

        #Opponent substitution
        else:
            if p1 in self.opp_curr:
                print('SUB OPERATION FAILED - Attempting to sub two players on different teams.')
                return
            if p2 not in self.reign_curr:
                print('SUB OPERATION FAILED - Attempting to sub off player not currently playing.')
                return
            if self.opp_started == False:
                print('SUB OPERATION FAILED - Opponent starting 5 never declared.')
                return
            if p2 == self.opp_curr[0]:
                x = input('You are attempting to sub out the goalie. Type \'y\' to continue, type another character to go back:')
                if x != 'y':
                    return

            if self.opp_last_time != time:
                for i in range(self.opp_last_time, time):
                    self.opp_on_ice.append(list(self.opp_curr))

            self.opp_curr.remove(p2)
            self.opp_curr.append(p1)
            self.opp_last_time = time


    #The 5 players in the starting lineup
    def start(self, team, goalie, num1, num2, num3, num4, num5):
        if team == 'reign':
            if self.reign_started == True:
                print('START OPERATION FAILED - Starting 5 already set')
                return

            self.reign_curr = [self.find_index('r', goalie), self.find_index('r', num1), self.find_index('r', num2), self.find_index('r', num3), self.find_index('r', num4), self.find_index('r', num5)]
            if -1 in self.reign_curr:
                print('START OPERATION FAILED - At least one player number DNE.')
                self.reign_curr = []
                return

            self.reign_started = True

        else:
            if self.opp_started == True:
                print('START OPERATION FAILED - Starting 5 already set')
                return

            self.opp_curr = [self.find_index('o', goalie), self.find_index('o', num1), self.find_index('o', num2), self.find_index('o', num3), self.find_index('o', num4), self.find_index('o', num5)]
            if -1 in self.opp_curr:
                print('START OPERATION FAILED - At least one player number DNE.')
                self.opp_curr = []
                return

            self.opp_started = True

    def end(self):
        for i in range(self.reign_last_time, 3600):
            self.reign_on_ice.append(list(self.reign_curr))
        self.reign_last_time = 3600
        self.reign_started = False

        for i in range(self.opp_last_time, 3600):
            self.opp_on_ice.append(list(self.opp_curr))
        self.opp_last_time = 3600
        self.opp_started = False


    #Variables : {p1: player who took shot, team: p1's team, on_target: T/F, blocked: T/F, goal: T/F, assist1: number of assister (enter -1 if N/A), assist2: same as assist1}
    def shot(self, p1, team, period, minutes, seconds, on_target, goal, assist1, assist2):
        time = (period - 1) * 20 + (minutes * 60) + seconds
        p1.shots += 1

        if team == 'r':
            for i in range(1, 6):
                self.reign_curr[i].shots_plus_minus += 1
                self.opp_curr[i].shots_plus_minus -= 1

            if on_target == True:
                p1.shots_on_target += 1
                if goal == True:
                    p1.goals += 1
                    for i in range(1, 6):
                        self.reign_curr[i].plus_minus += 1
                        self.opp_curr[i].plus_minus -= 1

                    if assist1 != -1:
                        self.find_index('r', assist1).assists += 1
                        if assist2 != -1:
                            self.find_index('r', assist2).assists += 1

        else:
            for i in range(1, 6):
                self.opp_curr[i].shots_plus_minus += 1
                self.reign_curr[i].shots_plus_minus -= 1

            if on_target == True:
                p1.shots_on_target += 1
                if goal == True:
                    p1.goals += 1
                    for i in range(1, 6):
                        self.opp_curr[i].plus_minus += 1
                        self.reign_curr[i].plus_minus -= 1

                    if assist1 != -1:
                        self.find_index('o', assist1).assists += 1
                        if assist2 != -1:
                            self.find_index('o', assist2).assists += 1

    def calc_stats(self, team):
        if team == 'reign':
            for i in range(len(self.reign_on_ice)):
                for j in range(0, 6):
                    self.reign_on_ice[i][j].time += 1

            name_list = []
            number_list = []
            time_list = []
            for i in range(len(self.reign)):
                name_list.append(self.reign[i].name)
                number_list.append(self.reign[i].number)
                time_list.append(self.reign[i].time)

            data = {'Name': name_list, 'Number': number_list, 'Time on Ice': time_list}
            df = pd.DataFrame(data=data)
            print(df)



    def find_index(self, team, num):
        if team == 'r':
            for i in range(len(self.reign)):
                if self.reign[i].number == num:
                    return self.reign[i]
        else:
            for i in range(len(self.opp)):
                if self.opp[i].number == num:
                    return self.reign[i]

        return -1


def main():
    myGame = Game()

    myGame.player('GOALIE', 'r', 100)
    myGame.player('A', 'r', 1)
    myGame.player('B', 'r', 2)
    myGame.player('C', 'r', 3)
    myGame.player('D', 'r', 4)
    myGame.player('E', 'r', 5)
    myGame.player('F', 'r', 6)
    myGame.player('G', 'r', 7)

    myGame.player('GOALIE', 'o', 100)
    myGame.player('A', 'o', 1)
    myGame.player('B', 'o', 2)
    myGame.player('C', 'o', 3)
    myGame.player('D', 'o', 4)
    myGame.player('E', 'o', 5)
    myGame.player('F', 'o', 6)
    myGame.player('G', 'o', 7)

    myGame.start('reign', 100, 1, 2, 3, 4, 5)
    myGame.start('opp', 100, 1, 2, 3, 4, 5)

    myGame.sub('r', 6, 1, 1, 1, 30)
    myGame.sub('r', 7, 2, 1, 1, 30)
    myGame.sub('r', 1, 6, 1, 3, 0)
    myGame.sub('r', 2, 7, 1, 3, 0)
    myGame.sub('r', 6, 1, 1, 4, 30)
    myGame.sub('r', 7, 2, 1, 4, 30)

    myGame.calc_stats('reign')
    
    #PRINTS LAST REIGN SHIFT
    if len(myGame.reign_curr) != 0:
        for i in range(len(myGame.reign)):
            print(myGame.reign[i].time)

    #PRINTS LAST OPP SHIFT
    #if len(myGame.opp_curr) != 0:
        #for i in range(0, 6):
            #print(myGame.opp_curr[i].number)

    #PRINTS REIGN_ON_ICE VECTOR
    for i in range(len(myGame.reign_on_ice)):
        print(i, ': ', myGame.reign_on_ice[i][0].number, ' ', myGame.reign_on_ice[i][1].number, ' ', myGame.reign_on_ice[i][2].number, ' ', myGame.reign_on_ice[i][3].number, ' ', myGame.reign_on_ice[i][4].number, ' ', myGame.reign_on_ice[i][5].number)



    

    



main()

