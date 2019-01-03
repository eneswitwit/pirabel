# import necessary packages
import string
import json
from scipy.integrate import quad
from sympy import integrate as indefinite
from sympy import diff
from sympy import Symbol
from sympy import latex
from fractions import Fraction

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

    decimal = int(value, int(number_system_input))
    result = convert_decimal_to_base_system(decimal, int(number_system_output))

    json_result = [
        {'result': result}
    ]

    return json.dumps(json_result)


def convert_decimal_to_base_system (n, base_system):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, int(base_system))
        if r >= 10:
            r = convert_base_to_letter(r)
        nums.append(str(r))
    return ''.join(reversed(nums))

def convert_base_to_letter (num):
    return pos_to_char(num-10).upper()


def pos_to_char(pos):
    return chr(pos + 97)

# rule of proportion 
@app.route("/rule-of-proportion/<value_1>/<value_2>/<value_3>/<value_4>")
def rule_of_proportionn(value_1, value_2, value_3, value_4):

    value_1=  float(value_1)
    value_2 = float(value_2)
    value_3 = float(value_3)
    value_4 = float(value_4)

    equal_zero = 0
    if value_1 == 0:
        equal_zero += 1 
    if value_2 == 0:
        equal_zero += 1
    if value_3 == 0:
        equal_zero += 1
    if value_4 == 0:
        equal_zero += 1

    if equal_zero != 1:
        return json.dumps({'error' : 'We need exactly 3 values inequal 0. We have now ' + str(equal_zero)})
        

    if value_1 == 0 or value_2 == 0:
        # compute proportion of value 3 and 4
        if value_2 == 0:
            prop = value_4/value_3
            value_2 = value_1 * prop
        else:
            prop = value_3/value_4
            value_1 = prop * value_2

    else:
        # compute proportion of value 1 and 2
        if value_4 == 0:
            prop = value_2/value_1
            value_4 = value_3 * prop
        else:
            prop = value_1/value_2
            value_3 = prop * value_4

    result = {
        'value_1' : value_1,
        'value_2' : value_2,
        'value_3' : value_3,
        'value_4' : value_4
    }


    json_result = [
        {'result': result}
    ]

    return json.dumps(json_result)

# fraction
@app.route("/fraction/<firstCounter>/<firstDenominator>/<operator>/<secondCounter>/<secondDenominator>")
def fraction(equation):

    firstCounter = eval(firstCounter)
    secondCounter = eval(secondCounter)

    firstFraction = Fraction(firstCounter, firstDenominator)
    secondFraction = Fraction(seconndCounter, secondDenominator)

    if operator == '+':
        result = firstFraction + secondFraction

    if operator == '-':
        result = firstFraction - secondFraction

    if operator == '*':
        result = firstFraction * secondFraction

    if operator == ':':
        result = firstFraction / secondFraction

    json_result = [
        {'resultCounter': result.numerator},
        {'resultDenominator': result.denominator},
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
