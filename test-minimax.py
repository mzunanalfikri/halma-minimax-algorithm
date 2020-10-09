import random

MAX_DEPTH = 3

'''
input state
return state (best move)
'''
def minimax_decision(state):
    generated_state = possible_state(state)
    print(generated_state)
    best_state_idx = 0
    max_obj_value = float('-inf')
    for i in range(len(generated_state)):
        print("obj value :", min_value(state,1))
        temp_obj_value = min_value(state, 1)
        if  temp_obj_value > max_obj_value :
            max_obj_value = temp_obj_value
            best_state_idx = i
    # return max_obj_value
    return generated_state[best_state_idx] # harusnya ini yang dipakai


def possible_state(state):
    #iterasi semua pion, pakai fungsi generate_all_move
    return [random.random() for i in range(2)]

def min_value(state, depth):
    print("depth : ", depth)
    if depth == MAX_DEPTH or check_win_state(state):
        return objective_func(state)
    
    v = float('inf')
    for s in possible_state(state):
        v = min(v, max_value(s, depth + 1))
    return v

def max_value(state, depth):
    print("depth : ", depth)
    if depth == MAX_DEPTH or check_win_state(state):
        return objective_func(state)

    v = float('-inf')
    for s in possible_state(state):
        v = max(v, min_value(s, depth + 1))
    return v

def check_win_state(state):
    return False

def objective_func(state):
    return random.random()

# ini masih bayangan
def generate_all_move(state, positon):
    pos_move = [] #hasil
    queue = []
    expand = []
    #generate yang satu step
    pos_move.append(generate_one_step(state, positon))
    #inisiasi gerakan yang lompat
    init_jump_step = generate_jump_step(state, position)
    pos_move.append(init_jump_step)
    queue.append(init_jump_step)
    while len(queue) != 0 :
        temp_move = queue.pop()
        if temp_move not in expand: #kalo belom pernah di expand, expand!
            expand.append(temp_move)
            #generate semua langkah loncat yang mungkin dari yang di expand
            temp_jump_move = generate_jump_step(state, temp_move)
            for move in temp_jump_move:
                if move not in pos_move: 
                    pos_move.append(move)
                if move not in queue: # masukin ke queue buat generate lagi nanti
                    queue.append(move)
    return pos_move
            
if __name__ == "__main__":
    print(minimax_decision(4))