import RPi.GPIO as GPIO
import time
from telegram.ext import Updater, CommandHandler
from picamera import PiCamera
'''
Imageio is a Python library that provides an easy interface to read and write a wide range of image data
including animated images, volumetric data, and scientific formats
'''
import imageio

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

cam = PiCamera()
cam.resolution = 'HD'
cam.rotation = 180

#Specify pin numbers
LED_R = 36
LED_G = 38
LED_B = 40
BUZ_PIN = 32
PIR_PIN = 7

#Sensor and LED RGB setup
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)
GPIO.setup(BUZ_PIN, GPIO.OUT)
GPIO.setup(PIR_PIN, GPIO.IN)

#Function for LED RGB lights
def setRed():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    GPIO.output(LED_R, GPIO.HIGH)
    GPIO.output(LED_G, GPIO.LOW)
    GPIO.output(LED_B, GPIO.LOW)

def setGreen():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_G, GPIO.HIGH)
    GPIO.output(LED_B, GPIO.LOW)

def setBlue():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_G, GPIO.LOW)
    GPIO.output(LED_B, GPIO.HIGH)

#Function for turn on and off alarm
def alarm_on():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUZ_PIN, GPIO.OUT)
    time.sleep(2)
    setRed()
    GPIO.output(BUZ_PIN, GPIO.HIGH)

def alarm_off():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUZ_PIN, GPIO.OUT)
    GPIO.output(BUZ_PIN, GPIO.LOW)
    GPIO.cleanup()
    setGreen()
    print('allarme spento')
    return 'allarme spento'

#Recording video function
def registration():
    images = []
    writer = imageio.get_writer('/home/pi/Desktop/video.mp4', fps=10) #Returns a Writer object which can be used to write data and meta data to the specified file
    for _ in range(100):
        cam.capture('video.jpg') #Capture an image from the camera, storing it in output.
        writer.append_data(imageio.imread('video.jpg')) #Append an image to the file video
    writer.close()

def relevation():
    setGreen()
    while True:
        i = GPIO.input(7)
        if i == 0:
            print('nessun intruso')
        elif i == 1:
            print('INTRUSO RILEVATO')
            alarm_on()
            registration()
            break
    return 'video pronto per essere inviato'

#Telegram bot
updater = Updater(token='1550096202:AAHg5KcjRTo7SkWosF2yBIyp88agalaf_x8', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Ciao sono il tuo nuovo sistema di videosorveglianza, ma puoi chiamarmi VSS. \n'
                                  'In questo bot ti segnalerò se rilevo dei movimenti in casa quando non ci sei. Tranquillo sei in buone mani, o meglio, in buoni circuiti\n'
                                  'Ecco i comandi che potrai utilizzare per controllarmi:\n'
                                  '/start_vss: ti permette di accendermi quando esci di casa.\n'
                                  "/stop_alarm: quando rilevo qualcuno faccio partire l'allarme; potrai decidere tu se spegnerlo o meno. \n"
                                  '/send_video: con questo comando potrai ricevere il video che registro e vedere chi è entrato in casa tua. \n')

def start_VSS(update, context):
    reply = relevation()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey, c'è qualcuno in casa tua")
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def stop_alarm(update, context):
    reply = alarm_off()
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    context.bot.send_message(chat_id=update.effective_chat.id, text='sistema pronto per un nuovo rilevamento')

def send_video(update, context):
    context.bot.send_video(chat_id=update.effective_chat.id, video=open('/home/pi/Desktop/video.mp4', 'rb'), supports_streaming=True)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

start_VSS_handler = CommandHandler('start_vss', start_VSS)
dispatcher.add_handler(start_VSS_handler)

stop_alarm_handler = CommandHandler('stop_alarm', stop_alarm)
dispatcher.add_handler(stop_alarm_handler)

send_video_handler = CommandHandler('send_video', send_video)
dispatcher.add_handler(send_video_handler)

print('I am listening...')
updater.start_polling()