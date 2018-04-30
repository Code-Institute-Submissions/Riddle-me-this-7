import os
import json
from flask import Flask, render_template, request, flash, redirect, session 

app = Flask(__name__)
app.secret_key = "some secret"
#global variables used to play tha game
score = 0
attempt = 0
#function that will reset the score 
def reset_score():
	global score
	score = 0
#function for writing into a json file
def append_record_to_json_file(record, file):
	leaderboard=[]

	with open(file, "r") as f:
		leaderboard = json.load(f)
	leaderboard.append(record)
	with open(file, "w") as f:
		json.dump(leaderboard, f, sort_keys=True, indent=4)

@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		reset_score()
		session["user"] = request.form["username"]
		return redirect(session["user"])
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
				flash("Now try this new riddle")
		if riddle_index > 9:
		#user data that will be stored in the leaderboard.json file
			entry = {
			"name" : session["user"],
			"score" : score
			}
		#calling the function to write the user data into the json file 
			append_record_to_json_file(entry, "data/leaderboard.json")

			session.pop("user", None)#close session
			return render_template("gameover.html",username=username, score=score)
	return render_template("game.html", username=username, riddles=data, riddle_index=riddle_index)


@app.route('/leaderboard')
def leaderboard():
	with open("data/leaderboard.json", "r") as json_data:
		data = json.load(json_data)
		sorted_data = sorted(data, key = lambda i: i["score"], reverse=True) #sort the data by the score value
	return render_template("leaderboard.html", leaderboard=sorted_data)


if __name__ == '__main__':
   app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)