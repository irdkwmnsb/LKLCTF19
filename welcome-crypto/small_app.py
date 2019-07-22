from flask import Flask
from flask import render_template_string, request
app = Flask(__name__)
flag = 'LKLCTF{придумайте флаг пж ребятаа}'

def hash(text):
	prime = 53
	s = 0
	for i in range(len(text)):
		s += prime**i*ord(text[i])

	return s

template = """
<form><input name="password"/><button type="submit">log in</button></form>
{{flag}}
"""


@app.route('/', methods=['GET'])
def index():
	passw = request.args.get('password', 'lox')
	print(passw, hash(passw))
	if passw == 'lox':
		return render_template_string(template)
	else:
		if hash(passw) == hash("3=1`;zqE#F!245C"):
			return render_template_string(template, flag=flag)
		else:
			return render_template_string(template, flag='wrong pass')


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=802)