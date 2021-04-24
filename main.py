from flask import Flask, request
from wireless import Wireless

wire = Wireless()
# Funciona !!!
#print(wire.connect(ssid='Ubee784A-2.4G',password='B5D7F6784A'))
#print(wire.current())
#print(wire.interfaces())

app = Flask(__name__)

@app.route('/wireless', methods=['POST'])
def addWireless():
    request_data = request.get_json()
    essid = None
    password = None
    #TODO: Intentar conectar
    if request_data:
        if 'essid' in request_data:
            essid = request_data['essid']
        if 'password' in request_data:
            password = request_data['password']
    # wire.connect(ssid=essid, password=password)
    return request_data

if __name__ == "__main__":
    app.run(debug=True)


