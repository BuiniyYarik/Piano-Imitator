import socket

# create client socket for Wi-Fi network of ESP32 
host = '192.168.4.1'
port = 9900
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

try:
    # receive and print data from server while connection is opened
    while True:
        data = sock.recv(64).decode('utf-8')
        if data == "Close session":
            break
        print(f"Received message: \"{data}\"")

except socket.error as e:
    print(e)
except Exception as e:
    print(e)
finally:
    # close client socket
    print("Closing connection to the server...")
    print("See you again!")
    sock.close()
