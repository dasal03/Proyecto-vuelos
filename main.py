from flask import Flask, render_template, session, flash, request
import sqlite3
import os

from werkzeug.utils import escape, redirect
from forms.formularios import Comentarios, Login, NewRegistro, Registro, Vuelos, User
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    frm = Login()
    if frm.validate_on_submit():
        username = escape(frm.username.data)
        password = escape(frm.password.data)
        # Cifra la contraseña
        enc = hashlib.sha256(password.encode())
        pass_enc = enc.hexdigest()

        #Conectar a la BD
        with sqlite3.connect("vuelos.db") as con:
            # Crea cursos para manipular la BD
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            #Prepara la sentencia SQL a ejecutar
            cursor.execute("SELECT username, perfil, id, nombre FROM usuario WHERE username = ? AND password = ?", [username, pass_enc])
            # sql = f"SELECT username FROM usuario WHERE username = '{username}' AND password = '{pass_enc}'"
            #cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                session["usuario"] = username
                session["iden"] = row["id"]
                session["nombre"] = row["nombre"]
                session["perfil"] = row["perfil"]

                if session["perfil"] == 1:
                    return redirect("/lista_vuelos")
                elif session['perfil'] == 2:
                    return redirect("/usuario/dashboard")
                elif session["perfil"] == 3:
                    return redirect("/administrador/dashboard")
            else:
                flash("Usuario/Password errados")

    return render_template("login.html", frm = frm)

#API Rest de registro de Usuarios
@app.route("/registrarse", methods=["GET", "POST"]) #Ruta
def registrar(): #Endpoint
    if "usuario" in session and session["perfil"] == 3:
        frm = Registro()
        # Valida los datos del formulario
        if frm.validate_on_submit():
            #Captura los datos del formulario
            username = frm.username.data
            nombre = frm.nombre.data
            correo = frm.correo.data
            password = frm.password.data
            perfil = frm.perfil.data
            # Cifra la contraseña
            enc = hashlib.sha256(password.encode())
            pass_enc = enc.hexdigest()

            #Conectar a la BD
            with sqlite3.connect("vuelos.db") as con:
                # Crea cursos para manipular la BD
                cursor = con.cursor()
                #Prepara la sentencia SQL a ejecutar
                cursor.execute("INSERT INTO usuario (nombre, username, correo, password, perfil) VALUES (?,?,?,?,?)", [nombre, username, correo, pass_enc, perfil])
                #Ejecuta la sentencia SQL
                con.commit()
                flash("Registro guardado con éxito")

        return render_template("registro.html", frm= frm) #Respuesta
    else:
        return "Acesso no permitido"

@app.route("/administrador/dashboard")
def admin_dashboard():
    if ("usuario" in session and session["perfil"]==3):
        frm = Vuelos()
        return render_template("admin_vuelos.html", frm=frm)
    else:
        return redirect("/")

@app.route("/usuario/dashboard")
def user_dashboard():
    if ("usuario" in session and session["perfil"]==2):
        frm2 = User()
        return render_template("user.html", frm2=frm2)
    else:
        return redirect("/")

@app.route("/vuelos/save",methods=["POST"])
def vuelos_save():
    if "usuario" in session:
        frm = Vuelos()
        codigo = frm.codigo.data
        avion = frm.avion.data
        piloto = frm.piloto.data
        capacidad = frm.capacidad.data
        estado = frm.estado.data
        origen = frm.origen.data
        destino = frm.destino.data
        id_piloto_fk = frm.id_piloto_fk.data
        with sqlite3.connect("vuelos.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Vuelos (codigo, avion, piloto, capacidad, estado, origen, destino, id_piloto_fk) VALUES (?,?,?,?,?,?,?,?)",[codigo, avion, piloto, capacidad, estado, origen, destino, id_piloto_fk])
            con.commit()
            flash("Guardado con éxito")
    else:
        return redirect("/")

    return render_template("admin_vuelos.html",frm= frm)

@app.route("/vuelos/get", methods=["POST"])
def vuelos_get():
    if "usuario" in session:
        frm = Vuelos()
        codigo = frm.codigo.data
        if len(codigo)>0:
            with sqlite3.connect("vuelos.db") as con:
                # Convierte la respuesta de la consulta a diccionario
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM Vuelos WHERE codigo = ?",[codigo])
                row = cur.fetchone()
                if row:
                    frm.avion.data = row["avion"]
                    frm.piloto.data = row["piloto"]
                    frm.capacidad.data = row["capacidad"]
                    frm.estado.data = row["estado"]
                    frm.origen.data = row["origen"]
                    frm.destino.data = row["destino"]
                    frm.id_piloto_fk.data = row["id_piloto_fk"]
                else:
                    frm.codigo.data = ""
                    frm.avion.data = ""
                    frm.piloto.data = ""
                    frm.capacidad.data = ""
                    frm.estado.data = ""
                    frm.origen.data = ""
                    frm.destino.data = ""
                    frm.id_piloto_fk.data = ""
                    flash("Vuelo no encontrado")
        else:
            flash("Debe digitar el Código del vuelo")

        return render_template("admin_vuelos.html",frm= frm)
    else:
        return redirect("/")

