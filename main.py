import telebot
from telebot import types
import pandas as pd
import random

# Token del bot de Telegram
TOKEN = '7455775782:AAGAnwCVb1yitZY-dXUMflFQPeOSY4WEyyc'
bot = telebot.TeleBot(TOKEN)

# Ruta del archivo ODS (LibreOffice)
ODS_FILE = 'Preguntas bot.ods'

# Variables para controlar el estado del juego
current_question = None
is_game_active = False  # Variable para controlar si el juego está activo

# Función para leer datos de un archivo ODS y mostrarlos al usuario
def leer_ods():
    try:
        hojas_dict = pd.read_excel(ODS_FILE, engine='odf', sheet_name=None)  # Lee todas las hojas
        return hojas_dict
    except Exception as e:
        print(f"Error leyendo el archivo ODS: {e}")
        return None

# Función para obtener preguntas y respuestas de una hoja
def obtener_preguntas_y_respuestas(df):
    preguntas = []
    for index, row in df.iterrows():
        pregunta = row[0]  # Asumiendo que la primera columna es la pregunta
        respuestas = row[2:].dropna().tolist()  # Las respuestas están en las columnas siguientes
        preguntas.append((pregunta, respuestas))
    return preguntas

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name  # Obtén el nombre del usuario
    bot.reply_to(message, f"Benvingut a TrivialverseQuiz, {user_name}! Tria una categoria per començar.")
    show_menu(message.chat.id)

@bot.message_handler(commands=['Quiz'])
def enviar_Quiz(message):
    global current_question, is_game_active  # Hacemos que las variables sean globales
    is_game_active = True  # Iniciar el juego
    hojas = leer_ods()
    
    if hojas is None:
        bot.reply_to(message, "Error al leer el archivo ODS. Asegúrate de que el archivo esté disponible y tenga el formato correcto.")
        return

    # Envia una pregunta de una de las hojas
    for nombre_hoja, df in hojas.items():
        preguntas = obtener_preguntas_y_respuestas(df)
        
        # Selecciona una pregunta aleatoria
        if preguntas:
            pregunta, respuestas = random.choice(preguntas)
            current_question = (pregunta, respuestas)  # Almacena la pregunta actual
            enviar_pregunta_con_respuestas(message.chat.id, pregunta, respuestas)
        else:
            bot.reply_to(message, f"La hoja '{nombre_hoja}' no contiene preguntas.")
        
        break  # Elimina esta línea si quieres obtener preguntas de más de una hoja

def enviar_pregunta_con_respuestas(chat_id, pregunta, respuestas):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Agregar botones para cada respuesta
    for respuesta in respuestas:
        markup.add(types.KeyboardButton(respuesta))
    
    bot.send_message(chat_id, pregunta, reply_markup=markup)

@bot.message_handler(func=lambda message: is_game_active and message.text not in ['/stop', '/start'])
def handle_response(message):
    respuesta_usuario = message.text
    # Aquí puedes manejar la lógica para verificar si la respuesta es correcta
    # Esto depende de cómo quieras estructurar la correcta
    # Por ahora, simplemente responderemos con un mensaje
    bot.reply_to(message, f"Has elegido: {respuesta_usuario}. ¡Gracias por responder!")

    # Llama a la función para enviar una nueva pregunta
    enviar_nueva_pregunta(message.chat.id)

def enviar_nueva_pregunta(chat_id):
    global current_question  # Usar la variable global
    hojas = leer_ods()
    
    if hojas is None:
        bot.reply_to(chat_id, "Error al leer el archivo ODS.")
        return

    # Envia una nueva pregunta de una de las hojas
    for nombre_hoja, df in hojas.items():
        preguntas = obtener_preguntas_y_respuestas(df)

        # Selecciona una pregunta aleatoria
        if preguntas:
            pregunta, respuestas = random.choice(preguntas)
            current_question = (pregunta, respuestas)  # Actualiza la pregunta actual
            enviar_pregunta_con_respuestas(chat_id, pregunta, respuestas)
        else:
            bot.reply_to(chat_id, f"La hoja '{nombre_hoja}' no contiene preguntas.")
        
        break  # Elimina esta línea si quieres obtener preguntas de más de una hoja

@bot.message_handler(commands=['stop'])
def stop_game(message):
    global is_game_active  # Hacemos que la variable sea global
    is_game_active = False  # Detener el juego
    bot.reply_to(message, "El juego ha sido detenido. Puedes iniciar nuevamente con el comando /start.")

#Funció per mostrar les comandes disponibles amb explicació detallada''' 
@bot.message_handler(commands=['help']) 
def help_command(message): 
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari 
    help_text = ( 
        f"{user_name}, aquí tens les comandes disponibles i les seves funcions:\n\n" 
        "/start - Inicia el bot i comença una partida\n" 
        "/stop - Atura la partida actual\n" 
        "/top - Mostra el rànquing de jugadors, quan estigui disponible\n" 
        "/dlc - Activa continguts extres (DLC), en desenvolupament\n" 
        "/help - Mostra aquest missatge d'ajuda\n" 
    ) 
    bot.reply_to(message, help_text)

#Funció per activar continguts extres (DLC) amb explicació detallada
@bot.message_handler(commands=['dlc'])
def dlc(message):
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari
    bot.reply_to(message, f"{user_name}, la funcionalitat DLC encara no està disponible. Estem treballant en ella.")

def show_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn_excel = types.KeyboardButton('/Quiz')  # Agrega un botón para ver los datos del archivo ODS
    btn_help = types.KeyboardButton('/help')
    btn_stop = types.KeyboardButton('/stop')  # Agrega un botón para detener el juego
    markup.add(btn_excel, btn_help, btn_stop)
    bot.send_message(chat_id, "Prem un botó per seleccionar una opció:", reply_markup=markup)

# Inici del bot
print("El bot està funcionant. Prem Ctrl+C per aturar-lo.")
bot.polling()