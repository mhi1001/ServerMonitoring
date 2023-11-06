import threading
import socket
import json
import ssl
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import date

SERVER = "127.0.0.1"
PORT = 8080
INFLUX_TOKEN = "To"
ORG = "myOrg"
PROCESSES_BUCKET = "host_processes"
USAGE_BUCKET = ""


def handle_client(client_socket, client_addr):

    # Wrap the client socket in an SSL layer
    client_ssl_socket = context.wrap_socket(client_socket, server_side=True)

    print(f"{date.today()}:[CONNECTION] Client:{client_addr[0]}:{client_addr[1]} has connected to server ")

    # Receive data from the client
    data = b""
    while True:
        # Get chunks of 1024 bytes
        chunk = client_ssl_socket.read(1024)
        # Whenever the chunk is null, means there is no more data coming, so break out of the loop
        if not chunk:
            break
        
        # Append each chunk together
        print(f"{date.today()}:[CONNECTION] Receiving data from: {client_addr[0]}:{client_addr[1]}")
        data += chunk

    print(f"{date.today()}:[CONNECTION] Finished receiving data")
    print(f"{date.today()}:[CONNECTION] Closed. Disconnecting: {client_addr[0]}:{client_addr[1]}")

    # Decode data from bytes to utf8 str
    alldata = data.decode()

    # Deserialize the string into a python data structure
    list_data = json.loads(alldata)

    
    # Testing purposes
    # write_to_file(alldata)

def write_to_influx(sequence_list):
    
    with InfluxDBClient(url="http://192.168.0.134:8086", token=INFLUX_TOKEN, org=ORG) as client:
        
        for line in sequence_list:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(PROCESSES_BUCKET, ORG, line)

def write_to_file(data):
    with open("servertest.txt", "w") as fh:
        fh.write(data)


# Create a socket and bind it to a port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER, PORT))
server_socket.listen()

# Create an SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="ssl/server.crt", keyfile="ssl/server.key")
print(f"{date.today()}:[INFO] Listening on {SERVER}:{PORT}")

# Wait for a client to connect
while True:
  client_socket, client_address = server_socket.accept()
  print(f"Received a connection from {client_address}")

  # Create a new thread to handle the client
  print(f"{date.today()}:[INFO] Starting thread for connection {client_address}")
  thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
  thread.start()