from flask import Flask, request, jsonify
app = Flask(__name__)

from helpers import bar

import numpy as np
import sys
import ast



@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from the url parameter /getmsg/?name=
    name = request.args.get("name", None)

    # For debugging
    print(f"Received: {name}")

    response = {}

    # Check if the user sent a name at all
    if not name:
        response["ERROR"] = "No name found. Please send a name."
    # Check if the user entered a number
    elif str(name).isdigit():
        response["ERROR"] = "The name can't be numeric. Please send a string."
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome API!"

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.json
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome API!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "No name found. Please send a name."
        })



@app.route('/foo', methods=['POST']) 
def foo():
    content = request.get_json()
    response = {}
    response["nome"]=content['name']
    result = bar(response)
    return jsonify(result)
    
@app.route('/getMessage', methods=['POST'])
def getMessage():

    content = request.get_json()
    arg1 = int(content['arg1'])
    arg2 = list(eval(content['arg2']))
    arg3 = content['arg3']
    arg4 = int(content['arg4'])
    testarray = ast.literal_eval(arg3)
    t = np.matrix(testarray)
    #print(t)

    # map cell to cell, add circular cell to goal point
    points_list = arg2
    goal = arg4+1
    nR=10
    if(goal>100):
        nR=20
    #import networkx as nx
    #G=nx.Graph()
    #G.add_edges_from(points_list)
    #pos = nx.spring_layout(G)
    #nx.draw_networkx_nodes(G,pos)
    #nx.draw_networkx_edges(G,pos)
    #nx.draw_networkx_labels(G,pos)
    #plt.show()

    # how many points in graph? x points
    MATRIX_SIZE = goal+1

    # create matrix x*y
    R = np.matrix(np.ones(shape=(MATRIX_SIZE, MATRIX_SIZE)))
    R *= -1


    # assign zeros to paths and 100 to goal-reaching point
    #for point in points_list:
    #  print(point)
    #    if point[1] == goal:
    #        R[point] = 100
    #   elif point[1] == arg1:
    #	    R[point] = 50
    #    else:
    #        R[point] = 0
    #    if point[0] == goal:
    #        R[point[::-1]] = 100
    #    elif point[0] == arg1:
    #	    R[point[::-1]] = 50
    #    else:
        # reverse of point
    #        R[point[::-1]]= 0

    # add goal point round trip

    R = t
    R[0,goal]=-1
    R[goal,goal]= 100


    #print(R)


    Q = np.matrix(np.zeros([MATRIX_SIZE, MATRIX_SIZE]))

    # learning parameter
    gamma = 0.8

    initial_state = 1
    
    current_state_row = R[initial_state,]
    av_act = np.where(current_state_row >= 0)[1]
    available_act = av_act

    next_action = int(np.random.choice(available_act, 1))    
    action = next_action
   



    # Training
    scores = []
    listSteps = []
    for j in range(nR):
        for i in range(700):
            current_state = np.random.randint(0, int(Q.shape[0]))
           
            current_state_row_new = R[current_state,]
            av_act_new = np.where(current_state_row_new >= 0)[1]
            
            available_act_new = av_act_new
            next_action_new = int(np.random.choice(available_act_new, 1))
            action = next_action_new
            
            max_index = np.where(Q[action,] == np.max(Q[action,]))[1]

            if max_index.shape[0] > 1:
                max_index = int(np.random.choice(max_index, size=1))
            else:
                max_index = int(max_index)
            max_value = Q[action, max_index]

            Q[current_state, action] = R[current_state, action] + gamma * max_value
            #   print('max_value', R[current_state, action] + gamma * max_value)

            if (np.max(Q) > 0):
                score = np.sum(Q / np.max(Q) * 100)
            else:
                score = 0
            
            scores.append(score)
            # print('Score:', str(score))

        #print("Trained Q matrix:")
        #print(Q / np.max(Q) * 100)

        # Testing
        current_state = 0
        steps = [current_state]



        while current_state != goal:

            next_step_index = np.where(Q[current_state,] == np.max(Q[current_state,]))[1]
    
            if next_step_index.shape[0] > 1:
                next_step_index = int(np.random.choice(next_step_index, size=1))
            else:
                next_step_index = int(next_step_index)

            steps.append(next_step_index)
            current_state = next_step_index

        listSteps.append(steps)

    #print("Most efficient path:")
    
    
    
   
    counter = 0
    num = listSteps[0]

    for i in listSteps:
        curr_frequency = listSteps.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i   
    return(num)

  


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api! NE22W</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    
    
