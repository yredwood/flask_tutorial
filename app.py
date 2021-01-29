from flask import Flask, render_template, request, redirect, url_for
import json

from models.blenderbot import HuggingfaceBlenderbot

app = Flask(__name__, static_url_path='', static_folder='static')

history = []
#bot = HuggingfaceBlenderbot()

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        sentence = request.form['text']

        #res = bot(history, sentence)
        res = sentence
        history.append({'user': sentence, 'bot': res})
        print (history)
    else:
        print ('get called')
    
    if len(history) > 0:
        return render_template('base.html', history=history)
    else:
        return render_template('base.html', history={})

@app.route('/clear', methods=('GET', 'POST'))
def clear_hist():
    if request.method == 'POST':
        global history
        history = []
        print ('clear history')
    return redirect(url_for('index'))
#    return render_template('base.html', sentence=history)

@app.route('/record', methods=('GET', 'POST'))
def record():
    print (request.form)
    print ('record and recognition-append history')
    global history
    history.append({'user': 'some speech singal..', 'bot': 'hello (in speech)'})
    return redirect(url_for('index'))


@app.route('/textbut', methods=('GET', 'POST'))
def nonamefunc(): 
    text = (request.form['text'])
    return text



