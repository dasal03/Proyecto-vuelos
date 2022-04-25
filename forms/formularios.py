from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired("Usuario es obligatorio")])
    password = PasswordField("Password", validators=[DataRequired("Password es obligatorio")])
    enviar = SubmitField ("Enviar")

class Registro(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired("Usuario es obligatorio")])
    nombre = StringField("Nombre", validators=[DataRequired("Nombre es obligatorio")])
    correo = StringField("Correo", validators=[DataRequired("Correo es obligatorio")])
    password = PasswordField("Password", validators=[DataRequired("Password es obligatorio")])
    perfil = SelectField("Perfil", coerce=int, choices=[("0","-- Elija opción -- "),("1","piloto"),("2","usuario"),("3","administrador")], validators=[DataRequired(message="Debe escoger una opción")])
    registrar = SubmitField("Registrar")
    check = BooleanField('Acepto términos y condiciones', validators=[DataRequired(message="Debe aceptar los terminos")])

class NewRegistro(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired("Usuario es obligatorio")])
    nombre = StringField("Nombre", validators=[DataRequired("Nombre es obligatorio")])
    correo = StringField("Correo", validators=[DataRequired("Correo es obligatorio")])
    password = PasswordField("Password", validators=[DataRequired("Password es obligatorio")])
    perfil = SelectField("Perfil", coerce=int, choices=[("0","-- Elija opción -- "),("2","usuario")], validators=[DataRequired(message="Debe escoger una opción")])
    registrar = SubmitField("Registrar")

class Vuelos(FlaskForm):
    codigo = StringField("Codigo", validators=[DataRequired("Codigo es obligatorio")])
    avion = StringField("Avion")
    piloto = StringField("Piloto")
    capacidad = StringField("Capacidad")
    estado = StringField("Estado")
    origen = StringField("Origen")
    destino = StringField("Destino")
    id_piloto_fk = StringField("ID Piloto Asignado")
    guardar = SubmitField("Guardar", render_kw=({"onfocus":"cambiarRuta('/vuelos/save')"}))
    consultar = SubmitField("Consultar", render_kw=({"onfocus":"cambiarRuta('/vuelos/get')"}))
    editar = SubmitField("Editar", render_kw=({"onfocus":"cambiarRuta('/vuelos/update')"}))
    eliminar = SubmitField("Eliminar", render_kw=({"onfocus":"cambiarRuta('/vuelos/delete')"}))

class User(FlaskForm):
    codigo = StringField("Codigo", validators=[DataRequired("Codigo es obligatorio")])
    avion = StringField("Avion")
    piloto = StringField("Piloto")
    capacidad = StringField("Capacidad")
    estado = StringField("Estado")
    origen = StringField("Origen")
    destino = StringField("Destino")
    id_piloto_fk = StringField("ID del Piloto")
    nombre = StringField("Nombre del Piloto")
    consultar = SubmitField("Consultar",render_kw=({"onfocus":"cambiarRuta2('/usuario/dashboard')"}))
    reservar = SubmitField("Reservar",render_kw=({"onfocus":"cambiarRuta2('/usuario/reserva')"}))

class Comentarios(FlaskForm):
    id_usuario = StringField("ID Usuario", validators=[DataRequired("ID del usuario es obligatorio")])
    cod_vuelo = StringField("Codigo vuelo", validators=[DataRequired("Codigo del vuelo es obligatorio")])
    comentario = TextAreaField("Comentario", validators=[DataRequired("Comentario es obligatorio")])
    enviar = SubmitField("Enviar")