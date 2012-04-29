"""Runs a Reversi wrapper in the console to launch a 1P or 2P game."""

# CIS-192: Python Programming
# Spring 2012
# Final Project: Reversi
# Kristen Lau, Jay Paik, Paul Terwilliger
#
# Required modules: pygame, numpy
# Included module: textrect

import sys
import reversi_server
import reversi_client
import reversi_single
import time
from multiprocessing import Process
import pygame
import socket

DARK_OLIVE_GREEN = (85, 107, 47)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
NAVAJO_WHITE = (238, 207, 161)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():
    """Ask the user to choose between 1P and 2P and run the game."""
    print "Welcome to Reversi!"
    print "Would you like to play against a computer or another player?"
    print "Enter 1 for 1P, 2 for 2P"
    game_type = raw_input('Choice: ')
    choices = ('1', '2')
    while game_type not in choices:
        print "I'm sorry, but I did not recognize your choice. \
Please try again."
        game_type = raw_input('Choice: ')
    if game_type == '1':
        one_player()
    elif game_type == '2':
        print "Would you like to host a game or join an existing game?"
        print "Enter 1 to host, 2 to join"
        host_or_join = raw_input('Choice: ')
        while host_or_join not in choices:
            print "I'm sorry, but I did not recognize your choice. \
Please try again."
            host_or_join = raw_input('Choice: ')
        if host_or_join == '1':
            addr = socket.gethostbyname(socket.gethostname())
            # Uncomment below to test on localhost
            # addr = 'localhost'
            two_player_host(addr, 31513)
        elif host_or_join == '2':
            print "Enter the IP address of the host (blank for localhost)"
            ip = raw_input('IP: ')
            if ip == '':
                ip = 'localhost'
            two_player_client(ip, 31513)

def one_player():
    """Run a new single player game."""
    reversi_single.new_game()

def two_player_host(address, port):
    """Run the server and client to host a 2-player game."""
    server1 = Process(target=reversi_server.new_server, args=(address, port))
    server1.start()
    client1 = Process(target=reversi_client.new_client, args=(address, port))
    client1.start()
    client1.join()
    server1.join()

def two_player_client(address, port):
    """Run the client to join a 2-player game."""
    reversi_client.new_client(address, port)
    
if __name__ == '__main__':
    main()
