import game

def main():
    myGame = game.Game()

    myGame.player('GOALIE', 'r', 100)
    myGame.player('A', 'r', 1)
    myGame.player('B', 'r', 2)
    myGame.player('C', 'r', 3)
    myGame.player('D', 'r', 4)
    myGame.player('E', 'r', 5)
    myGame.player('F', 'r', 6)
    myGame.player('G', 'r', 7)

    myGame.player('_GOALIE', 'o', 101)
    myGame.player('_A', 'o', 1)
    myGame.player('_B', 'o', 2)
    myGame.player('_C', 'o', 3)
    myGame.player('_D', 'o', 4)
    myGame.player('_E', 'o', 5)
    myGame.player('_F', 'o', 6)
    myGame.player('_G', 'o', 7)

    myGame.start('reign', 100, 1, 2, 3, 4, 5)
    myGame.start('opp', 101, 1, 2, 3, 4, 5)

    myGame.sub('r', 6, 1, 1, 1, 30)
    myGame.sub('o', 6, 1, 1, 1, 30)
    myGame.sub('r', 1, 6, 1, 5, 0)
    myGame.sub('o', 1, 6, 1, 5, 0)

    myGame.shot('r', 1, 1, 0, 15, True, True, -1, -1)
    myGame.shot('o', 2, 1, 0, 15, True, False, -1, -1)
    myGame.shot('r', 3, 1, 3, 30, True, True, -1, -1)


    for i in range(1, 6):
        print(myGame.reign_on_ice[15][i].number)

    myGame.end()

    myGame.calc_stats('reign')
    
    #PRINTS LAST REIGN SHIFT
    #if len(myGame.reign_curr) != 0:
        #for i in range(len(myGame.reign)):
            #print(myGame.reign[i].time)

    #PRINTS LAST OPP SHIFT
    #if len(myGame.opp_curr) != 0:
        #for i in range(0, 6):
            #print(myGame.opp_curr[i].number)

    #PRINTS REIGN_ON_ICE VECTOR
    #for i in range(len(myGame.reign_on_ice)):
        #print(i, ': ', myGame.reign_on_ice[i][0].number, ' ', myGame.reign_on_ice[i][1].number, ' ', myGame.reign_on_ice[i][2].number, ' ', myGame.reign_on_ice[i][3].number, ' ', myGame.reign_on_ice[i][4].number, ' ', myGame.reign_on_ice[i][5].number)



    

    



main()
