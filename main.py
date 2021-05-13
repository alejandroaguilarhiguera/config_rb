import firebase_admin
from firebase_admin import credentials, firestore
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
    "client_x509_cert_url": os.getenv("FIRESTORE_X509_CERT_URL")
})
firebase_admin.initialize_app(cred)

database = firestore.client()
device = database.collection("devices")
gpios = database.collection("gpios")

device_document = device.document(uuid)
device_row = device_document.get()

channel1 = gpios.document()
channel2 = gpios.document()
if device_row.exists:
    print("Se asigna la configuración inicial")
    # TODO: Hacer la configuración inicial de un raspberry
    # TODO: Configurar entorno de pruebas 'env' = development


    
    data = device_row.to_dict()
    data_gpios = data['gpio']

    channel1 = data_gpios['0']
    gpio.setup(channel1['channel'], gpio.OUT)

    if channel1['value'] == 1:
        gpio.output(channel1['channel'], gpio.LOW)
    else:
        gpio.output(channel1['channel'], gpio.HIGH)

    channel2 = data_gpios['1']
    gpio.setup(channel2['channel'], gpio.OUT)
    if channel2['value'] == 1:
        gpio.output(channel2['channel'], gpio.LOW)
    else:
        gpio.output(channel2['channel'], gpio.HIGH)

    
    print(data_gpios)
else:
    channel1.create({ "channel": 23, "value": 0 })
    channel2.create({ "channel": 24, "value": 0 })
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    gpio.output(channel1, gpio.HIGH)
    gpio.output(channel2, gpio.HIGH)
    
    device_document.create({
        "name": "Inicio",
        "gpio": {
            "0": gpios.document(channel1.id),
            "1": gpios.document(channel2.id),
        }
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
            if value == 1:
                gpio.output(channel, gpio.LOW)
            else:
                gpio.output(channel, gpio.HIGH)
            print(f'Actualización gpio {channel} con valor: {value}')
        elif change.type.name == 'REMOVED':
            print(f'Dispositivo eliminado: {change.document.id}')
            delete_done.set()

    callback_done.set()

doc_watch = channel1.on_snapshot(on_snapshot)
doc_watch = channel2.on_snapshot(on_snapshot)

while True:
    try:

        time.sleep(1)
    except KeyboardInterrupt:
        print('keyboard interript')
    finally:
        gpio.cleanup()
    # TODO: No puede estar todo el tiempo a la escucha porque es muy pesado
    #doc_watch.unsubscribe()