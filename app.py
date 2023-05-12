from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/disaster_watch')
def disaster_watch():
    return render_template('disaster_watch.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/donate')
def donate():
    return render_template('Donate.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/notification')
def notification():
    return render_template('notification.html')

if __name__ == '__main__':
    app.run(debug=True)
