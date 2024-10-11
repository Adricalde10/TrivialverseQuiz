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
correct_answer = None  # Variable para almacenar la respuesta correcta
score = 0  # Variable para almacenar la puntuación del jugador
scores = {}  # Diccionario para almacenar las puntuaciones de los usuarios

# Función para leer datos de un archivo ODS y mostrarlos al usuario
def leer_ods():
    try:
        hojas_dict = pd.read_excel(ODS_FILE, engine='odf', sheet_name=None)  # Lee todas las hojas
        return hojas_dict
    except Exception as e:
        print(f"Error leyendo el archivo ODS: {e}")
        return None

# Función para obtener preguntas, categorías, respuestas y la respuesta correcta de una hoja
def obtener_preguntas_y_respuestas(df):
    preguntas = []
    for index, row in df.iterrows():
        pregunta = row[0]  # Primera columna es la pregunta
        categoria = row[1]  # Segunda columna es la categoría
        respuestas = row[2:-1].dropna().tolist()  # Las respuestas están en las columnas siguientes, excepto la última
        respuesta_correcta = row[-1]  # Última columna es la respuesta correcta
        preguntas.append((pregunta, categoria, respuestas, respuesta_correcta))
    return preguntas

@bot.message_handler(commands=['start'])
def start(message):
    global score  # Hacemos que la variable de puntuación sea global
    user_id = message.from_user.id  # Obtén el ID del usuario
    scores[user_id] = 0  # Inicializa la puntuación del usuario
    score = 0  # Reinicia la puntuación al iniciar el juego
    user_name = message.from_user.first_name  # Obtén el nombre del usuario
    
    # Enviar términos y condiciones
    terms_and_conditions = (
        "Términos y Condiciones de Uso para TrivialverseQuiz\n\n"
        "1. Aceptación de los Términos\n"
        "Al acceder o utilizar el bot de Telegram TrivialverseQuiz, aceptas cumplir con estos Términos y Condiciones. "
        "Si no estás de acuerdo con alguna parte de estos términos, no debes usar el bot.\n\n"
        "2. Descripción del Servicio\n"
        "TrivialverseQuiz es un bot de trivia que permite a los usuarios participar en juegos de preguntas y respuestas. "
        "Los usuarios pueden seleccionar categorías de preguntas, responder a las preguntas y ver sus puntuaciones en un ránking.\n\n"
        "3. Uso del Bot\n"
        "- Debes tener al menos 13 años para utilizar el bot. Si eres menor de 13 años, necesitas el consentimiento de tus padres o tutores para utilizarlo.\n"
        "- Te comprometes a usar el bot de manera responsable y a no participar en actividades fraudulentas o perjudiciales.\n"
        "- Nos reservamos el derecho de suspender o cancelar tu acceso al bot si se determina que has violado estos Términos y Condiciones.\n\n"
        "4. Propiedad Intelectual\n"
        "Todo el contenido, incluidos los textos, gráficos, logos y otros materiales, es propiedad de TrivialverseQuiz o de sus licenciantes y está protegido por las leyes de derechos de autor y propiedad intelectual.\n\n"
        "5. Datos del Usuario\n"
        "- Nos comprometemos a proteger la privacidad de los usuarios. No recopilaremos información personal sin tu consentimiento.\n"
        "- Los datos recopilados durante el uso del bot se utilizarán únicamente para fines relacionados con el funcionamiento del servicio.\n"
        "- Puedes solicitar la eliminación de tu cuenta y datos en cualquier momento.\n\n"
        "6. Modificaciones a los Términos\n"
        "Nos reservamos el derecho de modificar estos Términos y Condiciones en cualquier momento. Te notificaremos sobre cambios significativos y tu uso continuado del bot después de tales modificaciones constituirá tu aceptación de los nuevos términos.\n\n"
        "7. Limitación de Responsabilidad\n"
        "En la medida máxima permitida por la ley, TrivialverseQuiz no será responsable de ningún daño directo, indirecto, incidental, especial o consecuente que resulte del uso o la imposibilidad de usar el bot.\n\n"
        "8. Ley Aplicable\n"
        "Estos Términos y Condiciones se regirán e interpretarán de acuerdo con las leyes de [Tu País o Estado]. "
        "Cualquier disputa que surja en relación con estos términos será resuelta en los tribunales competentes de [Tu Ciudad o Estado].\n\n"
        "9. Contacto\n"
        "Si tienes preguntas sobre estos Términos y Condiciones, puedes ponerte en contacto con nosotros a través de [tu dirección de contacto o correo electrónico]."
    )
    
    bot.reply_to(message, f"Benvingut a TrivialverseQuiz, {user_name}! Tria una categoria per començar.\n\n{terms_and_conditions}")
    show_menu(message.chat.id)

