import pandas as pd 
import telebot 
from telebot import types 
 
# Tu token del bot de Telegram 
TOKEN = '7455775782:AAGAnwCVb1yitZY-dXUMflFQPeOSY4WEyyc' 
bot = telebot.TeleBot(TOKEN) 
 
'''Funció per enviar un missatge de benvinguda amb el nom de l'usuari''' 
@bot.message_handler(commands=['start']) 
def start(message): 
    user_name = message.from_user.first_name  # Obtén el primer nom de l'usuari 
    bot.reply_to(message, f"Benvingut a TrivialverseQuiz, {user_name}! Tria una categoria per començar.") 
 
'''Funció per mostrar les comandes disponibles amb explicació detallada''' 
@bot.message_handler(commands=['help']) 
def help_command(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    help_text = ( 
        f"{user_name}, aquí tens les comandes disponibles i les seves funcions:\n\n" 
        "/start - Inicia el bot i comença una partida\n" 
        "/stop - Atura la partida actual\n" 
        "/top - Mostra el rànquing de jugadors, quan estigui disponible\n" 
        "/dlc - Activa continguts extres (DLC), en desenvolupament\n" 
        "/time - Activa el mode de joc amb temps\n" 
        "/help - Mostra aquest missatge d'ajuda\n" 
    ) 
    bot.reply_to(message, help_text) 
 
'''Funció per aturar la partida amb explicació detallada''' 
@bot.message_handler(commands=['stop']) 
def stop(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    bot.reply_to(message, f"{user_name}, has aturat la partida. Pots reiniciar-la amb /start.") 
 
'''Funció per mostrar el rànquing de jugadors amb explicació detallada''' 
@bot.message_handler(commands=['top']) 
def top(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    bot.reply_to(message, f"{user_name}, el rànquing encara no està disponible. Estem treballant-hi!") 
 
'''Funció per activar continguts extres (DLC) amb explicació detallada''' 
@bot.message_handler(commands=['dlc']) 
def dlc(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    bot.reply_to(message, f"{user_name}, la funcionalitat DLC encara no està disponible. Estem treballant en ella.") 
 
'''Funció per activar el mode amb temps amb explicació detallada''' 
@bot.message_handler(commands=['time']) 
def time(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    bot.reply_to(message, f"{user_name}, has activat el mode amb temps. Prepara't per jugar ràpid!") 
 
'''Funció per manejar els missatges de text i altres comandes''' 
@bot.message_handler(func=lambda message: True) 
def handle_text(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    bot.reply_to(message, f"{user_name}, no entenc aquest missatge. Prova una de les comandes disponibles amb /help.") 
 
'''Inici del bot''' 
print("") 
print("El bot està funcionant. Prem Ctrl+C per aturar-lo.") 
bot.polling()