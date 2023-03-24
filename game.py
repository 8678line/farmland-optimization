import pygame 
import numpy as np
pygame.init()
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 15)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dimension = 10
tile_size = 40
num_crops = 3
cur_tile_no = 0
money = 1000
colours = [(255,0,0),(0,255,0),(0,0,255)]
def init_game():
    screen.fill("white")
    pos_text = font.render('Position: ', True, (0,0,0))
    N_text = font.render('N(g): ', True, (0,0,0))
    P_text = font.render('P(g): ', True, (0,0,0))
    K_text = font.render('K(g): ', True, (0,0,0))
    pH_text = font.render('pH: ', True, (0,0,0))
    for i in range(dimension):
        for j in range(dimension):
            pH_val = np.random.randint(5,8)
            tiles.append(Tile(j,i,i+j,pH_val,i,j,False,True))
            pygame.draw.rect(screen, (150,75,0),(i*tile_size,j*tile_size,tile_size,tile_size))
            pygame.draw.line(screen, (255,255,255), (i*tile_size,j*tile_size), (i*tile_size + dimension*tile_size,j*tile_size))
            pygame.draw.line(screen, (255,255,255), (i*tile_size,j*tile_size), (i*tile_size,j*tile_size + dimension*tile_size))
    pygame.draw.rect(screen, (0,0,0), (tile_size*dimension+1,0, 150,120),3)#Tile box
    pygame.draw.rect(screen, (0,0,0), (tile_size*dimension+151,0, 350,10+num_crops*40),3)#Shop box
    screen.blit(pos_text, (tile_size*dimension+10,10))
    screen.blit(N_text, (tile_size*dimension+10,30))
    screen.blit(P_text, (tile_size*dimension+10,50))
    screen.blit(K_text, (tile_size*dimension+10,70))
    screen.blit(pH_text, (tile_size*dimension+10,90))
    text = font.render('Money:'+str(money),True,(0,0,0))
    screen.blit(text, (400,150)) 
    for i in range(num_crops):
        text = font.render(crops[i].name,True,colours[i])
        screen.blit(text, (tile_size*dimension+161,10+i*40))
        string = str('Price:'+str(crops[i].price)+' Sale:'+str(crops[i].sale)+' N:'+str(crops[i].N)+
        ' P:'+str(crops[i].P)+' K:'+str(crops[i].K))
        text = font.render(string, True,(0,0,0))
        screen.blit(text, (tile_size*dimension+161,30+i*40))
        pygame.draw.line(screen,(0,0,0),(tile_size*dimension+151,45+i*40),(tile_size*dimension+501,45+i*40))
    pygame.draw.rect(screen, (0,0,0), (tile_size*dimension+1,200,50,50),3)
    flush_text = font.render('Flush',True,(0,0,0))
    screen.blit(flush_text,(tile_size*dimension+6,220))
class Tile:
    def __init__(self, N, P, K, pH, x, y, isPressed, isEmpty):
        self.N = N
        self.P = P
        self.K = K
        self.pH = pH
        self.x = x
        self.y = y
        self.isPressed = isPressed
        self.isEmpty = isEmpty


    def ispH(self):
        if self.pH <= 7 and self.pH >= 6:
            return True
        return False
    
    def flood(self):
        self.N = self.N//3
        self.P = self.P//3
        self.K = self.K//3
        self.pH = 7

class Crop:
    def __init__(self, name, N, P, K, price, sale):
        self.name = name
        self.N = N
        self.P = P
        self.K = K
        self.price = price
        self.sale = sale

