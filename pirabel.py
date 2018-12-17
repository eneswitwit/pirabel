# import necessary packages
import json
from scipy.integrate import quad
from sympy import integrate as indefinite
from sympy import diff
from sympy import Symbol
from sympy import latex

# flask
from flask import Flask

app = Flask(__name__)
if __name__ == "__main__":
    app.run(host='0.0.0.0')


# routes
@app.route("/")
def home():
    return json.dumps("Pirabel API 1.0")


# integration routes
@app.route("/integrate/<fx>/<down_boundary>/<upper_boundary>")
def integrate_route(fx, down_boundary, upper_boundary):
    fx = convert_latex(fx)
    indefinite_result = convert_python(str(indefinite(fx, Symbol('x'))))
    integration_result = integration(fx, down_boundary, upper_boundary)[0]
    json_result = [
        {'indefinite': indefinite_result},
        {'calculation': calculation(indefinite_result, down_boundary, upper_boundary)},
        {'result': integration_result}
    ]
    return json.dumps(json_result)


@app.route("/integrate/indefinite/<fx>")
def indefinite_route(fx):
    fx = convert_latex(fx)
    indefinite_result = convert_python(str(indefinite(fx, Symbol('x'))))
    json_result = [
        {'indefinite': indefinite_result}
    ]
    return json.dumps(json_result)


# differentation routes
@app.route("/differentiate/<fx>")
def differentiate_route(fx):
    fx = convert_latex(fx)
    differentation_result = convert_python(str(diff(fx, Symbol('x'))))
    json_result = [
        {'derivative': differentation_result}
    ]
    return json.dumps(json_result)


# integration
def integration(fx, down_boundary, upper_boundary):
    down_boundary = float(down_boundary)
    upper_boundary = float(upper_boundary)
    area = quad(integrand(fx), down_boundary, upper_boundary)
    return area


def integrand(fx):
    return eval("lambda x:" + fx)


def calculation(fx, down_boundary, upper_boundary):
    left = fx.replace("x", upper_boundary)
    right = fx.replace("x", down_boundary)
    return left + " - " + right


# circle
@app.route("/circle/<input_value>")
def circle_route(input_value):
    equal_sign_index = input_value.find('=')
    value_type = input_value[:equal_sign_index]

    json_result = [
        {'debug': value_type}
    ]
    return json.dumps(json_result)

# convert number systems
@app.route("/convert-number-systems/<number_system_input>/<number_system_output>/<value>")
def convert_number_systems(number_system_input, number_system_output, value):

    result = int(value, number_system_input)

    json_result = [
        {'result': result}
    ]

    return json.dumps(json_result)

# helper functions
def convert_latex(fx):
    fx = fx.replace("{", "(")
    fx = fx.replace("}", ")")
    fx = fx.replace("^", "**")
    return fx


def convert_python(fx):
    fx = fx.replace("(", "{")
    fx = fx.replace(")", "}")
    fx = fx.replace("**", "^")
    return fx
