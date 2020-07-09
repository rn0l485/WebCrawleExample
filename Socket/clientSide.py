import socket,json

class client(object):
    def __init__(self, IP):
        self.get_connect(IP)

    def get_connect(self, IP):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((IP, 1234))   
 
    def send(self, msg):
        self.s.send(msg.encode('utf-8'))

    def get_recieve(self):
        data = self.s.recv(1024)   
        return data

if __name__ =='__main__':
    IP = input('IP: ')
    clientSide = client(IP)
    while True :
        searching = input('The account: ')
        if not searching:
            print ('You have to type something!')
        else:
            if searching == 'exit':
                break
            clientSide.send(searching)
            data = clientSide.get_recieve()
            if data == b'connection fail':
                clientSide = client(IP)
                print ('Sorry the account not exist')
            else:
                print('Data form: name, account, email, follower, address, phone')
                print (data)



