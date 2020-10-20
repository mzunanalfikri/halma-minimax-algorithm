from flask import Flask, request, jsonify
from halma import Halma


app = Flask(__name__)

@app.route('/')
def root():
    return "Hello world"

'''
request - body 
{
    "state" : array state game,
    "positon" : [x,y]
}
response :
{
    "possible-move" : [[x,y], [x1,y1]]
}
'''
@app.route('/possible-one-move')
def possible_one_move():
    state = request.json['state']
    position = request.json['position']
    possible_move = []
    halma = Halma(len(state), float('inf'))
    possible_move += halma.valid_actions_step(state, position)
    possible_move += halma.valid_actions_jump(state, position)
    return jsonify(possible_move = possible_move)

'''
request - body
{
    "state" : array state game,
    "player" : 1 or 2,
    "timelimit" : x (in second)
}
response 
{
    next_state = array of state
}
'''
@app.route('/best-decision-minimax', methods=['POST'])
def minimax():
    state = request.json['state']
    player = request.json['player']
    time_limit = request.json['timelimit']
    halma = Halma(len(state), time_limit)
    halma.board_state = state
    best_decision = halma.minimax_decision(player,False)
    return jsonify(next_state = best_decision)

@app.route('/minimax-local', methods=['POST'])
def minimax_local():
    state = request.json['state']
    player = request.json['player']
    time_limit = request.json['timelimit']
    halma = Halma(len(state), time_limit)
    halma.board_state = state
    best_decision = halma.minimax_decision(player,True)
    return jsonify(next_state = best_decision)

if __name__ == "__main__":
    app.run(debug=True)
