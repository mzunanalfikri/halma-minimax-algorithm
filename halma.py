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
    def calculate_distance(self, turn, position): 
        if turn == 0 :
            return ((self.bSize - position[0])**2 + (self.bSize - position[1])**2)**0.5
        else :
            return ((position[0])**2 + (position[1])**2)**0.5

    # generate list of tuple valid action (0, (i,j)) atau (1, (i,j))
    # 0 berarti gabisa jalan lagi
    # 1 berarti masih bisa jalan lagi
    def valid_action(self, position):
        listOfValidActions = []
        for i in range(position[0]-1, position[0]+2) :
            dif_i = i - position[0]

            if i >= 0:
                for j in range(position[1]-1, position[1]+2):
                    if j >= 0:
                        dif_j = j - position[1]
                        if self.board_state[i][j] == 0 :
                            listOfValidActions.append((0, (i,j)))
                        else : # lompatin 1 pion, masih bisa gerak lagi
                            jump_i = i + dif_i
                            jump_j = j + dif_j
                            if jump_i >= 0 and jump_j >= 0 :
                                if self.board_state[jump_i][jump_j] == 0:
                                    listOfValidActions.append((1, (jump_i, jump_j)))

        return listOfValidActions
    
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

if __name__ == "__main__":
    a = Halma(16)
    a.print_board()