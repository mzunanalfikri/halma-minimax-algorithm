# import sys 
# sys.setrecursionlimit(1000) 
import random
import time
import math
import random


MAX_DEPTH = 2
class Halma:
    def __init__(self, size, time_limit):
        self.bSize = size
        self.time_limit = time_limit
        self.board_state = [[0 for i in range(size)] for j in range(size)]
        self.pos_A = []
        self.pos_B = []
        self.init_board()
        self.init_board_val()

    def init_board_val(self):
        self.board_val1 = [[0 for i in range(self.bSize)] for j in range(self.bSize)]
        self.board_val2 = [[0 for i in range(self.bSize)] for j in range(self.bSize)]

        for i in range(self.bSize):
            for j in range(self.bSize):
                if i+j < self.bSize // 2:
                    self.board_val2[i][j] = self.bSize - i - j - 10
                else:
                    self.board_val2[i][j] = i + j
                if i+j >= self.bSize * 3 // 2 - 1:
                    self.board_val1[i][j] = self.bSize - i - j - 10
                else:
                    self.board_val1[i][j] = self.bSize - i - j

    def init_board(self):
        for i in range(self.bSize):
            for j in range(self.bSize):
                if i < self.bSize/2 and j < self.bSize/2 - i :
                    self.board_state[i][j] = 1
                    self.pos_A.append((i,j))

                if i >= self.bSize/2 and j >= self.bSize*3/2 - 1 - i:
                    self.board_state[i][j] = 2
                    self.pos_B.append((i,j))

    def print_board(self):
        for i in range(self.bSize):
            for j in range(self.bSize):
                if j == self.bSize - 1 :
                    print(self.board_state[i][j])
                else :
                    print(self.board_state[i][j], end=" ")
    
    # turn = 0 (player 1), turn = 1 (player 2)
    # position dalam tuple (i,j)
    def calculate_distance(self, currPos, goalPos): 
        return ((goalPos[0] - currPos[0])**2 + (goalPos[1] - currPos[1])**2)**0.5

    # generate list of tuple valid action (0, (i,j)) atau (1, (i,j))
    # 0 berarti gabisa jalan lagi
    # 1 berarti masih bisa jalan lagi
    def valid_actions_step(self, state, position):
        listOfValidActions = []
        for i in range(position[0]-1, position[0]+2) :
            if i >= 0 and i < self.bSize:
                for j in range(position[1]-1, position[1]+2):
                    if j >= 0 and j < self.bSize:
                        if state[i][j] == 0 :
                            listOfValidActions.append( (i,j))

        return listOfValidActions

    def valid_actions_jump(self, state, position):
        listOfValidActions = []

        for i in range(position[0] - 1, position[0] + 2) :
            dif_i = i - position[0]

            if i >= 0 and i < self.bSize:
                for j in range(position[1]-1, position[1]+2):
                    if j >= 0 and j < self.bSize:
                        dif_j = j - position[1]
                        jump_i = i + dif_i
                        jump_j = j + dif_j
                        if jump_i >= 0 and jump_i < self.bSize and jump_j >= 0 and jump_j < self.bSize :
                            if state[jump_i][jump_j] == 0 and state[i][j] != 0:
                                listOfValidActions.append((jump_i, jump_j))

        return listOfValidActions

    def copy_board(self, board) :
        sizeboard = len(board)
        new_board = [[0 for i in range(sizeboard)] for j in range(sizeboard)]
        for i in range(sizeboard) :
            for j in range(sizeboard) :
                new_board[i][j] = board[i][j]
        
        return new_board

            
    
    def generate_valid_state(self, board, player):
        if player == 1 :
            listPos = self.pos_A
        elif player == 2 :
            listPos = self.pos_B
        else :
            print("Tidak valid")
            return
        
        listOfValidState = []
        for pos in listPos :
            listOfValidActions = self.valid_action(board, pos)

            
            for action in listOfValidActions :
                state = self.copy_board(board)
                
                state[pos[0]][pos[1]] = 0
                state[action[1][0]][action[1][1]] = player

                # (state board, posisi awal perpindahan, posisi akhir perpindahan, boolean apakah habis lompat atau ngga)
                listOfValidState.append((state, pos, action))
        
        return listOfValidState


    def check_win_state(self, turn) :
        if turn == 0 :
            for x,y in self.pos_A :
                if x + y < self.bSize*3/2 - 1:
                    return False
            return True
        else :
            for x,y in self.pos_B :
                if x + y > self.bSize/2 - 1 :
                    return False
                
            return True
    
    def objective_func(self, state, player, position):
        if player == 1:
            return self.board_val1[position[0]][position[1]]
        else:
            return self.board_val2[position[0]][position[1]]


    def eval_board(self, turn):
        map_obj = []
        if turn == 0:
            for p in self.pos_A:
                map_obj.append(self.objective_func(self.board_state, turn, p))
        else:
            for p in self.pos_B:
                map_obj.append(self.objective_func(self.board_state, turn, p))

        return map_obj

    # mengembalikan keputusan terbaik dari suatu state dan player tertentu 
    def minimax_decision(self, player):
        s = time.time()
        generated_state = self.possible_state(self.board_state, player)
        # for state in generated_state:
        #     print_board(state)
        #     print("*"*90)
        best_state_idx = []
        max_obj_value = float('-inf')
        for i, state in enumerate(generated_state):
            # print("obj value :", self.min_value(state,1, player))
            temp_obj_value = self.min_value(state, 1, player, float('-inf'), float('inf'))
            if  temp_obj_value > max_obj_value :
                max_obj_value = temp_obj_value
                best_state_idx = [i]
            elif temp_obj_value == max_obj_value:
                best_state_idx.append(i)
            if time.time() - s > self.time_limit :
                break
        # return max_obj_value
        random.shuffle(best_state_idx)
        self.board_state = generated_state[best_state_idx[0]]
        print(best_state_idx)
        return generated_state[best_state_idx[0]] # harusnya ini yang dipakai


    def min_value(self, state, depth, player, alpha, beta):
        if depth == MAX_DEPTH:
            return self.objective_func_board(state, player)
        elif self.check_win_state_board(state) == player:
            return 1000
        elif self.check_win_state_board(state) != 0:
            return -1000
        
        v = float('inf')
        possible_state_min = self.possible_state(state, player)
        for s in possible_state_min:
            v = min(v, self.max_value(s, depth + 1, player, alpha, beta))
            # pruning
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, state, depth, player, alpha, beta):
        if depth == MAX_DEPTH:
            return self.objective_func_board(state, player)
        elif self.check_win_state_board(state) == player:
            return 1000
        elif self.s(state) != 0:
            return -1000

        v = float('-inf')
        possible_state_max = self.possible_state(state, player)
        for s in possible_state_max:
            v = max(v, self.min_value(s, depth + 1, player, alpha, beta))
            # pruning
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    # mengembalikan list of state dari semua state yang mungkin dari suatu posisi
    def possible_state(self, state, player):
        #iterasi semua pion, pakai fungsi generate_all_move
        # TO DO 
        assert player == 2 or player == 1
        all_state = []
        for i in range(self.bSize):
            for j in range(self.bSize):
                if (state[i][j] == player):
                    all_state += self.generate_all_move(state, (i,j))
        return all_state

    # check win state dari suatu board
    def check_win_state_board(self, state):
        pion1 = []
        pion2 = []
        for i in range(self.bSize):
            for j in range(self.bSize):
                if state[i][j] == 1:
                    pion1.append((i,j))
                else:
                    pion2.append((i,j))
        win1 = True
        win2 = True
        for x,y in pion1 :
            if x + y < self.bSize*3/2 - 1:
                win1 = False
        for x,y in pion2 :
            if x + y > self.bSize/2 - 1 :
                win2 = False
        if win1:
            return 1
        elif win2:
            return 2
        else:
            return 0

    # return value objective function dari suatu board
    # player 
    def objective_func_board(self, state, player):
        res = 0
        for i in range(self.bSize):
            for j in range(self.bSize):
                if state[i][j] == player:
                    res -= self.objective_func(state, player, (i, j))
                elif state[i][j] != 0:
                    res += self.objective_func(state, state[i][j], (i, j))
        # print("res",res)
        return res

    # generate semua kemungkinan posisi dari yang mungkin dari suatu pion
    # return list of position 
    def generate_all_move(self, state, position):
        pos_move = [] #hasil
        queue = []
        expand = []
        #generate yang satu step
        pos_move += self.valid_actions_step(state, position)
        #inisiasi gerakan yang lompat
        init_jump_step = self.valid_actions_jump(state, position)
        pos_move += init_jump_step
        queue += init_jump_step
        while len(queue) != 0 :
            temp_move = queue.pop(0)
            # print('temp : ', temp_move, ' expand :', expand)
            if temp_move not in expand: #kalo belom pernah di expand, expand!
                expand.append(temp_move)
                #generate semua langkah loncat yang mungkin dari yang di expand
                temp_jump_move = self.valid_actions_jump(state, temp_move)
                # print('temp jump : ', temp_jump_move)
                for move in temp_jump_move:
                    if move not in pos_move: 
                        pos_move.append(move)
                    if move not in queue: # masukin ke queue buat generate lagi nanti
                        queue.append(move)
        res_state = []
        copy_state = self.copy_board(state)
        pion = copy_state[position[0]][position[1]]
        copy_state[position[0]][position[1]] = 0
        for p in pos_move:
            temp = self.copy_board(copy_state)
            temp[p[0]][p[1]] = pion
            res_state.append(temp)
        return res_state

    # TODO ambil n random successor state dari possible state
    # TODO ambil suksesor random
    # TODO itung min max, kalo max ambil >, kalo <= dibreak
    # TODO def local_search():
    def local_search(self, arrstate, player):
        # Ambil 25 persen dar total generated state
        NELM = math.floor(len(arrstate)/4)
        # index randomizer
        x=random.sample(range(len(arrstate)), NELM)

        arr_local = []
        for idx in x:
            arr_local.append(arrstate[idx])

        return arr_local
        
