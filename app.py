from flask import Flask
from flask import render_template
from reactionbot import ReactionBot
import threading
app = Flask(__name__)
token = "MTIxOTU5NjYyNjc2MzcxNDY1Mw.GsqrCw.7CYe-qy_Go1HRNufCuMKECWaN9U--UynDC8OKk"
bot = ReactionBot()

thread = threading.Thread(target=bot.runBot)
@app.route('/')
def hellp():
    thread.start()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)