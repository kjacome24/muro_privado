from flask_app import app
from flask import render_template, redirect,request,session
from flask_app.models.usuario import Usuario
#1. Asegurarse de que la libreria esta installada y que se importe en el controladoro
from flask_bcrypt import Bcrypt
from flask import flash
#2  Creacion de instancia de Bycript pasando app como paramatro
bcrypt = Bcrypt(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/usuarios/registro', methods = ['POST'])
def crear_usuario():
    data = {
        'nombre' : request.form['nombre'],
        'apellido' : request.form['apellido'],
        'email' : request.form['email'],
        'password': request.form['password'],
        'confirmar_password' : request.form['confirmar_password']
    }
    if not Usuario.validar(data):
        return redirect('/')
    data['password'] = bcrypt.generate_password_hash(data['password'])
    data = {
        'id' : Usuario.save(data)
    }
    info_usuario = Usuario.get_one(data)
    if info_usuario is None:
        return('/')
    session['id'] = info_usuario.id
    session['nombre'] = info_usuario.nombre
    session['apellido'] = info_usuario.apellido
    session['email'] = info_usuario.email

    return redirect('/dashboard')





@app.route('/destroy', methods = ['POST'])
def destroy():
    session.clear()
    return redirect('/')




@app.route('/usuarios/login', methods = ['POST'])
def login():
    data = {
        'email' : request.form['email'],
        'password': request.form['password'],
    }
    usuario = Usuario.get_one_by_email(data)
    print(usuario)
    if not bcrypt.check_password_hash(usuario.password, data['password']):
        flash("El correo o el password no coniciden con la info en Base de datos!","login")
        return redirect('/')
    session['id'] = usuario.id
    session['nombre'] = usuario.nombre
    session['apellido'] = usuario.apellido
    session['email'] = usuario.email
    return redirect('/dashboard')
