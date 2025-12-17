from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, current_user,  login_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
   
    if username and password:
        user = User.query.filter_by(username=username).first()  
        if user and user.password == password:
            login_user(user)
            return jsonify({'message': 'Auenticação realizada com Sucesso'}), 200
        else:
            return jsonify({'message': 'Auenticação falhou'}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message: Logout realixado com sucesso!"})       

@app.route('/user', methods=["POST"])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if username and email and password:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario com registado com sucesso"}), 200

    return jsonify({"message": "erro"}), 400

@app.route('/users/<int:id_user>', methods=['GET'])
@login_required
def read_users(id_user):
    user = User.query.get(id_user)
    if user:
        return {'username': user.username,}
    return jsonify({"message": "usuário não encontrado"}), 404   

@app.route('/users/<int:id_user>', methods=['PUT'])
@login_required
def update_users(id_user):
    data = request.json
    user = User.query.get(id_user)

    if user and data.get("password"):
        user.password = data.get("password")
        db.commit()
        return jsonify({"message": f"Usuário {id_user} actualizado com sucesso"})
    return jsonify({"message": "usuário não encontrado"}), 404  

@app.route('/users/<int:id_user>', methods=['DELETE'])
@login_required
def delete_users(id_user):
    user = User.query.get(id_user)

    if id_user != current_user.id:
        return jsonify({"message": "Não permite apagar"}), 403  

    if user:
        db.session.delete(user)
        db.session.commit
        return jsonify({"message": f"Usuário {id_user} actualizado com sucesso "})
    return jsonify({"message": "usuário não encontrado"}), 404  


@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)