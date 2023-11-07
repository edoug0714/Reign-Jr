import player
import pandas as pd

class Game():
    #==================================================================================================================================================================
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
    #==================================================================================================================================================================
    def player(self, name, team, number):
        if team == 'r':
            self.reign.append(player.Player(name, team, number))
        else:
            self.opp.append(player.Player(name, team, number))
    #==================================================================================================================================================================
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
            if p2 not in self.opp_curr:
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
    #==================================================================================================================================================================
    #The 5 players in the starting lineup
    def start(self, team, goalie, num1, num2, num3, num4, num5):
        if team == 'reign':
            if self.reign_started == True:
                print('START OPERATION FAILED - Starting 5 already set')
                return

            self.reign_curr = [self.find_index('r', goalie), self.find_index('r', num1), self.find_index('r', num2), self.find_index('r', num3),
                               self.find_index('r', num4), self.find_index('r', num5)]
            if -1 in self.reign_curr:
                print('START OPERATION FAILED - At least one player number DNE.')
                self.reign_curr = []
                return

            self.reign_started = True

        else:
            if self.opp_started == True:
                print('START OPERATION FAILED - Starting 5 already set')
                return

            self.opp_curr = [self.find_index('o', goalie), self.find_index('o', num1), self.find_index('o', num2), self.find_index('o', num3),
                             self.find_index('o', num4), self.find_index('o', num5)]
            if -1 in self.opp_curr:
                print('START OPERATION FAILED - At least one player number DNE.')
                self.opp_curr = []
                return

            self.opp_started = True
    #==================================================================================================================================================================
    def end(self):
        for i in range(self.reign_last_time, 3600):
            self.reign_on_ice.append(list(self.reign_curr))
        self.reign_last_time = 3600
        self.reign_started = False

        for i in range(self.opp_last_time, 3600):
            self.opp_on_ice.append(list(self.opp_curr))
        self.opp_last_time = 3600
        self.opp_started = False
    #==================================================================================================================================================================
    def shot(self, team, num1, period, minutes, seconds, on_target, goal, assist1, assist2):
        p1 = self.find_index(team, num1)

        if p1 == -1:
            print('SHOT OPERATION FAILED - Player DNE.')
            return

        time = (period - 1) * 20 + (minutes * 60) + seconds
        print(time)
        print(len(self.reign_on_ice[15]))
        p1.shots += 1

        if team == 'r':

            for i in range(1, 6):
                self.reign_on_ice[time][i].shots_plus_minus += 1
                self.opp_on_ice[time][i].shots_plus_minus -= 1

            if on_target == True:
                self.opp_on_ice[time][0].shots_on_target += 1 #Add a shot to opponent goalie
                p1.shots_on_target += 1 #Add a shot on target to player
                if goal == True:
                    self.opp_on_ice[time][0].goals += 1 #Add a goal to opponent goalie
                    p1.goals += 1 #Add a goal to player
                    for i in range(1, 6):
                        self.reign_on_ice[time][i].plus_minus += 1
                        self.opp_on_ice[time][i].plus_minus -= 1

                    if assist1 != -1:
                        self.find_index('r', assist1).assists += 1
                        if assist2 != -1:
                            self.find_index('r', assist2).assists += 1

        else:
            for i in range(1, 6):
                self.opp_on_ice[time][i].shots_plus_minus += 1
                self.reign_on_ice[time][i].shots_plus_minus -= 1

            if on_target == True:
                self.reign_on_ice[time][0].shots_on_target += 1
                p1.shots_on_target += 1
                if goal == True:
                    self.reign_on_ice[time][0].goals += 1
                    p1.goals += 1
                    for i in range(1, 6):
                        self.opp_on_ice[time][i].plus_minus += 1
                        self.reign_on_ice[time][i].plus_minus -= 1

                    if assist1 != -1:
                        self.find_index('o', assist1).assists += 1
                        if assist2 != -1:
                            self.find_index('o', assist2).assists += 1
    #==================================================================================================================================================================
    def __get_toi(self, team):
        time_list = []

        if team == 'r':
            for i in range(len(self.reign_on_ice)):
                for j in range(1, 6):
                    self.reign_on_ice[i][j].time += 1
            
            for i in range(len(self.reign)):
                minutes = str(int(self.reign[i].time / 60))
                if len(minutes) == 1:
                    minutes = '0' + minutes
                seconds = str(self.reign[i].time % 60)
                if len(seconds) == 1:
                    seconds = '0' + seconds
                time_list.append(minutes + ':' + seconds)

        else:
            for i in range(len(self.opp_on_ice)):
                for j in range(1, 6):
                    self.opp_on_ice[i][j].time += 1

            for i in range(len(self.reign)):
                minutes = str(int(self.reign[i].time / 60))
                if len(minutes) == 1:
                    minutes = '0' + minutes
                seconds = str(self.reign[i].time % 60)
                if len(seconds) == 1:
                    seconds = '0' + seconds
                time_list.append(minutes + ':' + seconds)

        return time_list
    #==================================================================================================================================================================
    def __get_shots(self, team):
        shots_list = []

        if team == 'r':
            for i in range(len(self.reign)):
                shots_list.append(self.reign[i].shots)

        else:
            for i in range(len(self.opp)):
                shots_list.append(self.opp[i].shots)

        return shots_list
    #==================================================================================================================================================================
    def calc_stats(self, team):
            name_list = []
            number_list = []
            teams_list = []
            shots_list = []
            shots_on_list = []
            goals_list = []
            assists_list = []
            points_list = []
            plus_minus_list = []
            shots_plus_minus_list = []
            time_list = self.__get_toi('r')
            for i in range(len(self.reign)):
                name_list.append(self.reign[i].name)
                number_list.append(self.reign[i].number)
                teams_list.append(self.reign[i].team)
                shots_list.append(self.reign[i].shots)
                shots_on_list.append(self.reign[i].shots_on_target)
                goals_list.append(self.reign[i].goals)
                assists_list.append(self.reign[i].assists)
                points_list.append(self.reign[i].goals + self.reign[i].assists)
                plus_minus_list.append(self.reign[i].plus_minus)
                shots_plus_minus_list.append(self.reign[i].shots_plus_minus)

            data = {'Name': name_list, 'Number': number_list, 'Team': teams_list, 'Time on Ice': time_list, 'Shots': shots_list, 'Shots on Target': shots_on_list, 
                    'Goals': goals_list, 'Assists': assists_list, 'Points': points_list, '+/-': plus_minus_list, 'Shots +/-': shots_plus_minus_list}
            df = pd.DataFrame(data=data)
            df.to_csv('game_data.csv', index=False)
            print(df)
    #==================================================================================================================================================================
    def find_index(self, team, num):
        if team == 'r':
            for i in range(len(self.reign)):
                if self.reign[i].number == num:
                    return self.reign[i]
        else:
            for i in range(len(self.opp)):
                if self.opp[i].number == num:
                    return self.opp[i]

        return -1
    #==================================================================================================================================================================
