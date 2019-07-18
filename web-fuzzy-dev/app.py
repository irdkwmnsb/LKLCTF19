from flask import Flask, render_template, session, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from fish_text_api import FishText
import secrets
import traceback

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)
app.secret_key = secrets.token_hex(16)

ft = FishText()


@app.errorhandler(500)
def error(error):
    return render_template('flag.html', stacktrace=traceback.format_exc()), 500


@app.route("/page/<random>", methods=["GET", "POST"])
@limiter.limit("2 per second")
def page(random):
    if 'num' not in session:
        session['num'] = 0

    session['num'] += 1

    if session['num'] >= 70:
        if request.method == "GET":
            return render_template('submit.html')
        else:
            # TODO: Здесь будет часть с fuzzing-ом. Нужно написать сломанный чекер email-ов
            raise Exception("LKLCTF{FUzz1ng_plUs_craWl1ng_827unF}")
            return "ok"
    else:
        return render_template('menu.html', titles=ft.title(7).split("\n\n"),
                               pages=[secrets.token_hex(8) for _ in range(6)])


@app.route("/")
def index():
    return render_template("index.html", page=[secrets.token_hex(8) for _ in range(6)])


if __name__ == "__main__":
    app.run()
