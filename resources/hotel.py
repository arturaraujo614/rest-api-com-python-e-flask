from flask_restful import Resource,reqparse #reqparse necessario para receber elementos de requisicao
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} #SELECT *FROM HOTEIS

class Hotel(Resource):
    argumentos = reqparse.RequestParser() #reqparse permite receber elementos em json
    argumentos.add_argument('nome',type=str,required=True,help="The field 'nome'cannot be left in blank") #adicionar argumento identificado por nome
    argumentos.add_argument('estrelas',type=float,required=True,help="The field 'estrelas'cannot be left in blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json() #retorna o objeto, entao convertemos para json
        return {'message':'Hotel not found'},404
        
    @jwt_required() #Pra acessar a funcao, precisa passar primeiro o token de acesso
    def post(self,hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":"Hotel id '{}' already exists.".format(hotel_id)},400 #bad request
        dados = Hotel.argumentos.parse_args() #chave e valor dos dados recebidos, especie de dicionario. {'nome':Alfa} etc
        hotel = HotelModel(hotel_id,**dados) #é um objeto
        try:
            hotel.save_hotel()
        except:
            return {'message':'An internal erro ocurred trying to save hotel.'},500 #Internal Server Erro
        return hotel.json() #convertendo um obj em json

    @jwt_required()
    def put(self,hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id,**dados)
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados) #atualizar os dados com base no id encontrado
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(),200 #Ok
        hotel = HotelModel(hotel_id,**dados) #cria uma instancia do novo hotel, caso ele n seja encontrado
        try:
            hotel.save_hotel()
        except:
            return {'message':'An internal erro ocurred trying to save hotel.'},500 #Internal Server Erro
        return hotel.json(),201 #created

    @jwt_required()
    def delete(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {'message':'Hotel Deleted.'} 
            except:
                return {'message':'An internal erro ocurred trying to save hotel.'},500 #Internal Server Errohotel.delete_hotel()
            
        return {'message':'Hotel Not Found.'} ,404