#########################################################

from config import bot
import config
from time import sleep
from telebot import types

bot_data = {}
class Record:
    def __init__(self):
        self.height = None
        self.weight = None
        self.gender = None


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

#########################################################
@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    m = bot.send_message(
        message.chat.id,
        "\U0001F916 Bienvenido al bot del Índice de Masa Corporal",
        parse_mode="Markdown")
            
@bot.message_handler(commands=['menu'])
def on_command_menu(message):

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/imc')
    itembtn2 = types.KeyboardButton('/help')

    markup.add(itembtn1, itembtn2)
    
    bot.send_message(message.chat.id, "Selecciona una opción del menú:",reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.reply_to(
        message,
        "\U0001F63F Ups, no entendí lo que me dijiste.")        
#########################################################

if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################