if __name__ == "__main__":
    # i = 1
    # while (not halma.check_win_state_board(halma.board_state)):
    #     print("="*8, "turn", i, "="*8)
    #     print()
    #     print_board(halma.minimax_decision(1))
    #     halma.minimax_decision(2)
    #     i+=1
    #     print()
    # e = time.time()v
    # s = time.time()
    # print("Waktu yang dibutuhkan : ", e-s)

    halma = Halma(8, 10)
    bstate = halma.board_state
    for arr in bstate:
        print(arr, end="\n")
    postate = halma.possible_state(bstate, 1)

    statearridx = halma.local_search(postate,1)

    def print_state(arridx):
        for i in range(len(arridx)):
            print("\n")
            print("random state ke-"+str(i))
            for state in arridx[i]:
                print(state, end="\n")
                
    print_state(statearridx)

    def print_board(board):
        for i in range(len(board)):
            for j in range(len(board)):
                if j == len(board) - 1 :
                    print(board[i][j])
                else :
                    print(board[i][j], end=" ")












                    
    # a = Halma(8)
    # a.board_state[3][0] = 0 
    # a.board_state[3][1] = 1 
    # a.print_board()
    # res = (a.generate_all_move(a.board_state, (2,0) ))
    # for el in res:
    #     print("="*10)
    #     print_board(el)
    
    #====TEST=====#
    
    # b = Halma(8)
    # b.print_board()
    # print("="*90)
    # print_board(b.minimax_decision(1))
    # print("="*90)
    # b.board_state[7][7] = 0
    # b.board_state[5][5] = 2
    # print_board(b.minimax_decision(1))
    # print("="*90)
    # b.board_state[7][4] = 0
    # b.board_state[7][3] = 2
    # print_board(b.minimax_decision(1))
    # print("="*90)
    # b.board_state[4][7] = 0
    # b.board_state[3][7] = 2
    # print_board(b.minimax_decision(1))
    



