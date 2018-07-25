import json
from scipy.integrate import quad

from flask import Flask
app = Flask(__name__)

@app.route("/integrate/<fx>")
def integrate(fx):
    fx = convert_latex(fx);
    return json.dumps(integration(fx)[0]);

if __name__ == "__main__":
    app.run(host='0.0.0.0')

def integration(fx):
    area = quad(integrand(fx), 0, 1);
    return area;

def convert_latex(fx):
    return fx.replace("^","**");

def integrand(fx):
    return eval("lambda x:" + fx);