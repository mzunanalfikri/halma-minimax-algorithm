# import sys 
# sys.setrecursionlimit(1000) 

MAX_DEPTH = 3
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
    def valid_action(self, state, position):
        listOfValidActions = []
        for i in range(position[0]-1, position[0]+2) :
            dif_i = i - position[0]

            if i >= 0 and i < self.bSize:
                for j in range(position[1]-1, position[1]+2):
                    if j >= 0 and j < self.bSize:
                        dif_j = j - position[1]
                        if state[i][j] == 0 :
                            listOfValidActions.append((0, (i,j)))

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
                            if state[jump_i][jump_j] == 0:
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
                listOfValidState.append((state, pos, action[1], action[0]))
        
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
    
    def objective_func(self, turn, position):
        # turn = 0 (player 1), turn = 1 (player 2)
        # ilustrasi prioritas:
        # turn 1    turn 0
        # 1 2 4 7        10
        # 3 5 8         9 6
        # 6 9         8 5 3
        # 10        7 4 2 1
        
        for n in range(self.bSize//2):
            for m in range(n+1):
                if turn == 1:
                    pos_i = m
                    pos_j = n-m
                else: # turn = 0
                    pos_i = self.bSize-m-1
                    pos_j = self.bSize-n+m-1
                if self.board_state[pos_i][pos_j] != turn+1:
                    # kalau isinya bukan pion dari turn maka return
                    # print(pos_i, pos_j)
                    return self.calculate_distance(position, (pos_i, pos_j))

    def eval_board(self, turn):
        map_obj = []
        if turn == 0:
            for p in self.pos_A:
                map_obj.append(self.objective_func(turn, p))
        else:
            for p in self.pos_B:
                map_obj.append(self.objective_func(turn, p))

        return map_obj

    def max_func(self, depth, player, pos):
        if player == 0:
            turn = 1
        else:
            turn = 0

        if depth == MAX_DEPTH or self.check_win_state(player):
            return self.objective_func(player, pos)
        maxval = float('-inf')
        # movetaken = None
        
        if self.check_win_state(player):
            return "Player " + str(player) + "Win"
        else:
            for neighbor in self.pos_A:
                validactions = self.valid_action(neighbor)
                for act in validactions:
                    # print(act)
                    maxval = max(maxval, self.min_func(depth+1, player, act[1]))
                    # print(maxval)
                    # tmp = self.objective_func(turn, act[1])
                    # # print(tmp)
                    # if(tmp > maxval):
                    #     maxval = tmp
            # print("maxval "+str(maxval))
            return maxval

    def min_func(self, depth, player, pos):
        if player == 0:
            turn = 1
        else:
            turn = 0
    
        if depth == MAX_DEPTH or self.check_win_state(player):
            # print(pos)
            return self.objective_func(turn, pos)
        minval = float('inf')
        # movetaken = None
        
        if self.check_win_state(player):
            return "Player " + str(player) + "Win"
        else:
            for neighbor in self.pos_A:
                validactions = self.valid_action(neighbor)
                for act in validactions:
                    # print(act)
                    minval = min(minval, self.max_func(depth+1, player, act[1]))
                    # print(minval)
                    # tmp = self.objective_func(turn, act[1])
                    # # print(tmp)
                    # if(tmp < minval):   
                    #     minval = tmp
            # print("minval "+str(minval))
            return minval

if __name__ == "__main__":
    a = Halma(16)
    a.print_board()
    # print(a.board_state[1][7])
    # ev = a.eval_board(0)
    # for e in ev:
    #     print(e)
    # # a.board_state[15][15] = 1
    # print(a.objective_func(0,(0,0)))
    # print("Max : " + str(a.max_func(1, 1, (0,0))))
    # print("Min : " + str(a.min_func(1, 1, (0,0))))
    print(a.copy_board([[1,2,3],[4,5,6],[7,8,9]]))