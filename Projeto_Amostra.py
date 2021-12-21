

import pygame
import random
from pygame import display
from pygame.image import load
from pygame.sprite import Sprite, Group, GroupSingle

try:
    pygame.init()
    pygame.font.init()
except:
    print("O módulo pygame não está instalado")

fundo = load("images/space.jpg")
altura = 486
largura = 748
velocidade = 20
white=(255,255,255)
vidas = 20


relogio = pygame.time.Clock()
pontos = 0
score = "SCORE: " + str(pontos)
explosion = pygame.mixer.Sound('sounds/explosion.wav')
laser_som = pygame.mixer.Sound('sounds/laser1.wav')
music = pygame.mixer.music.load('sounds/space.ogg')

win = pygame.mixer.Sound("sounds/win.mp3")
bossound = pygame.mixer.Sound("sounds/boss.ogg")
def texto(msg,cor,tam,x,y):
    font=pygame.font.Font(None,tam)
    texto1 = font.render(msg,True,cor)
    superficie.blit(texto1,[x,y])

superficie = display.set_mode((largura, altura))
superficie.blit(fundo, (0 , 0))
display.set_caption("Space Legacy")
#  Game Over
GAME_OVER = False
#You win
YOU_WIN = False
#BAttle
Battle = False

class Nave(Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = load("images/Nave.png")
        self.right = False
        self.left = False
        self.rect = self.image.get_rect(
            center = (largura / 2, altura - 50 )
            )
        

    def atirar(self):
        self.laser =Laser()
        grupo_laser.add(self.laser)
        laser_som.play()

    def update(self):
        pass
        
class Boss(Sprite):

    def __init__(self):
        super().__init__()
        self.image = load("images/Boss.png")
        self.rect = self.image.get_rect(
            center = (largura/2, - 300)
            )

        

    def update(self):
        global GAME_OVER
        self.rect.y += 1

        if self.rect.y == altura - 300:
            GAME_OVER = True    
            self.kill()
        


        
        
        
class Laser(Sprite):
    def __init__(self):
        super().__init__()
        self.image = load("images/Laser.png")
        self.rect = self.image.get_rect(
            center = (nave.rect.x + 52, nave.rect.y)
        )
        
    def update(self):
        self.rect.y -= 10
        
        if self.rect.y < 50:
            self.kill()
            
            #MISSEIS.pop()
class Nave_Inimiga(Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = load("images/Nave_inimiga.png")
        self.rect = self.image.get_rect(
            center = (random.randint(10, largura - 92), random.randint(-20, 0))
            )
        
    def update(self):
        global GAME_OVER
        self.rect.y += 2
        if pontos > 500 and pontos < 800:
            self.rect.y += 2.2
            velocidade = 22
        if pontos > 800:
            self.rect.y += 2.5
            velocidade = 25
        
        if self.rect.y == 486:
            GAME_OVER = True
            self.kill()
            
            
  
nave_i = Nave_Inimiga()
grupo_inimigo = Group(nave_i)
nave = Nave()
laser = Laser()
boss = Boss()
grupo_laser = Group()
grupo_nave = GroupSingle(nave)
grupo_boss = GroupSingle(boss)
pygame.mixer.music.play(-1)




while True:
    if GAME_OVER:
        while GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        GAME_OVER = False
                        nave = Nave()
                        grupo_nave = GroupSingle(nave)
            superficie.blit(fundo, (0 , 0))
            texto("GAME OVER", white, 100, largura / 4 - 20, altura / 5)
            texto("(C) Continuar", white, 50, largura / 4, (altura / 4) + 80)
            if len(grupo_inimigo) >0:
                for i in grupo_inimigo:
                    grupo_inimigo.remove(i)
            pontos = 0
            display.update()
    if YOU_WIN:
        pygame.mixer.music.stop()
        win.play(-1)
        while YOU_WIN:
            superficie.blit(fundo, (0 , 0))
            texto("You Win", white, 100, largura / 3 - 20, altura / 5)
            texto("(C) Continuar", white, 50, largura / 3, (altura / 4) + 80)
            if len(grupo_inimigo) >0:
                for i in grupo_inimigo:
                    grupo_inimigo.remove(i)
            """if len(grupo_nave) > 0:
                for i in grupo_nave:
                    grupo_nave.remove(i)"""
            pontos = 0
            display.update()        
            
    else:
        superficie.blit(fundo, (0 , 0))
        grupo_nave.draw(superficie)
        if pontos >= 1000:
            grupo_boss.draw(superficie)
            bossound.play()
            grupo_boss.update()
            if len(grupo_inimigo) >0:
                for i in grupo_inimigo:
                    grupo_inimigo.remove(i)
        grupo_inimigo.draw(superficie)
        grupo_laser.draw(superficie)
        if len(grupo_laser) > 0:
            grupo_laser.update()
    
        grupo_inimigo.update()
        texto("Score: " + str(pontos), white, 25, largura - 100, 30)
        
        display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT :
                nave.left = True
            if event.key == pygame.K_RIGHT :
                nave.right = True
            if event.key == pygame.K_SPACE:
                nave.atirar()
                           
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                nave.left = False
            if event.key == pygame.K_RIGHT:
                nave.right = False
    
    if nave.right and nave.rect.x < largura - 92:
        nave.rect.x += velocidade
    if nave.left and nave.rect.x > 10:
        nave.rect.x -= velocidade

        
    if (pygame.sprite.groupcollide(grupo_laser, grupo_inimigo, True, True)):
        pontos += 10
        explosion.play()

    if (pygame.sprite.groupcollide(grupo_nave, grupo_inimigo, True, True)):
        GAME_OVER = True
        explosion.play()
        laser.kill()

    if (pygame.sprite.groupcollide(grupo_nave, grupo_boss, True, True)):
        GAME_OVER = True
        explosion.play()
        laser.kill()

    if (pygame.sprite.groupcollide(grupo_laser, grupo_boss, True, False)):
        if vidas <= 0:
            YOU_WIN = True
            boss.kill()
        vidas -= 1
        bossound.stop()
        explosion.play()
        
        
    



    
    
    if len(grupo_inimigo) <4: # se tiver menos que 5 inimigos , adiciona mais inimigo
        for i in range(5):
            enemy = Nave_Inimiga()
            grupo_inimigo.add(enemy)   
    if len(grupo_boss) < 1:
        chefe = Boss()
        grupo_boss.add(chefe)
            
    
    
    relogio.tick(30)


