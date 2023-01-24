import pygame

class button():
    def __init__(self,x,y,height,width,color,text = ''):
        self.x = x
        self.y = y
        self.height = height 
        self.width = width
        self.color = color
        self.text = text

    def draw(self,screen,outline=None):
        if outline is not None:
            pygame.draw.rect(screen,outline,[self.x-2,self.y-2,self.width-4,self.height-4])

        pygame.draw.rect(screen,self.color,[self.x,self.y,self.width,self.height])

        if self.text != '':
            font = pygame.font.Font("Press_Start_2P/PressStart2P-Regular.ttf", 10)
            text = font.render(self.text, 1, (255,255,255))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        

    def isOver(self,pos):
        if self.x <= pos[0] <= self.x+self.width and self.y <= pos[1] <= self.y+self.height: 
           return True
        return False
