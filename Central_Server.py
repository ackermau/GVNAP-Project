import os
import socket
import threading

def cmd_handler(connection_socket):
    signed_in = False
    while True:
        if(signed_in == False) :
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.connect((command_ip, command_port - 1))
            try:
                comfirmation = "Connected..."
                data_socket.send(comfirmation.encode('utf-8'))
                data_socket.close()
            except:
                print('failed sending comfirmation')
                data_socket.close()
            m = connection_socket.recv(buffer_size).decode('utf-8')
            cmd = m.split()[0]
            username = m.split()[1]
            hostname = m.split()[2]
            speedO = m.split()[3]
            if (cmd.upper() == 'SIGNIN'):
                sign_in(username, hostname, speedO)
                signed_in = True
            elif (cmd.upper() == 'QUIT'):
                quit_user(username, hostname, speedO)
                signed_in = False
                break
            list()
            file_collector(username, hostname, speedO)
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind((command_ip, command_port - 3))
        data_socket.listen()
        connection_socket, addr = data_socket.accept()
        file_keyword = connection_socket.recv(buffer_size).decode('utf-8')
        if (file_keyword.upper() == 'QUIT'):
            quit_user(username, hostname, speedO)
            signed_in = False
            break
        else:
            list_described_files(file_keyword)
        data_socket.close()
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind((command_ip, command_port + 2))
        data_socket.listen()
        connection_socket, addr = data_socket.accept()
        file_requested = connection_socket.recv(buffer_size).decode('utf-8')
        if (file_requested.upper() == 'QUIT'):
            quit_user(username, hostname, speedO)
            for file in req_list:
                quit_file(file, file_keyword)
            signed_in = False
            break
        else:
            print(file_requested)
            retrieve(file_requested.split()[1])
        data_socket.close()
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind((command_ip, command_port + 3))
        data_socket.listen()
        connection_socket, addr = data_socket.accept()
        terminate = connection_socket.recv(buffer_size).decode('utf-8')
        if(terminate.upper() == 'QUIT'):
            quit_user(username, hostname, speedO)
            for file in req_list:
                quit_file(file, file_keyword)
            signed_in = False
            print(users)
            print(files)
            break
        elif(terminate.upper() == 'NOPE'):
            pass


def sign_in(u_name, h_name, speed):
    users.append([u_name, h_name, speed])
    print(users)

def retrieve(f_name):
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((command_ip, command_port - 5))
    try:
        print(f_name)
        f = open(f_name, 'r')
        print('pass1')
        data = f.read(buffer_size)
        print(data)
        data_socket.send(data.encode('utf-8'))
        data_socket.close()
    except:
        print('failed sending file')
        data_socket.close()

def list():
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((command_ip, command_port + 1))
    try:
        dir_list = os.listdir(os.getcwd())
        list = '\n'.join(dir_list)
        data_socket.send(list.encode('utf-8'))
        data_socket.close()
    except:
        print('failed creating list')
        data_socket.close()

def file_collector(u_name, h_name, speed):
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind((command_ip, command_port - 2))
    data_socket.listen()
    connection_socket, addr = data_socket.accept()
    file = connection_socket.recv(buffer_size).decode('utf-8')
    if (file == 'QUIT'):
        quit_user(u_name, h_name, speed)
    else:
        file_sorter(file.split()[0], file.split()[1])
    data_socket.close()

def file_sorter(f_name, f_description):
    files.append([f_name, f_description])
    print(files)

def list_described_files(f_description):
    for file in files:
        if file[1] == f_description:
            req_list.append(file[0])
    print(req_list)
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((command_ip, command_port - 4))
    try:
        f_list = '\n'.join(req_list)
        data_socket.send(f_list.encode('utf-8'))
        data_socket.close()
    except:
        print('failed sending described files')
        data_socket.close()

def quit_user(u_name, h_name, speed):
    users.remove([u_name, h_name, speed])
    # command_socket.close()

def quit_file(f_name, f_description):
    files.remove([f_name, f_description])
    # command_socket.close()

command_ip = '216.171.56.60'
command_port = 7857 
buffer_size = 1024
users = [["Username", "Hostname", "Speed"]]
files = [["Filename", "File description"]]
req_list = []

command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_socket.bind((command_ip, command_port))

command_socket.listen()

while True:
    connection_socket, addr = command_socket.accept()
    threading.Thread(target=cmd_handler, args=(connection_socket,)).start()
    