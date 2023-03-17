import copy
import math

inf = math.inf

class Moves:
    def __init__(self):
        self.row_new = None
        self.col_new = None
        self.row_prev = None
        self.col_prev = None

    def terminal_state(self, board_1, board_2):
        pits = 0
        pits_1 = 0
        for i in range(2):
            for j in range(8):
                if board_1[i][j] >= 2:
                    pits = pits + 1
                if board_2[i][j] >= 2:
                    pits_1 = pits_1 + 1

        return pits == 0 or pits_1 == 0

    def winner(self, board_1, board_2, player1, player2):
        # change variable names of num and num_1
        pits = 0  # number of seeds in board 1
        pits_1 = 0  # number of seeds in board_2
        for i in range(2):
            for j in range(8):
                if board_1[i][j] >= 2:
                    pits = pits + 1
                if board_2[i][j] >= 2:
                    pits_1 = pits_1 + 1

        if pits == 0 and pits_1 != 0:
            print(player2 + " is the winner!")

        elif pits_1 == 0 and pits != 0:
            print(player1 + " is the winner!")
        else:
            self.winner_non_terminal_state(board_1,board_2,player1,player2)

    def winner_non_terminal_state(self, board_1, board_2, player1, player2):
        seeds_num = 0  # number of seeds in board 1
        seeds_num_1 = 0  # number of seeds in board_2
        for i in range(2):
            for j in range(8):
                seeds_num = seeds_num + board_1[i][j]
                seeds_num_1 = seeds_num_1 + board_2[i][j]

        if seeds_num > seeds_num_1:
            print(player1 + " is the winner!")

        elif seeds_num < seeds_num_1:
            print(player2 + " is the winner!")

        else:
            print("Draw")

    def upper_row_sowing(self, row, col, player, num=0):
        # player to be changed to board
        if num == 0:  # number of seeds
            num = player[row][col]
            player[row][col] = 0
        num_1 = num  # keeps track of number of seeds distributed
        for j in range(num):
            col = col - 1
            if col >= 0:
                player[row][col] = player[row][col] + 1
                num_1 = num_1 - 1
            else:
                row = 1
                num = num_1
                self.lower_row_sowing(row, col, player, num)
                return
        self.row_new = row
        self.col_new = col

    def lower_row_sowing(self, row, col, player, num=0):
        if num == 0:
            num = player[row][col]
            player[row][col] = 0

        num_1 = num
        for j in range(num):
            col = col + 1
            if col <= 7:
                player[row][col] = player[row][col] + 1
                num_1 = num_1 - 1
            else:
                row = 0
                num = num_1
                self.upper_row_sowing(row, col, player, num)
                return
        self.row_new = row
        self.col_new = col

    def reverse_upper_row_sowing(self, row, col, player, num=0):
        if num == 0:
            num = player[row][col]
            player[row][col] = 0
        num_1 = num
        for j in range(num):
            col = col + 1
            if col <= 7:
                player[row][col] = player[row][col] + 1
                num_1 = num_1 - 1
            else:
                row = 1
                num = num_1
                self.reverse_lower_row_sowing(row, col, player, num)
                return
        self.row_new = row
        self.col_new = col

    def reverse_lower_row_sowing(self, row, col, player, num=0, status=True):
        if num == 0:
            num = player[row][col]
            player[row][col] = 0
        num_1 = num
        for j in range(num):
            col = col - 1
            if col >= 0:
                player[row][col] = player[row][col] + 1
                num_1 = num_1 - 1
            else:
                row = 0
                num = num_1
                self.reverse_upper_row_sowing(row, col, player, num)
                return
        self.row_new = row
        self.col_new = col

    def is_relay_sowing(self, player):
        return player[self.row_new][self.col_new] >= 2

    def sowing(self, row, col, player):
        self.row_prev = row
        self.col_prev = col
        if (0 <= row < len(player)) and (0 <= col < len(player[0])):
            if player[row][col] >= 2:
                if row == 0:
                    self.upper_row_sowing(row, col, player)
                if row == 1:
                    self.lower_row_sowing(row, col, player)

        else:
            print("Wrong Input!Try Again!")

    def reverse_sowing(self, row, col, player, status=True):
        self.row_prev = row
        self.col_prev = col
        if (0 <= row < len(player)) and (0 <= col < len(player[0])):
            if player[row][col] >= 2:
                if row == 0:
                    self.reverse_upper_row_sowing(row, col, player)
                if row == 1:
                    self.reverse_lower_row_sowing(row, col, player)

        else:
            print("Wrong Input!Try Again!")

    def is_capture(self, player_opp, player):
        row = self.row_new
        col = self.col_new
        if row == 0 and 0 <= col <= 7:
            col_1 = 7 - col
            return player[row][col] >= 2 and player_opp[row][col_1] >= 1 and player_opp[row + 1][col_1] >= 1

    def capture(self, player_opp, player):
        row_prev = self.row_prev
        col_prev = self.col_prev
        row_current = self.row_new
        col_current = self.col_new
        if row_current == 0:
            num = player[row_prev][col_prev]
            col = 7 - col_current
            player[row_prev][col_prev] = player_opp[row_current][col] + player_opp[row_current + 1][col]
            player_opp[row_current][col] = 0
            player_opp[row_current + 1][col] = 0
            self.sowing(row_prev, col_prev, player)
            player[row_prev][col_prev] = num

    def is_reverse_capture(self, player_opp, player):
        row = self.row_new
        col = self.col_new
        if (row == 0 and col == 0) or (row == 0 and col == 1) or (row == 1 and col == 0) or (row == 1 and col == 1):
            board = copy.deepcopy(player)
            self.reverse_sowing(row, col, board, False)
            return self.is_capture(player_opp, board)

    def reverse_capture(self, player_opp, player):
        row = self.row_new
        col = self.col_new
        self.reverse_sowing(row, col, player)
        self.capture(player_opp, player)

    def get_board_sum(self, board):
        sums = 0
        for i in range(2):
            for j in range(8):
                sums = sums + board[i][j]
        return sums


    def print_boards(self, board_1, board_2):
        board = [board_1[1][7],board_1[1][6],board_1[1][5],board_1[1][4],board_1[1][3],board_1[1][2],board_1[1][1],
              board_1[1][0]]
        board1 = [board_1[0][7], board_1[0][6], board_1[0][5], board_1[0][4], board_1[0][3], board_1[0][2],
                  board_1[0][1],board_1[0][0]]
        print(board)
        print(board1)
        print()
        print(board_2[0])
        print(board_2[1])
        print()


