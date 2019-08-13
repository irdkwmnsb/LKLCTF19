from flask import Flask
from flask import render_template_string, request, session, redirect
import secrets

app = Flask(__name__)
flag = 'LKLCTF{1s_7h1s_ha$h_c0lI1$ion}'
SALT = "Это нацист, это нацист, это нацист"
app.config["SECRET_KEY"] = secrets.token_bytes(10)


def hash(text):
    text += SALT
    p = 17
    s = 0
    for i in range(len(text)):
        s += p ** i * ord(text[i])

    return s


template = """
<form>
    <input name="text" placeholder="Paycheck"/>
    <input name="hash" placeholder="Hash"/>
    <button type="submit">Redeem</button>
</form>

<h3>{{msg}}</h3>

Your balance is <h2>{{session.money}}</h2>
<form action="/reset">
    <button type="submit">Reset money</buton>
</form>

"""


@app.route('/', methods=['GET'])
def index():
    H = request.args.get('hash', '')
    paycheck = request.args.get('text', '')

    if "money" not in session:
        session["money"] = 0

    if not (H and paycheck):
        return render_template_string(template)
    else:
        if hash(paycheck) == int(H) and paycheck.isprintable():
            if session["money"] != 0:
                return render_template_string(template, msg="You cant activate more than one paycheck. Please reset.")
            else:
                session["money"] += int(paycheck.split()[-1])
                if session["money"] >= 1000:
                    return render_template_string(template, msg=flag)
                else:
                    return render_template_string(template)
        else:
            print(H, paycheck, hash(paycheck))
            return render_template_string(template, msg='Bad paycheck: not-printable symbols or incorrect signature')


@app.route('/reset')
def reset():
    session["money"] = 0
    return redirect('/')

# if __name__ == '__main__':
#     app.config["SECRET_KEY"] = b"enis"
#     app.run(host="0.0.0.0", port=802)
