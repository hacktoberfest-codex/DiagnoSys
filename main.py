from flask import Flask, url_for, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    return ({'message':'Hello World'})

if __name__ == '__main__':
    app.run(debug=True,port=5002)
