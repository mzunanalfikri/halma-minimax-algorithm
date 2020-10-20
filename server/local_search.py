import random
import time
import math
import sys

sys.setrecursionlimit(10000)

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
                elif state[i][j] == 2: 
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

    # REVIEW ambil n random successor state dari possible state
    # REVIEW ambil 1 suksesor random
    # REVIEW itung min max, kalo max ambil >, kalo <= dibreak
    def local_search(self, init_state, player):
        arrstate = self.possible_state(init_state, player)
        # Ambil 25 persen dar total generated state
        NELM = 0
        if(len(arrstate) < 2):
            NELM = math.ceil(len(arrstate)/2)
        else:
            NELM = math.floor(len(arrstate)*0.5)
        # index randomizer
        x = random.sample(range(len(arrstate)), NELM)
        arr_local = []
        for idx in x:
            arr_local.append(arrstate[idx])

        arr_obj_local = []
        for state in arr_local:
            arr_obj_local.append(self.objective_func_board(state,player))

        randidx = random.sample(range(len(arr_local)), 1)
        randomed_state = arr_local[randidx[0]]

        arr_obj_local.sort(reverse=True)
        

        return randomed_state
    
    def local_search_decision(self, init_state, randomed_state, player, s):
        
        decided_state = [[0 for i in range(self.bSize)] for j in range(self.bSize)]
        init_obj = self.objective_func_board(init_state, player)
        rand_obj = self.objective_func_board(randomed_state, player)

        print("Obj val init_state: " + str(init_obj))
        print("Obj val randomed_state: " + str(rand_obj))
        
        if not self.check_win_state_board(init_state) :
            if time.time() - s > self.time_limit :
                return init_state
            if(rand_obj >= init_obj):
                decided_state = randomed_state
            else:
                decided_state = self.local_search_decision(init_state, self.local_search(init_state, player), player, s)
            
        return decided_state



if __name__ == "__main__":
    # i = 1
    # while (not halma.check_win_state_board(halma.board_state)):
    #     print("="*8, "turn", i, "="*8)
    #     print()
    #     print_board(halma.minimax_decision(1))
    #     halma.minimax_decision(2)
    #     i+=1
    #     print()
    # e = time.time()
    # s = time.time()
    # print("Waktu yang dibutuhkan : ", e-s)

    def print_state(state):
        for row in state:
            print(row, end="\n")

    def print_list_state(arridx):
        for i in range(len(arridx)):
            print("\n")
            print("random state ke-"+str(i))
            for state in arridx[i]:
                print(state, end="\n")
    
    def print_board(board):
        for i in range(len(board)):
            for j in range(len(board)):
                if j == len(board) - 1 :
                    print(board[i][j])
                else :
                    print(board[i][j], end=" ")

    halma = Halma(16, 10)
    bstate = halma.board_state
    print("Initial State")
    for arr in bstate:
        print(arr, end="\n")
    print()
    postate = halma.possible_state(bstate, 1)

    statearridx = halma.local_search(bstate,1)
    print(statearridx)
    # deciszon = halma.local_search_decision(bstate,statearridx,1)
    
    i=1
    while (not halma.check_win_state_board(bstate)):
        s = time.time()
        print("="*8, "turn", i, "="*8)
        print()
        bstate = halma.local_search_decision(bstate, halma.local_search(bstate, i%2+1), i%2+1,s)
        print_board(bstate)
        # halma.minimax_decision(2)
        i+=1
        print()
    
    # print_state(decision)
    # print_state(statearridx)