# TrivialVerseQuiz
![Logo del Bot](botlogo.png)

## Descripción

TrivialVerseQuiz es un bot de Telegram diseñado para ofrecer un juego de trivia donde los usuarios pueden probar sus conocimientos en diversas categorías. Este bot es fácil de usar y permite a los jugadores competir entre sí en un ambiente interactivo.

## Funciones Obligatorias

Para desarrollar el bot, es necesario tener **Python 3** instalado en tu sistema. Además, necesitas instalar la biblioteca **pyTelegramBotAPI**, que permite interactuar con el API de Telegram Bot. Para instalarlo, abre la terminal de Visual Studio y ejecuta el siguiente comando:

```bash
pip install pyTelegramBotAPI
```

## Token

- Para que el bot fucione hemos utilizado el BotFather para que nos genere un Token, el token en el codigo ira algo asi:

TOKEN = '7455775782:AAGAnwCVb1yitZY-dXUMflFQPeOSY4WEyyc'

bot = telebot.TeleBot(TOKEN)


## Funcionalidades y Comandos Principales

1. **/start**

Inicia el bot, da la bienvenida al usuario y le invita a seleccionar una categoría para comenzar.

2. **/help**

Muestra la lista de comandos disponibles y su funcionalidad.

3. **/stop**

Detiene la partida actual.

4. **/top**

Muestra el ranking de jugadores (aún en desarrollo).

6. **/time**

 Activa el modo de juego con tiempo.

5. **/dlc**

Indica que el contenido adicional (DLC) está en desarrollo.

## Comandas Basicas de Telegram Bot

1. **start(message):**

 Envía un mensaje de bienvenida y muestra el menú de opciones.

2. **show_menu(chat_id):**

 Muestra el menú de opciones disponibles.

3. **menu_handler(message):** 

Gestiona la selección de opciones del menú.

4. **start_game(message):** 

Inicia una partida de trivia.

5. **send_trivia_question(chat_id):** 

Envía una pregunta de trivia con opciones de respuesta.

6. **trivia_response(call):**

 Maneja la respuesta del usuario a una pregunta de trivia.

## Ejemplo de Pregunta

El bot puede enviar preguntas de trivia como:

¿Con qué se craftea un corazón del mar?

A) Corazón del mar y prismarina
B) Corazón del mar y pepitas de acero
C) Corazón del mar y caparazones de nautilus
D) Caparazones de nautilus, prismarina y piedra luminosa

## Finalizar Bot

- Para finalizar el bot hemos utilitzado tenemos que precionar Ctrl + C, ja que sino el bot entra en un bucle infinito a la espera de una respuesta del usuari