from flask_restful import Resource,reqparse #reqparse necessario para receber elementos de requisicao
from models.usuario import UserModel
from flask_jwt_extended import create_access_token,jwt_required,get_jwt
from blacklist import BLACKLIST
import hmac

#Variavel Global, qualquer tem acesso a esse atributos
atributos = reqparse.RequestParser()
atributos.add_argument('login',type=str,required=True,help="The field 'login' cannot be blank")
atributos.add_argument('senha',type=str,required=True,help="The field 'senha' cannot be blank")

class User(Resource):
   #/usuarios/{user_id}
    def get(self,user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json() #retorna o objeto, entao convertemos para json
        return {'message':'User not found'},404

    @jwt_required()  
    def delete(self,user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
                return {'message':'User Deleted.'} 
            except:
                return {'message':'An internal erro ocurred trying to save user.'},500 #Internal Server Errohotel.delete_hotel()
            
        return {'message':'User Not Found.'} ,404

class UserRegister(Resource):
    #/cadastro

    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"messagem":f"The login  {dados['login']}"}
        
        user = UserModel(**dados) #Formar de escrever dados['login'],dados['senha']
        user.save_user()
        return {'message':'User created successfully!'},201 #Created

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and hmac.compare_digest(user.senha,dados['senha']): #forma segura de comrar 2 str
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'acess_token':token_de_acesso},200
        return {'message':'The username or password is incorrect'},401 #Unauthorize

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Identificator
        BLACKLIST.add(jwt_id)
        return {'message':'Logged out successfully'},200