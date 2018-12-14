import socket
import time
import datetime
import random

def calc_checksum(data):
    checksum=0
    i=1
    for ch in data:
        checksum += ord(ch)*i
        i=i+1
    return checksum


def test_random_cases(message) :
    r=random.random()
    if(r>0.7):
        # insert fake chars
        print("fake message sent : ")
        message = message + "abcd"
        return message
    return message



delimiter="|\||\|"
seq=0


serverName = 'localhost'
serverPort = 13001

timeOut = 2
isSafeDataReceived = False
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
message = input('Input lowercase sentence: ')

calcualated_message = test_random_cases(message)  # to check when fake data  sent randomly later add when we drop the message to test time out
data_to_send=calcualated_message + delimiter + str(calc_checksum(message))+delimiter+str(seq)
start_time = time.time()
print ("Request started at: " + str(datetime.datetime.utcnow()))
clientSocket.sendto(data_to_send.encode('UTF-8'),(serverName, serverPort))
print(data_to_send)
seq += 1
while 1:
    data, clientAddress = clientSocket.recvfrom(2048)
    received_data=data.decode("UTF-8").split(delimiter)  # [message checksum seq] or  [(TRUE or FALSE)  seq]

    if len(received_data) == 2:  # ack not message -->[(TRUE or FALSE)  seq]
        print("difference : "+str(time.time()-start_time))
        if received_data[0] == "TRUE" and time.time()-start_time<timeOut:  # receive message
            # data, clientAddress = clientSocket.recvfrom(2048)
            isSafeDataReceived=True
            print("RECEIVED :  seq " + received_data[1])
            start_time = time.time()
            print("start time changed to : "+ str(datetime.datetime.utcnow()))
        elif received_data[0] == "FALSE" and time.time()-start_time < timeOut:
            # resend data --->something went wrong
            print("Something went wrong , resend pckt")
            calcualated_message = test_random_cases(message)  # to check when fake data  sent randomly later add when we drop the message to test time out
            data_to_send = calcualated_message + delimiter + str(calc_checksum(message)) + delimiter + str(seq)
            clientSocket.sendto(data_to_send.encode('UTF-8'),(serverName, serverPort))

        elif time.time()-start_time > timeOut:
            print("TimeOut reached , resend pckt.....")
            start_time = time.time()
            calcualated_message = test_random_cases( message)  # to check when fake data  sent randomly later add when we drop the message to test time out
            data_to_send = calcualated_message + delimiter + str(calc_checksum(message)) + delimiter + str(seq)
            clientSocket.sendto(data_to_send.encode('UTF-8'), (serverName, serverPort))

    elif len(received_data) == 3 and isSafeDataReceived :  # data not ack and true ack received
        print("RECEIVED DATA : "+received_data[0])
        break
    #time.sleep(2)


#clientSocket.close()
message=input('Press enter to exit')
