from flask_app.config.mysqlconnection import connectToMySQL ###Nos podemos conectar a la BD y podemos jugar con la creacion del objeto y sus metodos

#####aqui debes importar otras clases en caso de que sea necesario
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.{8,})(?=.*[a-z])(?=.*[0-9])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$')


class Usuario:
    db_schema = 'muro_privado' ## Cambiar la BD a la que estamos apuntando
    def __init__(self,data):
        self.id = data['id'] 
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']


    @classmethod
    def get_all(cls):
        query = "select * from usuarios;" ###cambiar la tabla a la que apuntamos.
        resultados = connectToMySQL(cls.db_schema).query_db(query)
        usuarios = [] ###Cambiar el nombre del arreglo para algo que represente la tabla
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios
    
    @classmethod
    def save(cls,data):
        query = "insert into usuarios (nombre,apellido,email,password) values (%(nombre)s, %(apellido)s, %(email)s,%(password)s);"
        return connectToMySQL(cls.db_schema).query_db(query,data)

    @classmethod
    def get_one(cls,data):
        query = "select * from usuarios where id=%(id)s;"
        resultado = connectToMySQL(cls.db_schema).query_db(query,data)
        if len(resultado)> 0:
            return cls(resultado[0])
        else:
            return None
        
    @classmethod
    def get_one_by_email(cls,data):
        query = "select * from usuarios where email=%(email)s;"
        resultado = connectToMySQL(cls.db_schema).query_db(query,data)
        if len(resultado)> 0:
            return cls(resultado[0])
        else:
            return None


    @staticmethod
    def validar(data):
        is_valid = True
        query = "select * from usuarios where email=%(email)s;"
        resultado_query = connectToMySQL(Usuario.db_schema).query_db(query,data)
        if len(resultado_query) > 0:
            flash("El email ya esta registrado!","registro")
            is_valid = False
        if len(data['nombre']) <5 :
            flash("El  nombre debe tener mas de 5 letras","registro")
            is_valid = False
        if not NAME_REGEX.match(data['nombre']):
            flash("El nombre no puede tener numeros o caracteres especiales","registro")
            is_valid = False
        if len(data['apellido']) <5 :
            flash("El apellido debe tener mas de 5 letras","registro")
            is_valid = False
        if not NAME_REGEX.match(data['apellido']):
            flash("El apellido no puede tener numeros o caracters especiales","registro")
        if not EMAIL_REGEX.match(data['email']):
            flash("El email no cumple con las caracteristicas minimas solicitadas","registro")
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash("El password no cumple con las caracterisitas minimas","registro")
            is_valid = False
        if data['password'] != data['confirmar_password']:
            flash("Los passwords no coniciden","registro")
            is_valid = False
        return is_valid
    
