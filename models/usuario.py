from sql_alchemy import banco

class UserModel(banco.Model): #No momento que está banco.Model = do tipo banco e as tabelas sao de banco de dados
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))


    def __init__(self,login,senha): #por user_id ser integer e primay key, o banco vai entender que é um id e criar
        self.login = login
        self.senha= senha
    def json(self):
        return {
            'user_id':self.user_id,
            'login':self.login
        }
    @classmethod #Metodo de classe, nao acessa nada que seja self, recebe apenas o user_id
    def find_user(cls, user_id): 
        user = cls.query.filter_by(user_id=user_id).first() #SELECT *FROM hoteis WHERE hotel_id = hotel_id #cls é abreviacao da classe, no caso,HotelModel
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login): 
        user = cls.query.filter_by(login=login).first() #SELECT *FROM hoteis WHERE hotel_id = hotel_id #cls é abreviacao da classe, no caso,HotelModel
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self) #Cria coneção com banco e salva a variavel(objeto) self no banco
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self) #Cria coneção com banco e deleta a variavel(objeto) self no banco
        banco.session.commit()