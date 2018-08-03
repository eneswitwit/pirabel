# import necessary packages
import json
from scipy.integrate import quad
from sympy import integrate as indefinite
from sympy import diff
from sympy import Symbol
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
    # create message object instance
    msg = MIMEMultipart()
    message = "Sehr geehrter Herr Jaworski, \n es gibt einen Grund zum Feiern. Schmeißen Sie den Grill an und holen Sie das kalte Bier raus. \n Ich freue mich Ihnen mitteilen zu dürfen, dass sich ein neuer Subscriber für Scooya angemeldet hat. \n Email: " + email + " \n Hochachtungsvoll, Ihr Computer"
 
    # setup the parameters of the message
    password = "390495616Ew"
    msg['From'] = "witwitenes@gmail.com"
    msg['To'] = "eneswitwit@live.de"
    msg['Subject'] = "Scooya Subscription"
 
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
 
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
 
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
 
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
 
    server.quit()

    return json.dumps('Email written to emails.txt');