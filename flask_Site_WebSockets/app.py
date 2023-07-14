import random
import re
import sys
from threading import Lock

from flask import Flask, render_template, url_for, session, request, copy_current_request_context, session
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from flask_sock import Sock

from threading import Lock
import json
import os.path
import websocket

import requests

async_mode = None;


# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime #Importa tempo e data
app = Flask(__name__)#template_folder='templates',  static_folder='static'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

app.config['SECRET_KEY'] = 'secret!'
sock = Sock(app)

#Usar ws invés de http
ip = "ws://192.168.15.43/"  # LEMBRETE: Colocar ip ESP
ws = websocket.WebSocket()
ws.connect(ip)
#ws = requests.get(ip)
#ws.close() #Desconcetar
def background_thread():
    count = 0
    co = 0
    while True:
        # Espera 3 segundos
        #socketio.sleep(3)

        # Aumenta contador


        # Envia texto para Websocket do Esp
        ws.send("Ler Dados")

        # Recebe um texto de resposta do websocket do Esp
        result = ws.recv()
        if result == "SIM":
            count += 1
        # Envia o dado recebido para o websocketio do site
        #socketio.emit({'data': 'Bitcoin current price (USD): ' + result, 'count': count})
        socketio.emit('my_response',
                      {'data': result, 'count': count})
        print("thread")
        print(co)
        co+=1
        #emit('Botao', {'data': result})

'''
@sock.route("/rev")
def fun(ws):
   while True:
       texto = ws.receive()
       ws.send(texto[::-1])

def Overwrite():
   f = open("teste.json", 'r')
   data = f.read()
   #LEMBRETE COLOCAR WS.GET aqui
   data = {"Botao": str(json.load(data).get("Botao"))}
   f.close()
   f = open("teste.json", 'w')
   emit("Sinal",data,broadcast=True)
'''


@app.route('/')
def home():
    # f = open("teste.json", 'r')
    # data = {"Botao": str(json.load(f).get("Botao"))}
    return render_template('index.html', async_mode=socketio.async_mode)


# talvez precise de algum nome
@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'count': session['receive_count']})


# Receive the test request from client and send back a test response
@socketio.on('test_message')
def handle_message(data):
    print('received message: ' + str(data))
    emit('test_response', {'data': 'Test response sent'})


# Broadcast a message to all clients
@socketio.on('broadcast_message')
def handle_broadcast(data):
    print('received: ' + str(data))
    emit('broadcast_response', {'data': 'Broadcast sent'}, broadcast=True)


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})
    # colocar write file no final do video


# ws = websocket.WebSocket()
# ws.connect("ws://192.168.15.43")
# print("Connected to WebSocket server")

# str = input("Say something: ")
# selfhost = "127.0.0.1:5000"
# ws.send(selfhost)

# Wait for server to respond and print it
# result = ws.recv()
# print("Received: " + result)

'''
#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    dateCreated = db.Column(db.DateTime,default=datetime.utcnow())
    def __repr__(self):
        return '<Task %r>' % self.id

'''

'''
@app.route('/overwrite')#methods =['POST','GET']
def Dados():
    #Envia texto para Websocket do Esp
    ws.send("Ler Dados")
    #Recebe o dado
    result = ws.recv()
    print("Received: " + result)
    #state = request.args.get('Botao')
    s = {
        "Botao" : result
    }
    fname  =os.path.join(app.static_folder,"sample.json")

    with open(fname,"w") as outfile:
        json.dump(s,outfile)
    return 'overwrite com sucesso: Botão ligado?' + result

    #if request.method == 'POST':
    #    return render_template()
'''

'''
@app.route('/read')
def read():
    fname = os.path.join(app.static_folder, "sample.json")
    with open(fname, 'r') as openfile:
        json_obj = json.load(openfile)

    return json_obj['Botao']


@app.route('/toText/<usr>')
def user(usr):
    return f"<h1>{usr}</h1>"


# Termina conexão
@app.context_processor
def inject_load():
    if sys.platform.startswith('linux'):
        with open('/proc/loadavg', 'rt') as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {'load1': load[0], 'load5': load[1], 'load15': load[2]}

'''
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    socketio.run(app, host='0.0.0.0', port=5000)
    # app.run()
    # SocketIO.run(app)
    '''# Termina conexão
@app.context_processor
def inject_load():
    if sys.platform.startswith('linux'):
        with open('/proc/loadavg', 'rt') as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {'load1': load[0], 'load5': load[1], 'load15': load[2]}
'''