@app.route("/vuelos/update", methods=["POST"])
def vuelos_update():
    if "usuario" in session:
        frm = Vuelos()
        codigo = frm.codigo.data
        avion = frm.avion.data
        piloto = frm.piloto.data
        capacidad = frm.capacidad.data
        estado = frm.estado.data
        origen = frm.origen.data
        destino = frm.destino.data
        id_piloto_fk = frm.id_piloto_fk.data

        if len(codigo):
            if codigo.isnumeric():
                if len(avion):
                    if len(piloto):
                        if len(capacidad):
                            if len(estado):
                                if len(origen):
                                    if len(destino):
                                        if len(id_piloto_fk):
                                            with sqlite3.connect("vuelos.db") as con:
                                                cur = con.cursor()
                                                cur.execute("UPDATE Vuelos SET avion=?, piloto=?, capacidad=?, estado=?, origen=?, destino=?, id_piloto_fk=? WHERE codigo=?",[avion,piloto,capacidad,estado,origen,destino,id_piloto_fk,codigo])
                                                con.commit()
                                                if con.total_changes > 0:
                                                    flash("Vuelo actualizado")
                                                else:
                                                    flash("No se pudo actualizar el vuelo")
                                        else:
                                            flash("Debe digitar el codigo del piloto")
                                    else:
                                        flash("Debe digitar el destino del vuelo")
                                else:
                                    flash("Debe digitar el origen del vuelo")
                            else:
                                flash("Debe digitar el codigo")
                        else:
                            flash("Debe digitar el avion")
                    else:
                        flash("Debe digitar el piloto")
                else:
                    flash("Código debe ser númerico")
            else:
                flash("Debe digitar la capacidad")
        else:
            flash("Debe digitar el estado")

        return render_template("admin_vuelos.html", frm=frm)
    else:
        return redirect("/")

@app.route("/vuelos/delete",methods=["POST"])
def vuelos_delete():
    if "usuario" in session:
        frm = Vuelos()
        codigo = frm.codigo.data
        if len(codigo)>0:
            with sqlite3.connect("vuelos.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM Vuelos WHERE codigo = ?",[codigo])
                con.commit()

                flash("Vuelo Eliminado!")
        else:
            flash("Debe digitar el Código del vuelo")

        return render_template("admin_vuelos.html",frm= frm)
    else:
        return redirect("/")

@app.route("/ver-registros")
def view():
    con = sqlite3.connect("vuelos.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from usuario")
    rows = cur.fetchall()
    return render_template("view.html",rows = rows)

@app.route("/ver-vuelos", methods=["GET"])
def view_vuelos():
    con = sqlite3.connect("vuelos.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from vuelos")
    rows = cur.fetchall()
    return render_template("vuelos-listado.html",rows=rows)

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("vuelos.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from usuario where id = ?",id)
            msg = "Registro correctamente eliminado"
        except:
            msg = "No se puede eliminar"
        finally:
            return render_template("deleterecord.html",msg = msg)

@app.route("/piloto/dashboard", methods=["GET"])
def piloto_dashboard():
    if ("usuario" in session and session["perfil"]==1):
        frm = Vuelos()
        return render_template("vuelos-listado.html", frm=frm)
    else:
        return redirect("/")

@app.route("/lista_vuelos", methods=["GET"])
def vuelos_list():
    if "usuario" in session and session["perfil"] == 1:
        iden = session["iden"]
        with sqlite3.connect("vuelos.db") as con:
            # Convierte la respuesta de la consulta a diccionario
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #cur.execute("SELECT * FROM vuelos")
            cur.execute("SELECT codigo, avion, piloto,capacidad, origen, destino, estado, id_piloto_fk from vuelos WHERE id_piloto_fk =?", [iden])
            rows = cur.fetchall()

        return render_template("vuelos-listado.html",rows=rows)
    else:
        return redirect("/")

