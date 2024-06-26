from flask import Flask
from flask import render_template
from reactionbot import ReactionBot
import threading
app = Flask(__name__)
bot = ReactionBot()

thread = threading.Thread(target=bot.runBot)
@app.route('/')
def hellp():
    thread.start()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=10000)