class Omweso(Moves):
    def __init__(self):
        super().__init__()
        self.board_1 = [[4, 4, 4, 4, 4, 4, 4, 4],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

        self.board_2 = [[4, 4, 4, 4, 4, 4, 4, 4],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

        self.curr_player_name = None
        self.n_levels = 0
        self.states = dict()

    def playing(self, row, col, curr_board, opp_board, print_status=True):
        while curr_board[row][col] >= 2:
            self.sowing(row, col, curr_board)
            row = self.row_new
            col = self.col_new
            if print_status:
                print("Board after sowing")
                self.print_boards(self.board_1, self.board_2)

            if self.is_capture(opp_board, curr_board):
                self.capture(opp_board, curr_board)
                if print_status:
                    print("Board after capture:")
                    self.print_boards(self.board_1, self.board_2)

            if self.is_reverse_capture(opp_board, curr_board):
                self.reverse_capture(opp_board, curr_board)
                if print_status:
                    print("Board after reverse capture:")
                    self.print_boards(self.board_1, self.board_2)

    def utility(self, board_1, board_2):
        # calculate the number of seeds on each board
        pits = 0
        pits_1 = 0
        for i in range(2):
            for j in range(8):
                if board_1[i][j] >= 2:
                    pits = pits + 1
                if board_2[i][j] >= 2:
                    pits_1 = pits_1 + 1
        # if one of the boards has less than 2 seeds, the game is over
        if pits == 0 and pits_1 > 0:
            return -1
        elif pits_1 == 0 and pits > 0:
            return 1
        else:
            return 0

    def utility_1(self, board_1, board_2):
        seeds_num = 0
        seeds_num_1 = 0
        for i in range(2):
            for j in range(8):
                seeds_num = seeds_num + board_1[i][j]
                seeds_num_1 = seeds_num_1 + board_2[i][j]

        if seeds_num > seeds_num_1:
            return 1

        elif seeds_num_1 > seeds_num:
            return -1

        else:
            return 0

    def minimax(self, board_1, board_2, depth, is_maximizing):
        # check if the game is over
        if self.terminal_state(board_1, board_2):
            return self.utility(board_1, board_2)
        # if depth limit is reached, return the utility value
        if depth == 0:
            return self.utility_1(board_1,board_2)

        # maximize the value for player 1
        if is_maximizing:
            best_value = -inf
            for i in range(2):
                for j in range(8):
                    if board_1[i][j] >= 2:
                        board_copy = copy.deepcopy(board_1)
                        board_copy_1 = copy.deepcopy(board_2)
                        if i == 0:
                            row = i
                            col = j
                            while board_copy[row][col] >= 2:
                                self.upper_row_sowing(row, col, board_copy)
                                row = self.row_new
                                col = self.col_new
                                if self.is_capture(board_copy_1, board_copy):
                                    self.capture(board_copy_1, board_copy)
                                if self.reverse_capture(board_copy_1, board_copy):
                                    self.reverse_capture(board_copy_1, board_copy)

                        else:
                            row = i
                            col = j
                            while board_copy[row][col] >= 2:
                                self.lower_row_sowing(row, col, board_copy)
                                row = self.row_new
                                col = self.col_new
                                if self.is_capture(board_copy_1, board_copy):
                                    self.capture(board_copy_1, board_copy)
                                if self.reverse_capture(board_copy_1, board_copy):
                                    self.reverse_capture(board_copy_1, board_copy)

                        value = self.minimax(board_copy, board_copy_1, depth - 1, False)
                        best_value = max(best_value, value)
            return best_value

        if not is_maximizing:
            best_value = inf
            for i in range(2):
                for j in range(8):
                    if board_2[i][j] >= 2:
                        board_copy = copy.deepcopy(board_2)
                        board_copy_1 = copy.deepcopy(board_1)
                        if i == 0:
                            row = i
                            col = j
                            while board_copy[row][col] >= 2:
                                self.upper_row_sowing(row, col, board_copy)
                                row = self.row_new
                                col = self.col_new
                                if self.is_capture(board_copy_1, board_copy):
                                    self.capture(board_copy_1, board_copy)
                                if self.reverse_capture(board_copy_1, board_copy):
                                    self.reverse_capture(board_copy_1, board_copy)

                        else:
                            row = i
                            col = j
                            while board_copy[row][col] >= 2:
                                self.lower_row_sowing(row, col, board_copy)
                                row = self.row_new
                                col = self.col_new
                                if self.is_capture(board_copy_1, board_copy):
                                    self.capture(board_copy_1, board_copy)
                                if self.reverse_capture(board_copy_1, board_copy):
                                    self.reverse_capture(board_copy_1, board_copy)

                        value = self.minimax(board_copy_1, board_copy, depth - 1, True)
                        best_value = min(best_value, value)

            return best_value

    def best_move(self, board_1, board_2):
        best_value = -math.inf
        move = None
        for i in range(2):
            for j in range(8):
                # check if the move is valid
                if board_1[i][j] >= 2:
                    board_copy = copy.deepcopy(board_1)
                    board_copy_1 = copy.deepcopy(board_2)
                    # make a move and get the new board state
                    if i == 0:
                        row = i
                        col = j
                        while board_copy[row][col] >= 2:
                            self.upper_row_sowing(row, col, board_copy)
                            row = self.row_new
                            col = self.col_new
                            if self.is_capture(board_copy_1, board_copy):
                                self.capture(board_copy_1, board_copy)
                            if self.reverse_capture(board_copy_1, board_copy):
                                self.reverse_capture(board_copy_1, board_copy)

                    else:
                        row = i
                        col = j
                        while board_copy[row][col] >= 2:
                            self.lower_row_sowing(row, col, board_copy)
                            row = self.row_new
                            col = self.col_new
                            if self.is_capture(board_copy_1, board_copy):
                                self.capture(board_copy_1, board_copy)
                            if self.reverse_capture(board_copy_1, board_copy):
                                self.reverse_capture(board_copy_1, board_copy)

                    value = self.minimax(board_copy, board_copy_1, 4, False)
                    # if the value is greater than the current best value, update the best value and the best move
                    if value > best_value:
                        best_value = value
                        move = (i, j)
        return move

    def PlayerVsComputer(self, player_name, player_turn):
        player1_name = None
        player2_name = None
        curr_board = self.board_1
        opp_board = self.board_2
        if player_turn == 1:
            player1_name = player_name
            player2_name = "Computer"
        elif player_turn == 2:
            player1_name = "Computer"
            player2_name = player_name
        depth_level = 0
        self.curr_player_name = player1_name
        self.print_boards(obj.board_1, obj.board_2)
        while not self.terminal_state(curr_board, opp_board):
            print(self.curr_player_name + " is playing")
            if self.curr_player_name == "Computer":
                row, col = self.best_move(curr_board,opp_board)
                print("Played:" + str(row) + " " + str(col))
                self.playing(row, col, curr_board, opp_board)

            else:
                row, col = input("Enter row<Enter> and column:").split(" ")
                print("Played:" + row + " "+ col)
                row = int(row)
                col = int(col)
                self.playing(row, col, curr_board, opp_board)
                depth_level = depth_level + 1

            # change turns
            if curr_board is self.board_1:
                curr_board = self.board_2
                opp_board = self.board_1
                self.curr_player_name = player2_name

            elif curr_board is self.board_2:
                curr_board = self.board_1
                opp_board = self.board_2
                self.curr_player_name = player1_name

        if self.terminal_state(curr_board,  opp_board):
            self.winner(curr_board, opp_board, player1_name, player2_name)


    def ManualPlay(self, player1_name, player2_name):
        curr_board = self.board_1
        opp_board = self.board_2
        self.curr_player_name = player1_name
        obj.print_boards(curr_board, opp_board)
        while not self.terminal_state(curr_board, opp_board):
            print(self.curr_player_name + " is playing")
            row, col = input("Enter row<Enter> and column:").split(" ")
            row = int(row)
            col = int(col)
            self.playing(row, col, curr_board, opp_board)

            # change turns
            if curr_board is self.board_1:
                curr_board = self.board_2
                opp_board = self.board_1
                self.curr_player_name = player2_name

            elif curr_board is self.board_2:
                curr_board = self.board_1
                opp_board = self.board_2
                self.curr_player_name = player1_name

        if self.terminal_state(self.board_1, self.board_2):
            self.winner(self.board_1, self.board_2, player1_name, player2_name)


obj = Omweso()