@app.route("/usuario/dashboard", methods=["POST","GET"])
def buscar_vuelo():
    if "usuario" in session:
        frm2 = User()
        codigo = frm2.codigo.data
        if len(codigo)>0:
            with sqlite3.connect("vuelos.db") as con:
                # Convierte la respuesta de la consulta a diccionario
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                #cur.execute("SELECT avion, piloto, capacidad, estado, origen, destino, id_piloto_fk FROM Vuelos WHERE codigo = ?",[codigo])
                cur.execute("SELECT avion, piloto, capacidad, estado, origen, destino, id_piloto_fk, nombre FROM Vuelos V INNER JOIN usuario u WHERE codigo = ?",[codigo])
                con.commit()
                row = cur.fetchone()
                if row:
                    frm2.avion.data = row["avion"]
                    frm2.piloto.data = row["piloto"]
                    frm2.capacidad.data = row["capacidad"]
                    frm2.estado.data = row["estado"]
                    frm2.origen.data = row["origen"]
                    frm2.destino.data = row["destino"]
                    frm2.id_piloto_fk.data = row["id_piloto_fk"]

                    frm2.nombre.data = row["nombre"]
                else:
                    frm2.codigo.data = ""
                    frm2.avion.data = ""
                    frm2.piloto.data = ""
                    frm2.capacidad.data = ""
                    frm2.estado.data = ""
                    frm2.origen.data = ""
                    frm2.destino.data = ""
                    frm2.id_piloto_fk.data = ""

                    frm2.nombre.data=""
                    flash("Vuelo no encontrado")
        else:
            flash("Debe digitar el Código del vuelo")
        return render_template("user.html", frm2=frm2)
    else:
        return redirect("/")
    # return redirect("/usuario/dashboard")

@app.route("/usuario/reserva", methods=["POST", "GET"])
def vuelos_reserva():
    if "usuario" in session:
        frm2 = User()
        codigo = frm2.codigo.data
        avion = frm2.avion.data
        piloto = frm2.piloto.data
        capacidad = frm2.capacidad.data
        estado = frm2.capacidad.data
        origen = frm2.origen.data
        destino = frm2.destino.data
        id_piloto_fk = frm2.id_piloto_fk.data

        if len(codigo):
            if codigo.isnumeric():
                if len(avion):
                    if len(piloto):
                        if len(capacidad):
                            if len(estado):
                                if len(origen):
                                    if len(destino):
                                        if len(id_piloto_fk):
                                            with sqlite3.connect("vuelos.db") as con:
                                                cur = con.cursor()
                                                cur.execute("UPDATE Vuelos SET capacidad=capacidad-1 where codigo = ?",[codigo])
                                                con.commit()
                                                flash("Vuelo reservado")
                                        else:
                                            flash("Debe digitar el codigo del piloto")
                                    else:
                                        flash("Debe digitar el destino del vuelo")
                                else:
                                    flash("Debe digitar el origen del vuelo")
                            else:
                                flash("Debe digitar el codigo")
                        else:
                            flash("Debe digitar el avion")
                    else:
                        flash("Debe digitar el piloto")
                else:
                    flash("Código debe ser númerico")
            else:
                flash("Debe digitar la capacidad")
        else:
            flash("Debe digitar el estado")

        return render_template("user.html", frm2=frm2)
    else:
        return redirect("/")

@app.route("/usuario-nuevo", methods=["GET", "POST"])
def new_user():
        frm = NewRegistro()

        # Valida los datos del formulario
        if frm.validate_on_submit():
            #Captura los datos del formulario
            username = frm.username.data
            nombre = frm.nombre.data
            correo = frm.correo.data
            password = frm.password.data
            perfil = frm.perfil.data


            # Cifra la contraseña
            enc = hashlib.sha256(password.encode())
            pass_enc = enc.hexdigest()

            #Conectar a la BD
            with sqlite3.connect("vuelos.db") as con:
                # Crea cursos para manipular la BD
                cursor = con.cursor()
                #Prepara la sentencia SQL a ejecutar
                cursor.execute("INSERT INTO usuario (nombre, username, correo, password, perfil) VALUES (?,?,?,?,?)", [nombre, username, correo, pass_enc, perfil])
                #Ejecuta la sentencia SQL
                con.commit()
                flash("Registro guardado con éxito")

        return render_template("new_user.html", frm= frm) #Respuesta

@app.route("/comentarios", methods=["POST","GET"])
def comentario():
    frm = Comentarios()
    if frm.validate_on_submit():
        id_usuario = frm.id_usuario.data
        cod_vuelo = frm.cod_vuelo.data
        comentario = frm.comentario.data

        with sqlite3.connect("vuelos.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO comentarios (id_usuario,cod_vuelo,comentario) VALUES (?,?,?)",[id_usuario,cod_vuelo,comentario])
            con.commit()
            flash("Enviado con éxito")
    return render_template("comentarios.html", frm=frm)

@app.route("/ver-comentarios", methods=["GET"])
def ver_com():
    if "usuario" in session and session["perfil"]== 1:
        iden = session["iden"]
        with sqlite3.connect("vuelos.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT c.cod_vuelo, c.id_usuario, c.comentario FROM comentarios c INNER JOIN vuelos v WHERE c.cod_vuelo = v.codigo AND v.id_piloto_fk = ?",[iden])
            rows = cur.fetchall()
            return render_template("ver-comentarios.html",rows = rows)

@app.route("/ver-comentarios-vuelos", methods=["GET"])
def ver_com_vuelos():
    if "usuario" in session and session["perfil"]== 3:
        with sqlite3.connect("vuelos.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT cod_vuelo, id_usuario, comentario FROM comentarios")
            rows = cur.fetchall()
            return render_template("ver-comentarios-vuelos.html",rows = rows)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

app.run(debug=True)