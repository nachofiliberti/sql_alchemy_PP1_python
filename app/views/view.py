# Imports que son nativos de Python
import os
from datetime import timedelta

# Imports que son nativos del Framework y Librerias
from app import app, db, jwt
from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# Imports de variables generadas por nosotros
from app.models.models import (
    Localidad,
    Pais,
    Persona,
    Provincia,
    User,
)
from app.schemas.schema import (
    UserAdminSchema,
    UserBasicSchema,
    PaisSchema,
    ProvinciaSchema,
    LocalidadSchema
)

@app.route("/users")
@jwt_required()
def get_all_users():
    additional_info = get_jwt() #obtengo info adiccional del token 

    page = request.args.get('page', 1, type=int)
    can = request.args.get('can', 1000, type=int)
    users = db.session.query(User).paginate(
        page=page, per_page=can
    )

    if additional_info["is_admin"]:
        return jsonify(
            {
                "results":UserAdminSchema().dump(
                    users.items, many=True
                ),
                "next":url_for(
                    'get_all_users', page=users.next_num
                ) if users.has_next else None,
                "prev":url_for(
                    'get_all_users', page=users.prev_num
                ) if users.has_prev else None
            }
        )
    return jsonify(
        {
            "results": UserBasicSchema().dump(users.items, many=True)
        }
    )

@app.route("/localidades")
def get_all_localidades():
    localidades = Localidad.query.all()
    localidades_schema = LocalidadSchema().dump(localidades, many=True)
    return jsonify(localidades_schema)




@app.route("/provincias")
def get_all_provincias():
    provincias = Provincia.query.all()
    provincias_schema = ProvinciaSchema().dump(provincias, many=True)
    return jsonify(provincias_schema)



@app.route("/paises")
def get_all_paises():
    paises = Pais.query.all()
    paises_schema = PaisSchema().dump(paises, many=True)
    return jsonify(paises_schema)


@app.context_processor
def inject_paises():
    countries = db.session.query(Pais).all()
    return dict(
        paises=countries   
    )

@app.context_processor
def inject_idiomas():
    return dict(
        lang=['US','ES', 'FR']   
    )

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/agregar_pais', methods=['POST'])
def nuevo_pais():
    if request.method=='POST':
        nombre_pais = request.form['nombre']

        # Inicializo el objeto
        nuevo_pais = Pais(nombre=nombre_pais)
        # Preparo el objeto para enviarlo a la base de datos
        db.session.add(nuevo_pais)
        # Envio el objeto
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/borrar_pais/<id>')
def borrar_pais(id):

    pais = Pais.query.get(id)
    db.session.delete(pais)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin')
    password_hash = generate_password_hash(
        password, method='pbkdf2', salt_length=8
        )
    
    nuevo_usuario = User(username=username, password_hash=password_hash,is_admin=is_admin)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "Se recibio la data":"OK",
        "username":username,
        "password_hash":password_hash
        }, 200)

@app.route('/login')
def login():
    data = request.authorization
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    #check_password_hash(contraseña guardada, contraseña recibida)
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=20),
            additional_claims=dict(
                is_admin=user.is_admin,
            )
        )
        return jsonify({"ok":access_token})
    return jsonify(Error="No pude generar el token"),400

@app.route("/ruta_restringida")
@jwt_required()
def ruta_restringida():
    current_user = get_jwt_identity()
    additional_info = get_jwt()
    if additional_info['user_type']==1:
        return jsonify(
            {
                "Mensaje":f"El usuario {current_user} tiene acceso a esta ruta",
                "Info Adicional": additional_info
            }
        )
    return jsonify(
            {
                "Mensaje":f"El usuario {current_user} no tiene acceso a esta ruta",
            }
        )

@jwt.invalid_token_loader
def unauthorized_user(reason):
    return jsonify(mensaje=f"Acceso denegado porque : {reason}"), 401