@bot.message_handler(commands=['Quiz'])
def enviar_Quiz(message):
    global current_question, correct_answer, is_game_active, score  # Hacemos que las variables sean globales
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
            pregunta, categoria, respuestas, respuesta_correcta = random.choice(preguntas)
            current_question = (pregunta, respuestas)  # Almacena la pregunta actual
            correct_answer = respuesta_correcta  # Almacena la respuesta correcta
            enviar_pregunta_con_respuestas(message.chat.id, pregunta, categoria, respuestas)
        else:
            bot.reply_to(message, f"La hoja '{nombre_hoja}' no contiene preguntas.")
        
        break  # Elimina esta línea si quieres obtener preguntas de más de una hoja

def enviar_pregunta_con_respuestas(chat_id, pregunta, categoria, respuestas):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Agregar botones para cada respuesta
    for respuesta in respuestas:
        markup.add(types.KeyboardButton(respuesta))
    
    # Enviar la pregunta junto con la categoría
    bot.send_message(chat_id, f"Categoría: {categoria}\nPregunta: {pregunta}", reply_markup=markup)

@bot.message_handler(func=lambda message: is_game_active and message.text not in ['/stop', '/start'])
def handle_response(message):
    global correct_answer, is_game_active, score, scores  # Usamos la respuesta correcta, el estado del juego y la puntuación

    respuesta_usuario = message.text
    user_id = message.from_user.id  # Obtén el ID del usuario

    # Verificamos si la respuesta del usuario es correcta
    if respuesta_usuario == correct_answer:
        score += 1  # Incrementar la puntuación en 1
        scores[user_id] = score  # Actualiza la puntuación en el diccionario
        bot.reply_to(message, f"¡Correcto! 🎉 Tu puntuación actual es: {score}")
        # Llama a la función para enviar una nueva pregunta
        enviar_nueva_pregunta(message.chat.id)
    else:
        bot.reply_to(message, f"Respuesta incorrecta. La respuesta correcta era: {correct_answer}. Tu puntuación final es: {score}. El juego ha sido detenido.")
        is_game_active = False  # Detener el juego si la respuesta es incorrecta

def enviar_nueva_pregunta(chat_id):
    global current_question, correct_answer  # Usar la variable global
    hojas = leer_ods()
    
    if hojas is None:
        bot.reply_to(chat_id, "Error al leer el archivo ODS.")
        return

    # Envia una nueva pregunta de una de las hojas
    for nombre_hoja, df in hojas.items():
        preguntas = obtener_preguntas_y_respuestas(df)

        # Selecciona una pregunta aleatoria
        if preguntas:
            pregunta, categoria, respuestas, respuesta_correcta = random.choice(preguntas)
            current_question = (pregunta, respuestas)  # Actualiza la pregunta actual
            correct_answer = respuesta_correcta  # Actualiza la respuesta correcta
            enviar_pregunta_con_respuestas(chat_id, pregunta, categoria, respuestas)
        else:
            bot.reply_to(chat_id, f"La hoja '{nombre_hoja}' no contiene preguntas.")
        
        break  # Elimina esta línea si quieres obtener preguntas de más de una hoja

@bot.message_handler(commands=['stop'])
def stop_game(message):
    global is_game_active  # Hacemos que la variable sea global
    is_game_active = False  # Detener el juego
    user_id = message.from_user.id  # Obtén el ID del usuario
    bot.reply_to(message, f"El juego ha sido detenido. Tu puntuación final es: {scores.get(user_id, 0)}. Puedes iniciar nuevamente con el comando /start.")

# Funció per mostrar les comandes disponibles amb explicació detallada''' 
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

# Funció per mostrar el rànquing de jugadors
@bot.message_handler(commands=['top'])
def show_top(message):
    if not scores:
        bot.reply_to(message, "No hi ha puntuacions disponibles.")
        return

    # Ordenar el diccionario de puntuaciones por valor en orden descendente
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Crear el mensaje de puntuaciones
    ranking_message = "Rànquing de Jugadors:\n"
    for user_id, score in sorted_scores:
        user = bot.get_chat(user_id)  # Obtener información del usuario
        ranking_message += f"{user.first_name}: {score} punts\n"

    bot.reply_to(message, ranking_message)

# Funció per activar continguts extres (DLC) amb explicació detallada
@bot.message_handler(commands=['dlc'])
def dlc(message):
    user_name = message.from_user.first_name  # Obtén el nom de l'usuari
    bot.reply_to(message, f"{user_name}, la funcionalitat DLC encara no està disponible. Estem treballant en ella.")

def show_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn_excel = types.KeyboardButton('/Quiz')  # Agrega un botón para ver los datos del archivo ODS
    btn_help = types.KeyboardButton('/help')
    btn_top = types.KeyboardButton('/top')
    btn_stop = types.KeyboardButton('/stop')  # Agrega un botón para detener el juego
    markup.add(btn_excel, btn_top, btn_help, btn_stop)
    bot.send_message(chat_id, "Prem un botó per seleccionar una opció:", reply_markup=markup)

# Inici del bot
print("El bot està funcionant. Prem Ctrl+C per aturar-lo.")
bot.polling()
