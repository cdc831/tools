from flask import Flask, redirect, url_for, render_template, request, flash, session
from flaskext.mysql import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key = "CanteroSoft"

# --------------------------------------------------------------------------------------
# -----------------------                 MYSQL          -------------------------------
# --------------------------------------------------------------------------------------
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = '181.116.17.78'
app.config['MYSQL_DATABASE_PORT'] = 3308
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345'
app.config['MYSQL_DATABASE_DB'] = 'canterosoft'
mysql.init_app(app)


class Database:
    def __init__(self):

        # Conectamos con la base de datos
        self.con = mysql.connect()

        # Creamos el cursor
        self.cur = self.con.cursor()
    
    def login(self,usuarioLogin,passLogin):
        sQuery = "SELECT * FROM tblusuariosistema WHERE usuario = %s AND clave = %s"
        self.cur.execute(sQuery,(usuarioLogin, passLogin))
        result = self.cur.fetchone()
        return result

    def getUsuarios(self):
        sQuery = "SELECT * FROM tblusuariosistema"
        self.cur.execute(sQuery)
        result = self.cur.fetchall()
        return result


# Para el Encriptamiento
semilla = bcrypt.gensalt()













# --------------------------------------------------------------------------------------
# -----------------------                 RUTAS          -------------------------------
# --------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')









# --------------------------------------------------------------------------------------
# -----------------------          RUTAS / ADMIN         -------------------------------
# --------------------------------------------------------------------------------------

@app.route('/_admin')
def home():
    if 'nombre' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template('_admin/login.html')


@app.route('/_admin/inicio')
def inicio():
    if 'nombre' in session:

        db = Database()
        registros = db.login(session['nombre'] ,session['pass'])

        if (registros is None ):
            print("Usuario no encontrado")
            return render_template('_admin/login.html')
        else:
            session['nombre']   = registros[1]
            session['pass']     = registros[2]
            session['nivel']    = registros[3]
            session['estado']   = registros[4]
            return render_template('_admin/index.html', data = registros)
            
    else:
        return render_template('_admin/login.html')


@app.route('/_admin/ingresar', methods=["GET","POST"])
def ingresar():
    if (request.method == "GET"):
        if 'nombre' in session:
            return redirect(url_for(inicio))
        else:
            return render_template('_admin/login.html')
    else:
        # Obtengo los datos
        usuarioLogin = request.form['usuario']
        passLogin = request.form['pass']

        db = Database()
        registros = db.login(usuarioLogin,passLogin)

        if (registros is None ):
            print("Usuario no encontrado")
            return render_template('_admin/login.html')
        else:
            session['nombre']   = registros[1]
            session['pass']     = registros[2]
            session['nivel']    = registros[3]
            session['estado']   = registros[4]
            return render_template('_admin/index.html', data = registros)
            

@app.route('/_admin/convertir', methods=["GET","POST"])
def getConvert():
    if (request.method == "GET"):
        if 'nombre' in session:
            return render_template('_admin/convert.html')
        else:
            return render_template('_admin/login.html')
    else:
        varCaracter = request.form['varCaracter']
        varCadena = request.form['varCadena']

        listaOrdenada = sorted(list(varCadena.split(varCaracter)))
        
        return render_template('_admin/convert.html', res = listaOrdenada)


@app.route('/_admin/usuarios', methods=["GET","POST"])
def listUsuarios():
    if (request.method == "GET"):
        if 'nombre' in session:
            db = Database()
            res = db.getUsuarios()
            return render_template('_admin/usuarios.html', res = res)
        else:
            return render_template('_admin/login.html')        


@app.route('/_admin/salir')
def salir():
    session.pop('nombre', None) 
    return redirect(url_for('ingresar'))


if __name__ == '__main__':
	app.run(debug=True)