# Objective func alt
        # player 1, player 2
        # ilustrasi prioritas:
        # player 2  player 1
        # 1 2 4 7        10
        # 3 5 8         9 6
        # 6 9         8 5 3
        # 10        7 4 2 1
        ### Alt 1
        # value = float('inf')
        # for n in range(self.bSize//2):
        #     for m in range(n+1):
        #         if player == 2:
        #             pos_i = m
        #             pos_j = n-m
        #         else: # player = 1
        #             pos_i = self.bSize-m-1
        #             pos_j = self.bSize-n+m-1
        #         if state[pos_i][pos_j] != player:
        #             # kalau isinya bukan pion dari player maka return
        #             # print(self.calculate_distance(position, (pos_i, pos_j)))
        #             value = min(value, self.calculate_distance(position, (pos_i, pos_j)))
        # return value
        ### Alt 2
        # if player == 2:
        #     return self.calculate_distance(position, (0,0))
        # else:
        #     return self.calculate_distance(position, (self.bSize-1, self.bSize-1))
        ### Alt 3
        # value = 0
        # for n in range(self.bSize//2):
        #     for m in range(n+1):
        #         if player == 2:
        #             pos_i = m
        #             pos_j = n-m
        #         else: # player = 1
        #             pos_i = self.bSize-m-1
        #             pos_j = self.bSize-n+m-1
        #         if state[pos_i][pos_j] == player:
        #             value -= 1
        # return value
        ### Alt 4

    # bad max min
    
    # def max_func(self, depth, player, pos):
    #     if player == 0:
    #         turn = 1
    #     else:
    #         turn = 0

    #     if depth == MAX_DEPTH or self.check_win_state(player):
    #         return self.objective_func(player, pos)
    #     maxval = float('-inf')
    #     # movetaken = None
        
    #     if self.check_win_state(player):
    #         return "Player " + str(player) + "Win"
    #     else:
    #         for neighbor in self.pos_A:
    #             validactions = self.valid_action(neighbor)
    #             for act in validactions:
    #                 # print(act)
    #                 maxval = max(maxval, self.min_func(depth+1, player, act[1]))
    #                 # print(maxval)
    #                 # tmp = self.objective_func(turn, act[1])
    #                 # # print(tmp)
    #                 # if(tmp > maxval):
    #                 #     maxzval = tmp
    #         # print("maxval "+str(maxval))
    #         return maxval

    # def min_func(self, depth, player, pos):
    #     if player == 0:
    #         turn = 1
    #     else:
    #         turn = 0
    
    #     if depth == MAX_DEPTH or self.check_win_state(player):
    #         # print(pos)
    #         return self.objective_func(turn, pos)
    #     minval = float('inf')
    #     # movetaken = None
        
    #     if self.check_win_state(player):
    #         return "Player " + str(player) + "Win"
    #     else:
    #         for neighbor in self.pos_A:
    #             validactions = self.valid_action(neighbor)
    #             for act in validactions:
    #                 # print(act)
    #                 minval = min(minval, self.max_func(depth+1, player, act[1]))
    #                 # print(minval)
    #                 # tmp = self.objective_func(turn, act[1])
    #                 # # print(tmp)
    #                 # if(tmp < minval):   
    #                 #     minval = tmp
    #         # print("minval "+str(minval))
    #         return minval
