import sys
import pygame
import socket

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.points = 0
    
    def Close(self):
        self._server.DelPlayer(self)
    
    def Network_move(self, data):
        self._server.SendToAll(data)
    
    def Network_turn(self, data):
        self._server.SendToAll(data)

        
class ReversiServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        
        self.start = False
        self.wait_to_start = -1
        self.quit = 0
        self.host = None
        self.players = []
        
        self.address, self.port = kwargs['localaddr']
        print "Server started at", self.address, "at port", str(self.port)
        print "Now you can start the clients"
    
    def DelPlayer(self, player):
        print "Deleting Player" + str(player.addr)
        self.players.remove(player)
        
        if self.host not in self.players:
            self.quit = 1
    
    def Connected(self, player, addr):
        print "Player connected at", addr[0], "at port", addr[1]
        
        self.players.append(player)
        
        if not self.host:
            self.host = player
        
        player.Send({'action': 'number', 'num': len(self.players)})
        
        if len(self.players) == 2:
           self.SendToAll({'action': 'ready'})
           self.wait_to_start = 3000
        
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]
    
    def Loop(self):
    
        try:
            while True:
            
                self.Pump()
                
                if self.quit:
                    self.close()
                    sys.exit(0)
                
                if self.start:
                    pass
            
                pygame.time.wait(25)
            
                if self.wait_to_start > 0:
                    self.wait_to_start -= 25
                elif self.wait_to_start == 0:
                    self.start = True
                    self.wait_to_start = -1
                    print "Starting Game!"
                    self.SendToAll({'action': 'start'})
            
        except KeyboardInterrupt:
            self.close()
            sys.exit(0)
            
        self.close()
        sys.exit(0)

#print 'Enter the IP address of the server.'
#print 'Example: localhost or 192.168.0.2'
#print 'Empty for localhost'

#address = raw_input('Server IP: ')

# control if adresse is empty
#if address == '':
#	address = 'localhost'

# inizialize the server
#reversi_server = ReversiServer(localaddr=(address, 31500))
######reversi_server = ReversiServer(localaddr=('localhost', 31500))
# start mainloop
######reversi_server.Loop()



def new_server(address, port):
    #address = socket.gethostbyname(socket.gethostname())
    #address = 'localhost'
    reversi_server = ReversiServer(localaddr=(address, port))
    reversi_server.Loop()

