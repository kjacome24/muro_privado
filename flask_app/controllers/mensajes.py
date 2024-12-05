from flask_app import app
from flask import render_template, redirect,request,session
from flask_app.models.mensaje import Mensaje
from flask_app.models.usuario import Usuario

@app.route('/dashboard')
def dashboard():
    if session.get('id') == None:
        return redirect('/')
    usuarios = Usuario.get_all()
    data = {
        "receiver_id": session['id']
    }
    mensajes = Mensaje.mensajes_recibidos(data)
    numero_mensajes = len(mensajes)
    mensajes_enviados = Mensaje.mensajes_enviados({
        "sender_id" : session['id']
    })
    mensajes_enviados = mensajes_enviados['contador']
    return render_template('dashboard.html', usuarios=usuarios, mensajes=mensajes, numero_mensajes = numero_mensajes, mensajes_enviados=mensajes_enviados )


@app.route('/enviar_mensaje', methods = ['POST'])
def enviar_mensaje():
    print(request.form)
    data = {
        "contenido" : request.form['contenido'],
        "sender_id" : request.form['sender_id'],
        "receiver_id" : request.form['receiver_id']
    }
    print(data)
    if not Mensaje.validar(data):
        return redirect('/dashboard')
    Mensaje.guardar(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>', methods = ['POST','GET'])
def eliminar_mensaje(id):
    data = {
        "id" : id
    }
    Mensaje.eliminar(data)
    return redirect('/dashboard')