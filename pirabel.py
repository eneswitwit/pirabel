# import necessary packages
import string
import json
import subprocess

# math libs
from scipy.integrate import quad
from sympy import integrate as indefinite
from sympy import diff
from sympy import Symbol
from sympy import latex
from sympy.solvers import solve
from sympy import sympify
from sympy import exp, log, ln

from fractions import Fraction
from decimal import Decimal
from collections import OrderedDict

# auto deploy
from subprocess import Popen, PIPE
from os import path

# flask
from flask import Flask
from flask import request

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
    indefinite_result = indefinite(fx, Symbol('x'))
    integration_result = latex(sympify(str(integration(fx, down_boundary, upper_boundary)[0])))
    json_result = [
        {'indefinite': latex(sympify(str(indefinite_result)))},
        {'calculation': calculation(indefinite_result, down_boundary, upper_boundary)},
        {'result': integration_result}
    ]
    return json.dumps(json_result)


@app.route("/integrate/indefinite/<fx>")
def indefinite_route(fx):
    fx = convert_latex(fx)
    indefinite_result = latex(sympify(str(indefinite(fx, Symbol('x')))))
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
    left = sympify(fx)
    left = latex(left.subs(Symbol('x'), upper_boundary))
    right = sympify(fx)
    right = latex(right.subs(Symbol('x'), down_boundary))
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
@app.route("/fraction/<firstFactor>/<firstCounter>/<firstDenominator>/<operator>/<secondFactor>/<secondCounter>/<secondDenominator>")
def fraction(firstFactor, firstCounter, firstDenominator, operator, secondFactor, secondCounter, secondDenominator):


    fractionOne = Fraction(1)
    firstFractionCounter = Fraction(Decimal(firstFactor)*Decimal(firstCounter))
    firstFractionDenominator = fractionOne/Fraction(Decimal(firstDenominator))
    firstFraction = firstFractionCounter * firstFractionDenominator


    secondFractionCounter = Fraction(Decimal(secondFactor)*Decimal(secondCounter))
    secondFractionDenominator = fractionOne/Fraction(Decimal(secondDenominator))
    secondFraction = secondFractionCounter * secondFractionDenominator

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

# convert int to roman numbers
@app.route("/roman/<num>")
def convertArabicToRomam(num):

    num = int(num)
    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num > 0:
                roman_num(num)
            else:
                break

    romanString = "".join([a for a in roman_num(num)])

    return json.dumps(romanString)

@app.route("/arabic/<roman>")
def convertToRomanToArabic(roman):
    number = romanToInt(roman)
    return json.dumps(number)


def romanToInt(roman, values={'M': 1000, 'D': 500, 'C': 100, 'L': 50, 
                                'X': 10, 'V': 5, 'I': 1}):

    numbers = []

    for char in roman:
        numbers.append(int(values[char.upper()])) 

    total = 0

    if len(numbers) == 1:
        return numbers[0]

    else:
        for num1, num2 in zip(numbers, numbers[1:]):
            if num1 >= num2:
                total += num1
            else:
                total -= num1

    return total + num2



# compute zeros
@app.route("/compute-zero/<fx>")
def computeZero(fx):
    fx = convert_latex(fx)
    result = solve(fx, Symbol('x'))
    json_result = [latex(sympify(removeI(str(t)))) for t in result]
    return json.dumps(json_result)


def removeI(sol):
    index = sol.find('*I')
    if index != -1:
        return sol[:index]
    else:
        return sol

# helper functions
def convert_latex(fx):
    fx = fx.replace("{", "(")
    fx = fx.replace("}", ")")
    fx = fx.replace("^", "**")
    fx = fx.replace(":", "/")
    return fx


def convert_python(fx):
    fx = fx.replace("**", "^")
    fx = convert_exponents(fx)
    fx = fx.replace("*", "")
    return fx

def convert_exponents(fx):

    fx = fx.replace('^', '^{')
    index = fx.find('^{')
    newFx = fx

    while index != -1:

        # divide in substring 
        newFx = newFx[index+1:]

        newFxSpace = newFx.find(' ')

        if newFxSpace != -1:
            exponent = newFx[:newFxSpace]
            exponentNew = exponent + '}'
            # set in the } correctly
            fx = fx.replace(exponent, exponentNew)
        else:
            # set in the } correctly
            fx = fx + '}'


        # set new index 
        index = newFx.find('^{')

    return fx



# automatic deployment
@app.route("/deployment/pull", methods=['POST'])
def deploy():
    subprocess.call("/usr/bin/git pull", shell=True)
    return json.dumps('Deployed succesfully')





