class Player():
     def __init__(self, fname, number):
         self.fname = fname
         #self.lname = lname
         self.number = number
         self.time = 0
         self.entered = -1


class Game():
    def __init__(self):
        self.reign_goals = 0
        self.opp_goals = 0
        self.last_time = 0
        self.curr = []
        self.on_ice = []
    
    #P1 is being subbed on, P2 is being subbed off
    def sub(self, p1, p2, time):

        print('Time: ', time, ' Last Time: ', self.last_time)
        print('Before: ', self.on_ice)

        if self.last_time != time:
            for i in range(self.last_time, time):
                self.on_ice.append(list(self.curr))
        
        self.curr.remove(p2.number)
        self.curr.append(p1.number)
        self.curr.sort()
        self.last_time = time

        print('After: ', self.on_ice)

        
    

    def start(self, p1, p2, p3, p4, p5):
        p1.entered = 0
        p2.entered = 0
        p3.entered = 0
        p4.entered = 0
        p5.entered = 0

        self.curr = [p1.number, p2.number, p3.number, p4.number, p5.number]
        self.curr.sort()

def find_index(data, num):
        for i in range(len(data)):
            if data[i].number == num:
                return 1

        return -1



def main():
    myGame = Game()
    players = []
    
    players.append(Player('A', 1))
    players.append(Player('B', 2))
    players.append(Player('C', 3))
    players.append(Player('D', 4))
    players.append(Player('E', 5))
    players.append(Player('F', 6))
    players.append(Player('G', 7))

    myGame.start(players[0], players[1], players[2], players[3], players[4])

    myGame.sub(players[5], players[1], 5)
    myGame.sub(players[6], players[2], 5)
    myGame.sub(players[1], players[5], 55)

    #print(myGame.on_ice)
    print(len(myGame.on_ice))



main()

