from flask import Flask, render_template, request, send_from_directory
import os, json

app = Flask('app')


@app.route('/')
def hello_world():
  return "Server ON i hope"


@app.route('/server/usermanage', methods=["post"])
def server_usermanage():
  data = request.json
  return data



app.run(host='0.0.0.0', port=8080)

