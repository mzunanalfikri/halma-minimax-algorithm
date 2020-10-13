# import sys 
# sys.setrecursionlimit(1000) 
import random
import time

MAX_DEPTH = 1
class Halma:
    def __init__(self, size):
        self.bSize = size
        self.board_state = [[0 for i in range(size)] for j in range(size)]
        self.pos_A = []
        self.pos_B = []
        self.init_board()

    def init_board(self):
        for i in range(self.bSize):
            for j in range(self.bSize):
                if i < self.bSize/2 and j < self.bSize/2 - i :
                    self.board_state[i][j] = 1
                    self.pos_A.append((i,j))

                if i >= self.bSize/2 and j >= self.bSize*3/2 + - 1 - i:
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

            
    
    def generate_valid_state(self, board, player) :
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
        # player 1, player 2
        # ilustrasi prioritas:
        # player 2  player 1
        # 1 2 4 7        10
        # 3 5 8         9 6
        # 6 9         8 5 3
        # 10        7 4 2 1
        
        for n in range(self.bSize//2):
            for m in range(n+1):
                if player == 2:
                    pos_i = m
                    pos_j = n-m
                else: # player = 1
                    pos_i = self.bSize-m-1
                    pos_j = self.bSize-n+m-1
                if state[pos_i][pos_j] != player:
                    # kalau isinya bukan pion dari player maka return
                    # print(self.calculate_distance(position, (pos_i, pos_j)))
                    return self.calculate_distance(position, (pos_i, pos_j))

    def eval_board(self, turn):
        map_obj = []
        if turn == 0:
            for p in self.pos_A:
                map_obj.append(self.objective_func(self.board_state, turn, p))
        else:
            for p in self.pos_B:
                map_obj.append(self.objective_func(self.board_state, turn, p))

        return map_obj

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
    #                 #     maxval = tmp
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

    # mengembalikan keputusan terbaik dari suatu state dan player tertentu 
    def minimax_decision(self, player):
        generated_state = self.possible_state(self.board_state, player)
        # for state in generated_state:
        #     print_board(state)
        #     print("*"*90)
        best_state_idx = 0
        max_obj_value = float('-inf')
        for i, state in enumerate(generated_state):
            # print("obj value :", self.min_value(state,1, player))
            temp_obj_value = self.min_value(state, 1, player)
            if  temp_obj_value > max_obj_value :
                max_obj_value = temp_obj_value
                best_state_idx = i
        # return max_obj_value
        self.board_state = generated_state[best_state_idx]
        return generated_state[best_state_idx] # harusnya ini yang dipakai

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

    def min_value(self, state, depth, player):
        if depth == MAX_DEPTH or self.check_win_state_board(state, player):
            return self.objective_func_board(state, player)
        
        v = float('inf')
        for s in self.possible_state(state, player):
            v = min(v, self.max_value(s, depth + 1, player))
        return v

    def max_value(self, state, depth, player):
        if depth == MAX_DEPTH or self.check_win_state_board(state, player):
            return self.objective_func_board(state, player)

        v = float('-inf')
        for s in self.possible_state(state, player):
            v = max(v, self.min_value(s, depth + 1, player))
        return v

    # check win state dari suatu board
    def check_win_state_board(self, state, player):
        assert player == 1 or player == 2
        pion = []
        for i in range(self.bSize):
            for j in range(self.bSize):
                if state[i][j] == player:
                    pion.append((i,j))
        if player == 1 :
            for x,y in pion :
                if x + y < self.bSize*3/2 - 1:
                    return False
            return True
        else :
            for x,y in pion :
                if x + y > self.bSize/2 - 1 :
                    return False
            return True

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

if __name__ == "__main__":
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
    s = time.time()
    
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
    
    halma = Halma(8)
    i = 1
    while (not halma.check_win_state(0) or not halma.check_win_state(1)):
        print("="*8, "turn", i, "="*8)
        print_board(halma.minimax_decision(1))
        print_board(halma.minimax_decision(2))
        i+=1
        print()
    e = time.time()
    print("Waktu yang dibutuhkan : ", e-s)
