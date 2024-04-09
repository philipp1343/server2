from flask import Flask, request, jsonify
import random
import json

app = Flask(__name__) 


def generate_equation():
   
    while True:
        lhs = [random.randint(1, 10) for _ in range(4)]
        operators = [random.choice('+-*/') for _ in range(3)]

        equation = str(lhs[0])
        for i in range(3):
            equation += ' ' + operators[i] + ' ' + str(lhs[i+1])

        result = eval(equation)

        if result % 1 == 0:
            break
        
    equation_dict = {
        "operators": operators,
        "lhs": lhs,
        "result": result
    }

    with open("equation.json", "w") as json_file:
        json.dump(equation_dict, json_file, indent=4)

@app.route('/give-equations')
def give_equations():
    generate_equation()
    with open("equation.json", "r") as json_file:
        equation = json.load(json_file)
    return jsonify(equation)

@app.route('/solve-equation', methods=['POST'])
def solve_equation_route():
    
    equation = request.json 
    
    result = solve_equation(equation)
    actual_result = equation["result"]
    if result == actual_result:
        
        return jsonify({"result": "Success!"})
    else:
        return jsonify({"result": "You were wrong : ("})


def solve_equation(equation_dict):
    lhs = equation_dict["lhs"]
    operators = equation_dict["operators"]
    
    equation = str(lhs[0])
    for i in range(3):
        equation += ' ' + operators[i] + ' ' + str(lhs[i+1])
    print(equation)
    result = eval(equation)
    return result

if __name__ == '__main__':
    app.run(debug=True)
