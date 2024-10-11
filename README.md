# TrivialVerseQuiz
![Logo del Bot](botlogo.png)

## Descripción

TrivialVerseQuiz es un bot de Telegram diseñado para ofrecer un juego de trivia donde los usuarios pueden probar sus conocimientos en diversas categorías. Este bot es fácil de usar y permite a los jugadores competir entre sí en un ambiente interactivo.

## Funciones Obligatorias

- Para desarrollar el bot, es necesario tener **Python 3** instalado en tu sistema. Además, necesitas instalar la biblioteca **pyTelegramBotAPI**, que permite interactuar con el API de Telegram Bot. Para instalarlo, abre la terminal de Visual Studio y ejecuta el siguiente comando:

```bash
pip install pyTelegramBotAPI
```

- Pandas: Para manejar los datos del archivo ODS, necesitarás la biblioteca pandas. Puedes instalarla con:
bash

```
pip install pandas
```

## Token

- Para que el bot fucione hemos utilizado el BotFather para que nos genere un Token, el token en el codigo ira algo asi:
```
TOKEN = '7455775782:AAGAnwCVb1yitZY-dXUMflFQPeOSY4WEyyc'

bot = telebot.TeleBot(TOKEN)
```

## Implementacion Archvi ODS

- Para que el bot nos muestre las preguntas hemos tenido que descargarlo del drive ja que no sabiamos como conjuntar el archivo drive, por eso lo hemos hecho de manera local descargando el archivo y poniendolo en la misma carpeta.

para ejecutar el archivo tenemos que utilitzar este comando

```
ODS_FILE = 'Preguntas bot.ods'

```
esto sirve para que encuentre el archivo

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

## Comando de Ayudas

1. **help_command(message):**

 Muestra la lista de comandos disponibles y sus explicaciones.

2. **dlc(message):**

 Informa sobre la funcionalidad DLC que está en desarrollo.

 ## Obtencion de preguntas y Respuestas

 - para que el bot recorra las preguntas mediante el archivo ods, tiene que leer el archivo con la siguiente comanda

 ```
hojas_dict = pd.read_excel(ODS_FILE, engine='odf', sheet_name=None)
 ```

 1. **pd.read_excel:**

Es una funcion de Pandas que sirve para leer archivos Excel, y es compatible com los archivos ODS de libreOffice si utilizamos esta extencion  **engine='odf'**

2. **sheet_name=None:**

 Esto le dice a la función que debe leer todas las hojas del archivo

Para las Respuestas hemos creado una nueva variable donde recorrera toda la hoja mediante un for para hacerlo en bucle empezando desde la primera linea
```
for index, row in df.iterrows():
    pregunta = row[0]  # Asumiendo que la primera columna es la pregunta
    respuestas = row[2:].dropna().tolist()  # Las respuestas están en las columnas siguientes
    preguntas.append((pregunta, respuestas))
```
## Ejemplo de Pregunta

El bot puede enviar preguntas de trivia como:

¿Con qué se craftea un corazón del mar?

A) Corazón del mar y prismarina
B) Corazón del mar y pepitas de acero
C) Corazón del mar y caparazones de nautilus
D) Caparazones de nautilus, prismarina y piedra luminosa

## Finalizar Bot

- Para finalizar el bot hemos utilitzado tenemos que precionar Ctrl + C, ja que sino el bot entra en un bucle infinito a la espera de una respuesta del usuari