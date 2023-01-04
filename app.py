from flask import Flask, render_template, request
import game as game
import pandas as pd
app = Flask(__name__)

player1_name = ""
player2_name = ""
bg = "1"
name = ""

@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/statistics')
def statistics():
    return render_template("statistics.html")

@app.route('/allPlayer')
def allPlayer():
    d = pd.read_csv('pong_game_stat.csv')
    df1 = pd.DataFrame(d)
    labels = list(df1["Name"])
    values1 = list(df1["Score"])
    values2 = list(df1["Total_games_played"])
    values3 = list(df1["Games_won"])
    values4 = list(df1["Games_lost"])
    return render_template("allPlayer.html",labels=labels,values1=values1,values2=values2,values3=values3,values4=values4)

@app.route('/singlePlayer', methods=['GET', 'POST'])
def singlePlayer():
    global name
    name=""
    if request.method == 'POST':
        name = request.form['name']
    if name != "":
        d = pd.read_csv('pong_game_stat.csv')
        df = pd.DataFrame(d)
        lst = list(df["Name"])
        name = name.upper()
        for i in range(len(lst)):
            if lst[i] == name:
                score = df.iloc[i]["Score"]
                played  = df.iloc[i]["Total_games_played"]
                won = df.iloc[i]["Games_won"]
                lost = df.iloc[i]["Games_lost"]
        final_lst = [score, played, won, lost]
        return render_template("singlePlayer.html",final_lst=final_lst,name=name)    
    return render_template("getName.html")


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global bg
    if request.method == 'POST':
        bg = request.form['bgno']
        return render_template("home.html")
    return render_template("settings.html")

@app.route('/tutorial')
def tutorial():
    return render_template("tutorial.html")

@app.route('/regame', methods=['GET', 'POST'])
def regame():
    if request.method == 'POST':
        if request.form['reply'].upper() != "YES":
            return render_template("home.html")
    return render_template("newgame.html")

@app.route('/newgame', methods=['GET', 'POST'])
def new_game():
    global player1_name
    global player2_name
    player1_name = ""
    player2_name = ""
    if request.method == 'POST':
        player1_name = request.form['player1']
        player2_name = request.form['player2']
    if player1_name != "":
        return render_template("regame.html",func = game.main(player1_name, player2_name,bg))
    return render_template("newgame.html")
    

if __name__ == '__main__':  
    app.run(debug=True)