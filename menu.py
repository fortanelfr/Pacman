import pygame
from src.constants import *
from src.button import *
import run 
  
  
# initializing the constructor 
pygame.init() 

# opens up a window 
screen = pygame.display.set_mode(SCREENSIZE) 

  
# black color 
color = (BLACK) 
  
# light shade of the button 
color_light = (170,170,170) 
  
# dark shade of the button 
color_dark = (100,100,100) 
  
# stores the width of the 
# screen into a variable 
width = screen.get_width() 
  
# stores the height of the 
# screen into a variable 
height = screen.get_height()

button_width = width/3
button_heigth = height/12

button_x = width/3
button_y = height/12 * 5

start = button(button_x,button_y,button_heigth,button_width,color_dark,text = 'Start Game')
score = button(button_x,button_y + height/12*1.5,button_heigth,button_width,color_dark,text = 'Score')
exit = button(button_x,button_y + height/12*3,button_heigth,button_width,color_dark,text = 'Exit')


  
# defining a font 
smallfont = pygame.font.SysFont('Corbel',35) 
  
# rendering a text written in 
# this font 
text = smallfont.render('Start Game' , True , color)
  
while True: 
      
    for ev in pygame.event.get(): 
          
        if ev.type == pygame.QUIT: 
            pygame.quit() 
              
        #checks if a mouse is clicked 
        if ev.type == pygame.MOUSEBUTTONDOWN: 
              
            #if the mouse is clicked on the 
            # button the game is terminated 
            if start.isOver(mouse):
                game = run.GameController()
                game.startGame()
                while True:
                     game.update()

            if exit.isOver(mouse):
                pygame.quit() 
                
                  
    # fills the screen with a color 
    screen.fill(BLACK) 
      
    # stores the (x,y) coordinates into 
    # the variable as a tuple 
    mouse = pygame.mouse.get_pos() 
      
    # if mouse is hovered on a button it 
    # changes to lighter shade 
    if start.isOver(mouse):
        start.draw(screen,color_light)
          
    else: 
        start.draw(screen)

    if score.isOver(mouse):
        score.draw(screen,color_light)
          
    else: 
        score.draw(screen)

    if exit.isOver(mouse):
        exit.draw(screen,color_light)
          
    else: 
        exit.draw(screen)
      
    # superimposing the text onto our button 
    #screen.blit(text , (button_x + button_width/16,button_y + button_heigth/4))


      
    # updates the frames of the game 
    pygame.display.update() 