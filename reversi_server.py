import pygame

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.points = 0
        
    def Network_move(self, data):
        self._server.SendToAll(data)
        pass
        
class ReversiServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        
        self.start = False
        self.wait_to_start = -1
        
        self.players = []
        
        address, port = kwargs['localaddr']
        print "Server started at", address, "at port", str(port)
        print "Now you can start the clients"
    
    def Connected(self, player, addr):
        print "Player connected at", addr[0], "at port", addr[1]
        
        self.players.append(player)
        player.Send({'action': 'number', 'num': len(self.players)-1})
        
        if len(self.players) == 2:
           self.SendToAll({'action': 'ready'})
           self.wait_to_start = 3000
        
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]
    
    def Loop(self):
        while True:
            reversi_server.Pump()
            
            if self.start:
                pass
            
            pygame.time.wait(25)
            
            if self.wait_to_start > 0:
                self.wait_to_start -= 25
            elif self.wait_to_start == 0:
                self.start = True
                self.wait_to_start = -1
                print "starting game"
                self.SendToAll({'action': 'start'})

print 'Enter the IP address of the server.'
print 'Example: localhost or 192.168.0.2'
print 'Empty for localhost'

#address = raw_input('Server IP: ')

# control if adresse is empty
#if address == '':
#	address = 'localhost'

# inizialize the server
#reversi_server = ReversiServer(localaddr=(address, 31500))
reversi_server = ReversiServer(localaddr=('localhost', 31500))
# start mainloop
reversi_server.Loop()
