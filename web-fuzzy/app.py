from flask import Flask, render_template, session, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import secrets
import traceback
import re
import os
import json
import subprocess

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)
app.secret_key = secrets.token_hex(16)
graph = {}

app.jinja_env.filters['zip'] = zip

@app.before_first_request
def load_graph():
    global graph
    graph = json.load(open("graph.json"))


@app.errorhandler(500)
def error(error):
    return render_template('flag.html', stacktrace=traceback.format_exc() + ""), 500


email_regex = re.compile(r"(?P<name>\w+)@(?P<domain>\w+.+)")
ping_percent_regex = re.compile(r"(\d+)%")
def try_ping(domain):
    d = subprocess.getoutput(f"ping {domain} -c 1 -W 2")
    r = ping_percent_regex.search(d)
    return r


@app.route("/page/<page_n>", methods=["GET", "POST"])
def page(page_n):
    if page_n not in graph or page_n == 'root':
        return abort(404)
    if graph[page_n] == True:
        if request.method == "GET":
            return render_template('submit.html')
        else:
            if 'email' not in request.form:
                abort(400)
            email = request.form['email']
            r = email_regex.match(email)
            p = try_ping(r['domain'])
            if p[1] == '0':
                return "ok"
            else:
                return f"The mail server seems to be down. {p[0]} packets lost"

    else:
        node = graph[page_n]
        return render_template('menu.html',
                               #titles=ft.title(len(node['children']) + 1),
                               titles=[secrets.token_hex(2) for _ in range(len(node['children']) + 2)],
                               # Это здесь потому что у меня нет интернета в пути.
                               parent=node['parent'],
                               pages=node['children'])


@app.route("/")
def index():
    return render_template("index.html", page=graph['root'])


if __name__ == "__main__":
    app.run()
