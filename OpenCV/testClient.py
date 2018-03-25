import socket

s = socket.socket()
host = "localhost"
port = 8800
s.connect((host, port))

file = open("./test_images/images.jpg", "rb")
imgData = file.read()

s.send(imgData)

s.close()