Crop_A = Crop('A',1,1,1,1,3)
Crop_B = Crop('B',3,3,3,10,15)
Crop_C = Crop('C',5,5,5,30,50)
crops = []
crops.append(Crop_A)
crops.append(Crop_B)
crops.append(Crop_C)
tiles = []
#MAIN GAME LOOP
init_game()
while running:
    #print(tiles[cur_tile_no].x,tiles[cur_tile_no].y)
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    #print(mouse_x,mouse_y)
    tile_x = mouse_x//tile_size
    tile_y = mouse_y//tile_size
    for event in pygame.event.get():
        #print(event.type)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tile_x >= 0 and tile_x < dimension and tile_y >= 0 and tile_y < dimension:#if a tile is clicked
                tiles[cur_tile_no].isPressed = False
                pygame.draw.rect(screen, (255,255,255), (tile_size*dimension+48,30, 95,60))#whiten previous values
                pygame.draw.rect(screen, (255,255,255), (tile_size*dimension+38,90, 105,20))#whiten previous values
                pygame.draw.rect(screen, (255,255,255), (tile_size*dimension+83,10, 65,20))#whiten previous values
                tile_no = tile_y+dimension*tile_x
                cur_tile_no = tile_no
                tiles[tile_no].isPressed = True
                text = font.render('X:'+str(tiles[tile_no].x)+' Y:'+str(tiles[tile_no].y),True,(0,0,0))
                screen.blit(text, (tile_size*dimension+83,10, 60,20))
                text = font.render(str(tiles[tile_no].N),True,(0,0,0))
                screen.blit(text, (tile_size*dimension+48,30, 95,60))
                text = font.render(str(tiles[tile_no].P),True,(0,0,0))
                screen.blit(text, (tile_size*dimension+48,50, 95,60))
                text = font.render(str(tiles[tile_no].K),True,(0,0,0))
                screen.blit(text, (tile_size*dimension+48,70, 95,60))
                string = str(tiles[tile_no].ispH())
                text = font.render(string,True,(0,0,0))
                screen.blit(text, (tile_size*dimension+38,90, 105,20))
            if mouse_x >= 555 and mouse_x <= 900:
                if mouse_y >= 0 and mouse_y <= 45:
                    if money >= crops[0].price and tiles[cur_tile_no].K >= crops[0].K and tiles[cur_tile_no].N >= crops[0].N and tiles[cur_tile_no].P >= crops[0].P and tiles[cur_tile_no].isEmpty and tiles[cur_tile_no].ispH():
                        tiles[cur_tile_no].isEmpty = False
                        pygame.draw.rect(screen,colours[0],(tiles[cur_tile_no].x*tile_size,tiles[cur_tile_no].y*tile_size,tile_size,tile_size))
                        money -= crops[0].price
                        pygame.draw.rect(screen,(255,255,255),(400,150,200,15))
                        text = font.render('Money:'+str(money),True,(0,0,0))
                        screen.blit(text, (400,150)) 
                if mouse_y >= 46 and mouse_y <= 85:
                    if money >= crops[1].price and tiles[cur_tile_no].K >= crops[1].K and tiles[cur_tile_no].N >= crops[1].N and tiles[cur_tile_no].P >= crops[1].P and tiles[cur_tile_no].isEmpty and tiles[cur_tile_no].ispH():
                        tiles[cur_tile_no].isEmpty = False
                        pygame.draw.rect(screen,colours[1],(tiles[cur_tile_no].x*tile_size,tiles[cur_tile_no].y*tile_size,tile_size,tile_size)) 
                        money -= crops[1].price
                        pygame.draw.rect(screen,(255,255,255),(400,150,200,15))
                        text = font.render('Money:'+str(money),True,(0,0,0))
                        screen.blit(text, (400,150)) 
                if mouse_y >= 86 and mouse_y <= 125:
                    if money >= crops[2].price and tiles[cur_tile_no].K >= crops[2].K and tiles[cur_tile_no].N >= crops[2].N and tiles[cur_tile_no].P >= crops[2].P and tiles[cur_tile_no].isEmpty and tiles[cur_tile_no].ispH():
                        tiles[cur_tile_no].isEmpty = False
                        pygame.draw.rect(screen,colours[2],(tiles[cur_tile_no].x*tile_size,tiles[cur_tile_no].y*tile_size,tile_size,tile_size)) 
                        money -= crops[2].price  
                        pygame.draw.rect(screen,(255,255,255),(400,150,200,15))
                        text = font.render('Money:'+str(money),True,(0,0,0))
                        screen.blit(text, (400,150))   
            if mouse_x >= 400 and mouse_x <= 450:
                if mouse_y >= 200 and mouse_y <= 250:
                    tiles[cur_tile_no].flood()    
                    pygame.draw.rect(screen, (255,255,255), (tile_size*dimension+48,30, 95,60))#whiten previous values
                    pygame.draw.rect(screen, (255,255,255), (tile_size*dimension+38,90, 105,20))#whiten previous values
                    pygame.draw.rect(screen, (255,255,255), (tile_size*dimension+83,10, 65,20))#whiten previous values
                    text = font.render('X:'+str(tiles[tile_no].x)+' Y:'+str(tiles[tile_no].y),True,(0,0,0))
                    screen.blit(text, (tile_size*dimension+83,10, 60,20))
                    text = font.render(str(tiles[tile_no].N),True,(0,0,0))
                    screen.blit(text, (tile_size*dimension+48,30, 95,60))
                    text = font.render(str(tiles[tile_no].P),True,(0,0,0))
                    screen.blit(text, (tile_size*dimension+48,50, 95,60))
                    text = font.render(str(tiles[tile_no].K),True,(0,0,0))
                    screen.blit(text, (tile_size*dimension+48,70, 95,60))
                    string = str(tiles[tile_no].ispH())
                    text = font.render(string,True,(0,0,0))
                    screen.blit(text, (tile_size*dimension+38,90, 105,20))


    #print(mouse_x,mouse_y)
    #isPressed = pygame.mouse.get_pressed()[0]
    #if isPressed:
        


    #print(pygame.mouse.get_pos()[0]//tile_size,pygame.mouse.get_pos()[1]//tile_size)
    #print(pygame.mouse.get_pressed()[0])
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()




