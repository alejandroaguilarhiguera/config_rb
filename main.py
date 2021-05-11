import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import json
import threading
import time

load_dotenv()

uuid = os.getenv("UUID")
env = os.getenv("ENV")

callback_done = threading.Event()

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
device_document = device.document(uuid)
device_row = device_document.get()
if device_row.exists:
    print("Se asigna la configuración inicial")
    # TODO: Hacer la configuración inicial de un raspberry
    # TODO: Configurar entorno de pruebas 'env' = development
    device_document.set({
        "gpio": {
            "0": { "id": 1, "channel": 1},
            "1": { "id": 2, "channel": 2 }
        }  
    })
    data = device_row.to_dict()
    print(data)
else:
    
    device_document.create({ "name": "Inicio"})
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
            data = change.document.get("gpio")
            print(f'Actualización gpio: {data}')
        elif change.type.name == 'REMOVED':
            print(f'Dispositivo eliminado: {change.document.id}')
            delete_done.set()

    callback_done.set()

doc_watch = device_document.on_snapshot(on_snapshot)

while True:
    
    time.sleep(1)
    # TODO: No puede estar todo el tiempo a la escucha porque es muy pesado
    #doc_watch.unsubscribe()