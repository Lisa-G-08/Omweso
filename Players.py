from Omweso import *
choice = int(input("""Enter choice:
                               1- Player Vs Player
                               2- Player Vs Computer
                               Choice:"""))

if choice == 1:
    player1_name = input("Enter player 1 name:")
    player2_name =input("Enter player 2 name:")
    obj.ManualPlay(player1_name, player2_name)

if choice == 2:
    player_name = input("Enter player name:")
    player_turn = int(input("Enter turn:"))
    obj.PlayerVsComputer(player_name, player_turn)





