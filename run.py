import os
import json
from flask import Flask, render_template, request, flash, redirect 

app = Flask(__name__)
app.secret_key = "some secret"

score = 0
attempt = 0

@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		with open("data/users.txt", "a") as user_list:
			user_list.writelines(request.form["username"] + "\n")
		return redirect(request.form["username"])
	return render_template("index.html")

@app.route('/<username>', methods=["GET", "POST"])
def user(username):
	with open("data/riddles.json", "r") as json_data:
		data = json.load(json_data)
	riddle_index = 0
	global score
	global attempt
	if request.method == "POST":
		riddle_index = int(request.form["riddle_index"])
		user_response = request.form["message"].lower()
		if data[riddle_index]["answer"] == user_response:
			riddle_index += 1
			score += 1
			attempt = 0
		else:
			attempt += 1
			flash("{} it is not the right answer. Try again and don't rush.\nAttempts used: {}".format(request.form["message"], attempt))
			if attempt == 2 :
				riddle_index += 1
				attempt = 0
				flash("Now try this riddle")
	if request.method == "POST":
		if riddle_index > 9:
			return render_template("gameover.html",username=username, score=score)



	return render_template("game.html", username=username, riddles=data, riddle_index=riddle_index)




	
@app.route('/leaderboard')
def leaderboard():
	return render_template("leaderboard.html")



if __name__ == '__main__':
   app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)