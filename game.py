import player
import pandas as pd

class Game():
    #==================================================================================================================================================================
    def __init__(self):                                                                                                                                               
        self.reign_started = False                                                                                                                                                                                                                                                 
        self.reign_last_time = 0                                                                                                                                                                                                                               
        self.reign = []                                                                                                                                                                                                                                                             
        self.reign_curr = []                                                                                                                                                                                                                                   
        self.reign_on_ice = []                                                                                                                                                                                                                                           
    #==================================================================================================================================================================
    #Adds a new player to the 'reign' vector
    def player(self, name, number):
            self.reign.append(player.Player(name, number))
    #==================================================================================================================================================================
    #P1 is being subbed on, P2 is being subbed off
    def sub(self, num1, num2, period, minutes, seconds):
        time = (period - 1) * 1200 + minutes * 60 + seconds

        #Series of tests to verify the substitution is valid
        p1 = self.find_index(num1)
        p2 = self.find_index(num2)
        if p1 == -1 or p2 == -1:
            print('SUB OPERATION FAILED - At least one player number DNE.')
            return
        elif p1 in self.reign_curr:
            print('SUB OPERATION FAILED - Attempting to sub on player currently playing.')
            return
        elif p2 not in self.reign_curr:
            print('SUB OPERATION FAILED - Attempting to sub off player not currently playing.')
            return
        elif self.reign_started == False:
            print('SUB OPERATION FAILED - Reign starting 5 never declared.')
            return
        elif p2 == self.reign_curr[0]:
            x = input('You are attempting to sub out the goalie. Type \'y\' to continue, type another character to go back:')
            if x != 'y':
                return

        #Updates the reign_on_ice vector as long as the last sub was not at the same time
        if self.reign_last_time != time:
            for i in range(self.reign_last_time, time):
                self.reign_on_ice.append(list(self.reign_curr))

        #Switches the players in the 'reign_curr' vector
        self.reign_curr.remove(p2)
        self.reign_curr.append(p1)
        self.reign_last_time = time
    #==================================================================================================================================================================
    #The 5 players in the starting lineup
    def start(self, goalie, num1, num2, num3, num4, num5):
        #If a starting 5 has already been set, exit
        if self.reign_started == True:
            print('START OPERATION FAILED - Starting 5 already set')
            return

        self.reign_curr = [self.find_index(goalie), self.find_index(num1), self.find_index(num2), self.find_index(num3), self.find_index(num4), self.find_index(num5)]
        if -1 in self.reign_curr:
            print('START OPERATION FAILED - At least one player number DNE.')
            self.reign_curr = []
            return

        self.reign_started = True
    #==================================================================================================================================================================
    #Ends the game (called when all subs are complete) 
    def end(self):
        #Updates reign_on_ice vector
        for i in range(self.reign_last_time, 3600):
            self.reign_on_ice.append(list(self.reign_curr))

        #Preps for overtime if necessary
        self.reign_last_time = 3600
        self.reign_started = False
    #==================================================================================================================================================================
    def shot(self, num1, period, minutes, seconds, team = 'r', blocked = False, block = -1, on_target = False, goal = False, assist1 = -1, assist2 = -1):
        if team != 'r':
            time = (period - 1) * 1200 + minutes * 60 + seconds

            #Adjust reign players shots +/-
            for i in range(1, 6):
                self.reign_on_ice[time][i].shots_plus_minus -= 1

            if blocked:
                #Checks if blocker is on ice at 'time'
                p2 = self.find_index(block)
                if p2 not in self.reign_on_ice[time]:
                    print('SHOT OPERATION FAILED - Shot blocker not on ice at given time.')
                    return
                p2.blocked_shots += 1

            #Count goalie stats 
            if on_target:
                self.reign_on_ice[time][0].shots_on_target += 1
                if goal:
                    self.reign_on_ice[time][0].goals += 1

        else:
            time = (period - 1) * 1200 + minutes * 60 + seconds

            p1 = self.find_index(num1)
            #Checks if shooter is on ice at 'time'
            if p1 not in self.reign_on_ice[time]:
                print('SHOT OPERATION FAILED - Shot taker not on ice at given time.')
                return
            p1.shots += 1

            #Adjust reign players shots +/-
            for i in range(1, 6):
                self.reign_on_ice[time][i].shots_plus_minus += 1

            if on_target:
                p1.shots_on_target += 1
                if goal:
                    p1.goals += 1
                    #Adjusts reign players +/-
                    for i in range(1, 6):
                        self.reign_on_ice[time][i].plus_minus += 1

                    #Check to see assisting players exist and increment 'assist' stat
                    if self.find_index(assist1) != -1:
                        self.find_index(assist1).assists += 1
                        if self.find_index(assist2) != -1:
                            self.find_index(assist2).assists += 1
    #==================================================================================================================================================================
    def hit(self, num1, period, minutes, seconds):
        time = (period - 1) * 1200 + minutes * 60 + seconds

        p1 = self.find_index(num1)
        if p1 not in self.reign_on_ice[time]:
            print('HIT OPERATION FAILED - Player not on ice at given time.')
            return
        p1.hits += 1
    #==================================================================================================================================================================
    #Gets the total time on ice for all reign players
    def __get_toi(self):
        time_list = []

        #Iterates through every second of the game and adds up each player's game time in seconds
        for i in range(len(self.reign_on_ice)):
            for j in range(0, 6):
                self.reign_on_ice[i][j].time += 1
            
        #Converts each players' time on ice from seconds to a string in format minutes:seconds and adds to list
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
    #Prints a dataframe of all reign players' stats
    def calc_stats(self):
        #Initializing empty lists to be used later
        name_list = []
        number_list = []
        shots_list = []
        shots_on_list = []
        goals_list = []
        assists_list = []
        points_list = []
        blocks_list = []
        hits_list = []
        plus_minus_list = []
        shots_plus_minus_list = []
        time_list = self.__get_toi()

        #Iterates through all players in 'reign' list and adds up their stats
        for i in range(len(self.reign)):
            name_list.append(self.reign[i].name)
            number_list.append(self.reign[i].number)
            shots_list.append(self.reign[i].shots)
            shots_on_list.append(self.reign[i].shots_on_target)
            goals_list.append(self.reign[i].goals)
            assists_list.append(self.reign[i].assists)
            points_list.append(self.reign[i].goals + self.reign[i].assists)
            blocks_list.append(self.reign[i].blocked_shots)
            hits_list.append(self.reign[i].hits)
            plus_minus_list.append(self.reign[i].plus_minus)
            shots_plus_minus_list.append(self.reign[i].shots_plus_minus)

        #Creates the dataframe with player stats
        data = {'Name': name_list, 'Number': number_list, 'Time on Ice': time_list, 'Shots': shots_list, 'Shots on Target': shots_on_list, 
                'Goals': goals_list, 'Assists': assists_list, 'Points': points_list, 'Blocked Shots': blocks_list, 'Hits': hits_list, '+/-': plus_minus_list, 
                'Shots +/-': shots_plus_minus_list}
        df = pd.DataFrame(data=data)
        df.to_csv('game_data.csv', index=False)
        print(df)
    #==================================================================================================================================================================
    #Helper function used to convert player number to player object
    def find_index(self, num):
        for i in range(len(self.reign)):
            if self.reign[i].number == num:
                return self.reign[i]

        return -1
    #==================================================================================================================================================================
