import json
from scipy.integrate import quad
from sympy import integrate as indefinite
from sympy import Symbol

from flask import Flask
app = Flask(__name__)

# routes
@app.route("/")
def home():
    return json.dumps("Pirabel API 1.0");

@app.route("/integrate/<fx>/<down_boundary>/<upper_boundary>")
def integrate_route(fx, down_boundary, upper_boundary):
    fx = convert_latex(fx);
    indefinite_result = convert_python(str(indefinite(fx, Symbol('x'))));
    integration_result = integration(fx, down_boundary, upper_boundary)[0];
    json_result = [
        ['indefinite', indefinite_result],
        ['calculation', calculation(indefinite_result, down_boundary, upper_boundary)],
        ['result', integration_result]
    ];
    return json.dumps(json_result);

@app.route("/integrate/indefinite/<fx>")
def indefinite_route(fx):
    fx = convert_latex(fx);
    indefinite_result = convert_python(str(indefinite(fx, Symbol('x'))));
    json_result = [
        ['indefinite', indefinite_result]
    ];
    return json.dumps(json_result);

if __name__ == "__main__":
    app.run(host='0.0.0.0')

#integration
def integration(fx, down_boundary, upper_boundary):
    down_boundary = float(down_boundary);
    upper_boundary = float(upper_boundary);
    area = quad(integrand(fx), down_boundary, upper_boundary);
    return area;

def integrand(fx):
    return eval("lambda x:" + fx);

def calculation(fx, down_boundary, upper_boundary):
    left = fx.replace("x", upper_boundary);
    right = fx.replace("x", down_boundary);
    return left + " - " + right;

#helper functions 
def convert_latex(fx):
    return fx.replace("^","**");

def convert_python(fx):
    return fx.replace("**","^");    
