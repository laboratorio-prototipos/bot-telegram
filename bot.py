from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
import telebot, random

DEBUG = True

engine = create_engine("sqlite:///users.db")
metadata = MetaData()
users = Table(users,metadata,
        Column('user_id',Integer,primary_key=True),
        Column('total_cachamas',Integer,default=0),
        Column('last_request',DateTime))

with open("token.txt") as f:
    token = f.read()
    bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start']):
    def startMessage(message):
        bot.send_message(message.chat,"Soy el bot de laboratorio de prototipos")

@bot.message_handler(commands=['cachama']):
    def cachama(message):
        if (message.chat.type == 'private' or message.chat.type == 'channel') and DEBUG == False:
            return
        total_cachamas = get_users_cachamas(message.from.id)
        if can_get_cachama(message.user.id):
            new_cachamas = generate_new_cachamas()
            total_cachamas=total_cachamas+new_cachamas
            response = random.choice(cachama_templates_new).format(name=message.from.first_name,new=new_cachamas,total=total_cachamas)
        else:
            response = random.choice(cachama_templates).format(name=message.from.first_name,total=total_cachamas)
        bot.send_message(message.chat,response)

def generate_new_cachamas():
    return (10*random.randint(0,9))+random.randint(0,9)

if __name__ == "__main__":
    bot.polling()


