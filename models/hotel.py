from sql_alchemy import banco

class HotelModel(banco.Model): #No momento que está banco.Model = do tipo banco e as tabelas sao de banco de dados
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self,hotel_id,nome,estrelas,diaria,cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
    def json(self):
        return {
            'hotel_Id':self.hotel_id,
            'nome':self.nome,
            'estrelas':self.estrelas,
            'diaria' :self.diaria,
            'cidade':self.cidade
        }
    @classmethod #Metodo de classe, nao acessa nada que seja self, recebe apenas o hotel_id
    def find_hotel(cls, hotel_id): 
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() #SELECT *FROM hoteis WHERE hotel_id = hotel_id #cls é abreviacao da classe, no caso,HotelModel
        if hotel:
            return hotel
        return None

    def update_hotel(self,nome,estrelas,diaria,cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade    

    def save_hotel(self):
        banco.session.add(self) #Cria coneção com banco e salva a variavel(objeto) self no banco
        banco.session.commit()

    def delete_hotel(self):
        banco.session.delete(self) #Cria coneção com banco e deleta a variavel(objeto) self no banco
        banco.session.commit()