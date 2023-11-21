import game

def main():
    myGame = game.Game()

    myGame.player('GOALIE', 100)
    myGame.player('A', 1)
    myGame.player('B', 2)
    myGame.player('C', 3)
    myGame.player('D', 4)
    myGame.player('E', 5)
    myGame.player('F', 6)
    myGame.player('G', 7)

    myGame.start(100, 1, 2, 3, 4, 5)
    myGame.sub(6, 1, 2, 10, 0)
    myGame.sub(7, 2, 2, 10, 0)
    myGame.end()

    myGame.shot(1, 1, 10, 0)
    myGame.shot(3, 1, 15, 0, on_target = True, goal = True)
    myGame.shot(15, 1, 17, 0, team = 'o', blocked = True, block = 4)


    myGame.calc_stats()



main()
