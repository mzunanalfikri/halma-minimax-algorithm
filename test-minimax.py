import random

MAX_DEPTH = 3

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
    return max_obj_value
    # return generated_state[best_state_idx] # harusnya ini yang dipakai


def possible_state(state):
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

if __name__ == "__main__":
    print(minimax_decision(4))