import pandas as pd 
import telebot 
from telebot import types 
 
# Tu token del bot de Telegram 
TOKEN = '7455775782:AAGAnwCVb1yitZY-dXUMflFQPeOSY4WEyyc' 
bot = telebot.TeleBot(TOKEN) 
 
# Funció per enviar un missatge de benvinguda amb informació detallada 
@bot.message_handler(commands=['start']) 
def start(message): 
    user_name = message.from_user.first_name  # Obtén el primer nom de l'usuari 
    welcome_text = ( 
        "¿Qué es lo que puede hacer nuestro bot @TrivialverseQuizBot?\n\n" 
        "Este es un bot de preguntas tipo trivial que te permite poner a prueba tus conocimientos. " 
        "Si quieres competir con amigos, simplemente abre el perfil del bot y usa el botón 'Añadir a grupo'.\n\n" 
        "Envía /start para comenzar el quiz.\n" 
        "Escribe /stop cuando quieras detener el quiz.\n" 
        "Envía /stats si quieres ver quién va ganando.\n" 
    ) 
     
    # Enviar el mensaje de bienvenida centrado 
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown') 
    show_menu(message.chat.id) 
 
# Funció per mostrar el menú amb botons d'opcions 
def show_menu(chat_id): 
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Crea un teclat a la pantalla 
    menu_button = types.KeyboardButton("☰ Menú")  # Botó amb 3 ratlles "menú" 
    markup.add(menu_button) 
    bot.send_message(chat_id, "Prem el botó ☰ Menú per veure les opcions disponibles.", reply_markup=markup) 
 
# Funció per gestionar el desplegable de "tres ratlles" 
@bot.message_handler(func=lambda message: message.text == "☰ Menú") 
def menu_handler(message): 
    markup = types.InlineKeyboardMarkup()  # Crea el teclat en línia per mostrar les opcions 
    commands = [ 
        ("Iniciar partida", "start_game"), 
        ("Aturar partida", "stop_game"), 
        ("Rànquing de jugadors", "top_players"), 
        ("DLC", "dlc_content"), 
        ("Mode ràpid", "fast_mode"), 
        ("Ajuda", "help") 
    ] 
    for command, callback_data in commands: 
        markup.add(types.InlineKeyboardButton(command, callback_data=callback_data)) 
     
    bot.send_message(message.chat.id, "Selecciona una opció del menú:", reply_markup=markup) 
 
# Funció per gestionar els botons del menú en línia 
@bot.callback_query_handler(func=lambda call: True) 
def handle_callback(call): 
    if call.data == "start_game": 
        start_game(call.message) 
    elif call.data == "stop_game": 
        stop(call.message) 
    elif call.data == "top_players": 
        top(call.message) 
    elif call.data == "dlc_content": 
        dlc(call.message) 
    elif call.data == "fast_mode": 
        time(call.message) 
    elif call.data == "help": 
        help_command(call.message) 
 
 
 
 
# Ejemplo poco funcional 
 
 
# Funció per començar una partida de trivia 
def start_game(message): 
    bot.send_message(message.chat.id, "Comença el trivial! Tria la resposta correcta.") 
    send_trivia_question(message.chat.id) 
 
# Funció per enviar una pregunta de trivial amb opcions (A, B, C, D) 
def send_trivia_question(chat_id): 
    question = "Con que se craftea un corazon del mar?" 
    options = ["A) Corazon del mar i prismarina", "B) corazon del mar i pepitas de acero", "C) Corazon del mar i caparazones de nautilus", "D) caparazones nautilus, prismarina i piedra luminosa"] 
 
    markup = types.InlineKeyboardMarkup() 
    option_buttons = [ 
        types.InlineKeyboardButton("A", callback_data="A"), 
        types.InlineKeyboardButton("B", callback_data="B"), 
        types.InlineKeyboardButton("C", callback_data="C"), 
        types.InlineKeyboardButton("D", callback_data="D") 
    ] 
     
    for button in option_buttons: 
        markup.add(button) 
 
    bot.send_message(chat_id, question, reply_markup=markup) 
 
# Funció per gestionar les respostes de les opcions de trivia 
@bot.callback_query_handler(func=lambda call: call.data in ['A', 'B', 'C', 'D']) 
def trivia_response(call): 
    correct_answer = "C" 
    user_answer = call.data 
 
    if user_answer == correct_answer:
        bot.send_message(call.message.chat.id, "Correcte! 🎉") 
    else: 
        bot.send_message(call.message.chat.id, "Incorrecte. La resposta correcta és C) caparazones del mar i caparazones nautilus.") 
 
 
 
 
# Altres funcions del bot 
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
 
@bot.message_handler(commands=['stop']) 
def stop(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    bot.reply_to(message, f"{user_name}, has aturat la partida. Pots reiniciar-la amb /start.") 
 
@bot.message_handler(commands=['top']) 
def top(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    bot.reply_to(message, f"{user_name}, el rànquing encara no està disponible. Estem treballant-hi!") 
 
@bot.message_handler(commands=['dlc']) 
def dlc(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    bot.reply_to(message, f"{user_name}, la funcionalitat DLC encara no està disponible. Estem treballant en ella.") 
 
@bot.message_handler(commands=['time']) 
def time(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    bot.reply_to(message, f"{user_name}, has activat el mode amb temps. Prepara't per jugar ràpid!") 
 
# Inici del bot 
print("") 
print("El bot està funcionant. Prem Ctrl+C per aturar-lo.") 
bot.polling()