from flask import Flask, render_template, request, redirect, url_for, make_response
import json
import os
import uuid
import io
import base64
from pydub import AudioSegment

from models.blenderbot import HuggingfaceBlenderbot

import nemo
import nemo.collections.asr as nemo_asr

app = Flask(__name__, static_url_path='', static_folder='static')

history = []

#nlp_model = HuggingfaceBlenderbot()
#asr_model = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5Base-En")

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

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


@app.route('/txtBtnClick', methods=('GET', 'POST'))
def txtBtnClick(): 
    if request.method == 'POST':
        print (request.get_json())
        res = make_response({'text': 'response'}, 200)
        return res
    else:
        return ''

@app.route('/recordBtnClick', methods=('GET', 'POST'))
def recordBtnClick():
    if request.method == 'POST':
        pass
    return "hiel"

@app.route('/clearBtnClick', methods=('GET', 'POST'))
def clearBtnClick():
    return ""


@app.route('/inference', methods=('GET', 'POST'))
def infer():
    if request.method == 'POST':
        print ('infer called!!!')
        record = request.json.get('record')
        record = base64.b64decode(record.encode('utf-8'))

        as_audio = AudioSegment.from_file(
                io.BytesIO(record)).\
                        set_frame_rate(16000).set_channels(1)

        wavpath = 'tmp/tmpaudio.wav'
        as_audio.export(wavpath, format='wav')
        transcript = asr_model.transcribe(paths2audio_files=[wavpath])
        print ('transcript: ', transcript)

        response = nlp_model([], transcript[0])
        print ('response: ', response)

        res = make_response({'transcript': transcript[0], 'response': response}, 200)
        return res


