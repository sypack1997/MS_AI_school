from flask import Flask
import sys
app =Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello'

@app.route('/1')
def One():
    return '{msg:"1 Page"}'
@app.route('/2')
def Two():
    return '{msg:"2 Page"}'