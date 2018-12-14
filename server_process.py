def calc_checksum(data):
    checksum = 0
    i = 1
    for ch in data:
        checksum += ord(ch) * i
        i += 1
    #print(checksum)
    return checksum


import socket
import time
import datetime

serverPort = 13001
delimiter = "|\||\|"
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
while 1:
    ack = ''
    data, clientAddress = serverSocket.recvfrom(2048)
    message = data.decode("UTF-8")
    received_data = message.split(delimiter)  # [message checksum seq]
    print(received_data)
    if len(received_data) == 3:  # message not ack
        # print("calc "+str(calc_checksum(received_data[0])))

        if calc_checksum(received_data[0]) != int(received_data[1]):
            # corrupted data received
            # don't send any modified data
            # send neg ack
            print("corrupted data sent.......")
            ack = "FALSE" + delimiter + received_data[2]
            serverSocket.sendto(ack.encode("UTF-8"), clientAddress)
            time.sleep(1)

        else:  # data sent correctly
            print("Right data sent.......")
            ack = "TRUE" + delimiter + received_data[2]
            serverSocket.sendto(ack.encode("UTF-8"), clientAddress)
            time.sleep(1)
            modifiedMessage = received_data[0].upper()
            data_to_send = modifiedMessage + delimiter + received_data[1] + delimiter + received_data[2]
            serverSocket.sendto(data_to_send.encode("UTF-8"), clientAddress)
