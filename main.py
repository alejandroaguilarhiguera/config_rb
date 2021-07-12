import firebase_admin
from firebase_admin import credentials, firestore, auth
import RPi.GPIO as gpio
import os
from dotenv import load_dotenv
import json
import threading
import time

load_dotenv()

uuid = os.getenv("UUID")
env = os.getenv("ENV")

callback_done = threading.Event()
gpio.setmode(gpio.BCM)
cred = credentials.Certificate({
    "type": os.getenv("FIRESTORE_TYPE"),
    "project_id": os.getenv("FIRESTORE_PROJECT_ID"),
    "private_key_id": os.getenv("FIRESTORE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIRESTORE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIRESTORE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIRESTORE_CLIENT_ID"),
    "auth_uri": os.getenv("FIRESTORE_AUTH_URI"),
    "token_uri": os.getenv("FIRESTORE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIRESTORE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIRESTORE_X509_CERT_URL"),
})
owner = os.getenv("OWNER")

firebase_admin.initialize_app(cred)
database = firestore.client()


device = database.collection("devices")
gpios = database.collection("gpios")

device_document = device.document(uuid)
device_row = device_document.get()

channels = []

if device_row.exists:
    print("Se asigna la configuración inicial")
    # TODO: Hacer la configuración inicial de un raspberry
    # TODO: Configurar entorno de pruebas 'env' = development
    data = device_row.to_dict()
    data_gpios = data['gpio']
    for key in data_gpios:
        index = data_gpios.index(key)
        channel = data_gpios[index]
        channels.append(channel)
        row = channel.get()
        channel_data = row.to_dict()
        print('channel ', channel_data['channel'])
        print('Status ', "LOW" if channel_data['value'] == 0 else "HIGH" )
        # PRODUCCIÓN
        gpio.setup(channel_data['channel', gpio.OUT])
        gpio.output(channel_data['channel'], gpio.LOW if channel_data['value'] == 0 else gpio.HIGH)

else:
    # Inicializar
    gpio_data = [
        {"channel": 23, 'value': 0},
        {"channel": 24, 'value': 0},
    ]
    array_document_gpio = []

    for key in gpio_data:
        index = gpio_data.index(key)
        channels.append(gpios.document())
        channels[index].create(gpio_data[index])
        array_document_gpio.append(gpios.document(channels[index].id))
        # PRODUCCIÓN
        gpio.setup(gpio_data[index].channel, gpio.OUT)
        gpio.output(gpio_data[index].channel, gpio.LOW if gpio_data[index].value == 0 else gpio.HIGH)

    device_document.create({
        "name": "Inicio",
        "gpio": array_document_gpio,
        "owner": owner,
    })
    print("Se ha creado un documento")


def on_snapshot(doc_snapshot, changes, read_time):
    #for doc in doc_snapshot:
    #    print(f'Received document snapshot: {doc.id}')
    for change in changes:
        print(change)
        if change.type.name == 'ADDED':
            print(f'Dispositívo nuevo: {change.document.id}')
        elif change.type.name == 'MODIFIED':
            print(f'Dispositívo modificado: {change.document.id}')
            value = change.document.get("value")
            channel = change.document.get("channel")
            #FIXME: Se tiene que tener un mejor lugar para colocar esto
            gpio.setup(channel,gpio.OUT)
            gpio.output(channel, gpio.LOW if value == 0 else gpio.HIGH)
            print(f'Actualización gpio {channel} con valor: {value}')
        elif change.type.name == 'REMOVED':
            print(f'Dispositivo eliminado: {change.document.id}')
            delete_done.set()

    callback_done.set()
doc_watch = []
for channel in channels:
    doc_watch.append(channel.on_snapshot(on_snapshot))

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('keyboard interript')
finally:
    print("gpio.cleanup")
    #gpio.cleanup()
    for doc in doc_watch:
        doc.unsubscribe()
    # TODO: No puede estar todo el tiempo a la escucha porque es muy pesado
