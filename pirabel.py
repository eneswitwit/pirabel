import json
from scipy.integrate import quad
from sympy import integrate as indefinite
from sympy import diff
from sympy import Symbol
import smtplib


# flask
from flask import Flask
app = Flask(__name__)
if __name__ == "__main__":
    app.run(host='0.0.0.0')

# routes
@app.route("/")
def home():
    return json.dumps("Pirabel API 1.0");

# integration routes
@app.route("/integrate/<fx>/<down_boundary>/<upper_boundary>")
def integrate_route(fx, down_boundary, upper_boundary):
    fx = convert_latex(fx);
    indefinite_result = convert_python(str(indefinite(fx, Symbol('x'))));
    integration_result = integration(fx, down_boundary, upper_boundary)[0];
    json_result = [
        {'indefinite': indefinite_result},
        {'calculation': calculation(indefinite_result, down_boundary, upper_boundary)},
        {'result': integration_result}
    ];
    return json.dumps(json_result);

@app.route("/integrate/indefinite/<fx>")
def indefinite_route(fx):
    fx = convert_latex(fx);
    indefinite_result = convert_python(str(indefinite(fx, Symbol('x'))));
    json_result = [
        {'indefinite': indefinite_result}
    ];
    return json.dumps(json_result);

# differentation routes
@app.route("/differentiate/<fx>")
def differentiate_route(fx):
    fx = convert_latex(fx);
    differentation_result = convert_python(str(diff(fx, Symbol('x'))));
    json_result = [
        {'derivative' :differentation_result}
    ];
    return json.dumps(json_result);



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

#derivative


#helper functions 
def convert_latex(fx):
    return fx.replace("^","**");

def convert_python(fx):
    return fx.replace("**","^");    


# scooya 
@app.route("/scooya/<email>")
def scooya_subscribe(email):
    # write to txt
    emails = open('emails.txt','a');
    emails.write(',' + email);
    emails.close();

    # write email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("witwitenes@gmail.com", "390495616Ew")

    msg = " Neuer Subscriber fuer scooya.de: " + email;
    server.sendmail("witwitenes@gmail.com", "seoptix@googlemail.com", msg);
    server.quit()

    return json.dumps('Email written to emails.txt');