from flask import Flask,jsonify
from flask_restful import Api
from resources.hotel import Hoteis,Hotel
from resources.usuario import User,UserRegister,UserLogin,UserLogout
from flask_jwt_extended import JWTManager #Gerencia a parte de autenticação
from blacklist import BLACKLIST

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' # vai criar na raiz, um banco do tipo sqlite. Para mudar o banco, basta mudar o nome sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Se nao botar, aparece um aviso pedindo se é false ou true que sobrecarrega o sistema
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request #verificar se existe o banco antes da primeira request no postman.
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self,token):
    return token['jti'] in BLACKLIST
    
@jwt.revoked_token_loader
def access_token_invalidation(jwt_header, jwt_payload):
    return jsonify(msg=f"You have been logged out!"), 401

api.add_resource(Hoteis, '/hoteis') #Hoteis é a classe que será chamado a partir do comando /hoteis
api.add_resource(Hotel,'/hoteis/<string:hotel_id>') #Class Hotel tem todo o CRUD, notel_id como parametro de entrada
api.add_resource(User,'/usuarios/<int:user_id>')
api.add_resource(UserRegister,'/cadastro')
api.add_resource(UserLogin,'/login')
api.add_resource(UserLogout,'/logout')


if __name__ == '__main__':
    from sql_alchemy import banco #So sera importado a partir do arquivo principal, app.py. Pois ele será necessário \
    #no arquivo Hotel.py. Ai pra nao ficar loop, ele só sera chamado a partir do main.
    banco.init_app(app) #ao iniciar o app, ele aciona onde o import banco é chamado
    app.run(debug=True)