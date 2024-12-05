from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import usuario
from flask import flash
from datetime import datetime



class Mensaje:
    db_schema = 'muro_privado' ## Cambiar la BD a la que estamos apuntando
    def __init__(self,data):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.contenido = data['contenido']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']

    def tiempo_en_formato(self):
        now = datetime.now()

        horas = now - (self.created_at)

        if horas.days > 1 and horas.days <= 30:
            horas = f"{horas.days} days ago"
        elif horas.days > 30 and horas.days < 365:
            horas = f"{int((horas.days/30))} months ago"
        elif horas.days > 365:
            horas = f"{int((horas.days/365))} years ago"
        else:
            horas = f"{int((horas.seconds/60)/60)} hours ago"
        return horas 
    
    @classmethod
    def guardar(cls,data):
        query = "insert into mensajes (sender_id,receiver_id,contenido) values (%(sender_id)s,%(receiver_id)s,%(contenido)s);"
        return connectToMySQL(cls.db_schema).query_db(query,data)
    
    @classmethod
    def eliminar(cls,data):
        query = "delete from mensajes where id=%(id)s;"
        return connectToMySQL(cls.db_schema).query_db(query,data)
    
    @classmethod
    def mensajes_recibidos(cls,data):
        query = "select * from mensajes left join usuarios on mensajes.sender_id=usuarios.id where mensajes.receiver_id=%(receiver_id)s order by mensajes.created_at desc;"
        resultados = connectToMySQL(cls.db_schema).query_db(query,data)
        mensajes = []
        for mensaje in resultados:
            sender_data = {
                "id" : mensaje["usuarios.id"],
                "nombre" : mensaje["nombre"],
                "apellido" : mensaje["apellido"],
                "password" : mensaje["password"],
                "email" : mensaje["email"],
                "created_at" : mensaje["usuarios.created_at"],
                "updated_at" : mensaje["usuarios.updated_at"]
            }
            sender = usuario.Usuario(sender_data)
            data_mensaje = {
                "id" : mensaje["id"],
                "contenido" : mensaje['contenido'],
                "sender_id" : sender,
                "receiver_id" : mensaje['receiver_id'],
                "created_at" : mensaje["created_at"],
                "updated_at" : mensaje["updated_at"]
            }

            mensajes.append(cls(data_mensaje))
        return mensajes
    
    @classmethod
    def mensajes_enviados(cls,data):
        query = "select count(*) as 'contador' from mensajes where sender_id=%(sender_id)s;"
        resultados = connectToMySQL(cls.db_schema).query_db(query,data)
        return resultados[0]
    
    @staticmethod
    def validar(data):
        is_valid = True
        if len(data['contenido']) < 3:
            flash("El mensaje debe tener al menos 3 letras!","mensajes")
            is_valid = False
        return is_valid