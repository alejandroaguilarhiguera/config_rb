import bluetooth

host = ""
port = 1
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('Start socket Bluetooth')
try:
	server.bind((host, port))
	print("Binding completed")
except:
	print("Binding incompleted")

server.listen(1)
client, address = server.accept()
print("connected:", address)
print("client:", client)
try:
	while True:
		data = client.recv(1024).decode("utf-8") 
		print(data)
		if data == 'a':
			print('Usted imprimió a')
		elif data == 'b':
			print("Usted imprimió b")
		else:
			print("Solo puede enviar a o b")
except KeyboardInterrupt:
	print('salio')
