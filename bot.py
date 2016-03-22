from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import telebot, random

DEBUG = True

engine = create_engine("sqlite:///users.db")
Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer,nullable=False,primary_key=True)
    total = Column(Integer,default=0,nullable=False)
    last_generate = Column(DateTime,nullable=False)

Base.metadata.create_all(engine)

with open("token.txt") as f:
    token = f.read()
    bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def startMessage(message):
    bot.send_message(message.chat.id,"Soy el bot de laboratorio de prototipos")

@bot.message_handler(commands=['cachama'])
def cachama(message):
    if (message.chat.type == 'private' or message.chat.type == 'channel') and DEBUG == False:
        return
    total_cachamas = get_users_cachamas(message.from_user.id)
    if can_get_cachama(message.user.id):
        new_cachamas = generate_new_cachamas()
        total_cachamas=total_cachamas+new_cachamas
        response = random.choice(cachama_templates_new).format(name=message.from_user.first_name,new=new_cachamas,total=total_cachamas)
    else:
        response = random.choice(cachama_templates).format(name=message.from_user.first_name,total=total_cachamas)
    bot.send_message(message.chat.id,response)

def can_get_cachama(id):
    pass

def generate_new_cachamas():
    return (10*random.randint(0,9))+random.randint(0,9)

if __name__ == "__main__":
    bot.polling()


