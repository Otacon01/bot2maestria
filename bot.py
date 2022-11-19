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


@bot.message_handler(commands=['imc'])
def on_command_imc(message):
    response = bot.reply_to(message, "¿Cuál es tu estatura en metros?")
    bot.register_next_step_handler(response, process_height_step)


def process_height_step(message):
    try:
        height = float(message.text)
        record = Record()
        record.height = height
        bot_data[message.chat.id] = record
        response = bot.reply_to(message, '¿Cuál es tu peso en kilogramos?')
        bot.register_next_step_handler(response, process_weight_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def process_weight_step(message):
    try:
        weight = float(message.text)
        record = bot_data[message.chat.id]
        record.weight = weight
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        response = bot.reply_to(message, '¿Cuál es tu género?',
        reply_markup=markup)
        bot.register_next_step_handler(response, process_gender_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def process_gender_step(message):
    gender = message.text
    record = bot_data[message.chat.id]
    record.gender = gender
    imc(message)


def imc(message):
    clasificacion = ""
    record = bot_data[message.chat.id]
    imc = record.weight / pow(record.height, 2)
    if imc < 18.50:
        clasificacion="Peso Bajo"
    elif imc >=18.50 and imc < 24.99:
        clasificacion="Peso Normal"
    elif imc >=25 and imc < 30:
        clasificacion="Sobrepeso"
    elif imc >=30 :
        clasificacion="Obesidad"

    answer = f"Data = (Height: {record.height}, Weight: {record.weight}, Gender: {record.gender}, Clasificacion:{clasificacion})\nIMC = {imc}"
    bot.reply_to(message, answer)

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