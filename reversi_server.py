"""Runs the client and connects to the provided host and port."""

# CIS-192: Python Programming
# Spring 2012
# Final Project: Reversi
# Kristen Lau, Jay Paik, Paul Terwilliger
#
# Required modules: pygame, numpy
# Included module: textrect

import sys
import pygame
import socket
import time

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

class ClientChannel(Channel):
    """A class representing the client channel."""
    
    def __init__(self, *args, **kwargs):
        """Initialize."""
        Channel.__init__(self, *args, **kwargs)
    
    def Close(self):
        """Delete the disconnected player from the server."""
        self._server.DelPlayer(self)
    
    def Network_move(self, data):
        """Send the move data to all players."""
        self._server.SendToAll(data)
    
    def Network_turn(self, data):
        """Send the turn data to all players."""
        self._server.SendToAll(data)
        
    def Network_reset(self, data):
        """Reset the clients and server."""
        self._server.SendToAll(data)
        self._server.replay()


class ReversiServer(Server):
    """A class representing the server."""
    
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        """Initialize the server."""
        Server.__init__(self, *args, **kwargs)
        
        self.start = False
        self.wait_to_start = -1
        self.quit = 0
        self.host = None
        self.players = []
        
        self.address, self.port = kwargs['localaddr']
        print "Server started at", self.address, "at port", str(self.port)
    
    def DelPlayer(self, player):
        """Remove a player from the server."""
        if player in self.players:
            print "Removing Player" + str(player.addr)
            self.players.remove(player)
        
        if self.host not in self.players:
            self.quit = 1
        elif len(self.players) == 1 and self.host in self.players:
            self.SendToAll({'action': 'reset',
                            'message': "Your opponent has left the game!"})
    
    def Connected(self, player, addr):
        """Handle client connections to the server."""
        if len(self.players) == 2:
            player.Send({'action': 'quit',
                         'message': "There are already two players in \
that game."})
        else:
            print "Player connected at", addr[0], "at port", addr[1]
        
            self.players.append(player)
        
            if not self.host:
                self.host = player
        
            player.Send({'action': 'number', 'num': len(self.players)})
        
            if len(self.players) == 2:
               self.SendToAll({'action': 'ready'})
               self.wait_to_start = 3000
    
    def replay(self):
        """Reset the game to replay."""
        if len(self.players) == 2:
            self.SendToAll({'action': 'ready'})
            self.wait_to_start = 3000
        
    def SendToAll(self, data):
        """Send data to all players."""
        [p.Send(data) for p in self.players]
    
    def Loop(self):
        """Main server loop."""
        try:
            while True:
            
                self.Pump() # Update data
                
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


def new_server(address, port):
    """Start a new server."""
    reversi_server = ReversiServer(localaddr=(address, port))
    reversi_server.Loop()

