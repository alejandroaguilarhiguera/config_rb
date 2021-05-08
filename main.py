from flask import Flask, request
import subprocess


app = Flask(__name__)

@app.route('/wireless', methods=['POST'])
def addWireless():
    request_data = request.get_json()
    ssid = None
    password = None
    #TODO: Intentar conectar
    if request_data:
        if 'ssid' in request_data:
            ssid = request_data['ssid']
        if 'password' in request_data:
            password = request_data['password']
    
    config_lines = [
    '\n',
    'network={',
    '\tssid="{}"'.format(ssid),
    '\tpsk="{}"'.format(password),
    '\tkey_mgmt=WPA-PSK',
    '}'
    ]
    config = '\n'.join(config_lines)
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as wifi:
        wifi.write(config)
    subprocess.run('rm /etc/dhcpcd.conf && cp /etc/dhcpcd.conf.orig.cliente_wifi /etc/dhcpcd.conf', shell=True)
    subprocess.run('reboot')

    return request_data
    #return True

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)


