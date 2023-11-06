import socket
import ssl
import psutil
import time
import json
from pathlib import Path

# Main server settings
SERVER = "127.0.0.1"
PORT = 8080


def write_to_file(data):
    with open("clienttest.txt", "w") as fh:
        fh.write(data)
        
def send_data_to_server(data):

    # Encode the data so you can send it via socket
    data = data.encode()
    
    # Create socket object, and specify AF_INET which specifies IPV4
    # SOCK_STREAM specifies TCP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        # Connect the socket to the server
        client.connect((SERVER, PORT))
        # Sending the data
        client.sendall(data)
        
def send_data_to_server_ssl(data):
    # Testing purposes write to file
    # write_to_file(data)

    # Create socket object, and specify AF_INET which specifies IPV4
    # SOCK_STREAM specifies TCP protocol
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create an SSL context
    # To allow self signed certificates - needed for create_unverified_context
    context = ssl._create_unverified_context()

    # Connect to the server
    client_ssl_socket = context.wrap_socket(client_socket, server_hostname=SERVER)
    client_ssl_socket.connect((SERVER, PORT))

    # Send some data to the server
    client_ssl_socket.send(data)

    # Gracefully shutdown socket
    client_ssl_socket.shutdown(socket.SHUT_WR)
    client_ssl_socket.close()
    
    print("[ INFO ] Data sent")

def get_system_running_processes():
    
    # Store sequences for each process
    processes = []
    
    # get ip address MAYBE check for exceptions
    ip = get_own_ip_address()
    
    
    # Iterate over all running processes in the system
    for proc in psutil.process_iter():
        try:
            
            if proc.name() != "":
                
                # get process name
                proc_name = proc.name()
                # get the full path of each process
                proc_path = proc.exe()
                proc_path = Path(proc_path)
                # get process memory usage
                proc_mem_usage = round(proc.memory_info().rss/(1024*1024), 2)
                # get process memory percentage
                proc_mem_percentage = round(proc.memory_percent(),2)
                # get process Create time
                time_create = proc.create_time()
                proc_creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_create))
                # get process PID
                proc_pid = proc.pid
                
                # InfluxDB Line Protocol
                line = f'proc_mon,host={ip} name="{proc_name}",pid={proc_pid},path="{proc_path}",mem_usage={proc_mem_usage},mem_percent={proc_mem_percentage},creation_time="{proc_creation_time}"'

                # Append to list
                processes.append(line)
            
            # Catch common exceptions 
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  
        
    return processes

def get_own_ip_address():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((SERVER, PORT))
    return s.getsockname()[0]

# Get stats from the system
sequence_list = get_system_running_processes()

# Serialize python datastructure into string
data = json.dumps(sequence_list)

# Encode the string data into bytes so it can be sent via socket
data = data.encode()

# Send the data to the main system via SSL socket TCP
send_data_to_server_ssl(data=data)
