import pygame

from PodSixNet.Connection import connection, ConnectionListener

pygame.init()


#COLORS
DARK_OLIVE_GREEN = (85, 107, 47)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        
        self.screen = pygame.display.set_mode((640, 640))
        
        self.num = None
        
        self.ready = False
        
        self.start = False
        
        self.font = pygame.font.SysFont('sans,freesans,courier,arial', 18, True)
        
        self.points = [0, 0]
        
        self.movement = [0, 0]
        self.color = None
    
    def Network_move(self, data):
        self.movement[data['player']] = data['pos']
        
    def Network_number(self, data):
        self.num = data['num']
    
    def Network_ready(self, data):
        self.ready = not self.ready
        if self.num == 0:
            self.color = BLACK
        else:
            self.color = WHITE
    
    def Network_points(self, data):
        self.points[0] = data[0]
        self.points[1] = data[1]
        
    def Network_start(self, data):
        self.ready = False
        self.start = True
    
    def Loop(self):
        while True:
            connection.Pump()
            self.Pump()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif self.start:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print event.pos
                        print self.num
                        self.movement[self.num] = event.pos
                        #pygame.draw.circle(self.screen, WHITE, event.pos, 40)
                        connection.Send({'action': 'move', 'player': self.num, 'pos': self.movement[self.num]})
                        
            if self.start:
            	if self.movement[0] != 0:
            	    #print self.movement
            	    pygame.draw.circle(self.screen, BLACK, self.movement[0], 40)
            	if self.movement[1] != 0:
            	    #print self.movement
            	    pygame.draw.circle(self.screen, WHITE, self.movement[1], 40)
            	
            	pygame.display.flip()

            if self.ready:
                self.screen.fill(DARK_OLIVE_GREEN)
                self.screen.blit(self.font.render('Ready', True, (0, 0, 255)), (320-self.font.size('Ready')[0]/2, 290))
                pygame.display.flip()
                self.screen.fill(DARK_OLIVE_GREEN)
            elif not self.start:
                self.screen.fill(DARK_OLIVE_GREEN)
                self.screen.blit(self.font.render('Waiting for players...', True, (255, 255, 255)), (320-self.font.size('Waiting for players...')[0]/2, 320))
                pygame.display.flip()
                
                
            pygame.time.wait(25)

print 'Enter the server IP address'
print 'Empty for localhost'
# ask the server IP address
# server = raw_input('Server IP: ')
# control if server is empty
#if server == '':
#	server = 'localhost'

# init the listener
#client = Client(server, 31500)
client = Client('localhost', 31500)
# start the mainloop
client.Loop()
