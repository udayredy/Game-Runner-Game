import pygame
from random import randint,choice
from sys import exit

pygame.init()
pygame.display.set_caption("Runner")

screen = pygame.display.set_mode((800,400),pygame.RESIZABLE)
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1=pygame.image.load("graphics\player\player_walk_1.png").convert_alpha()
        player_walk_2=pygame.image.load("graphics\player\player_walk_2.png").convert_alpha()
        self.player=[player_walk_1,player_walk_2]
        self.player_index=0
        self.player_jump=pygame.image.load("graphics\player\jump.png")
        self.image=self.player[self.player_index]
        self.rect=self.image.get_rect(midbottom=(80,300))
        self.gravity=0

    def player_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=300:
            self.gravity=-20
            jump_music.play()
        if keys[pygame.K_RIGHT]:
            self.rect.x+=5
        if keys[pygame.K_LEFT]:
            self.rect.x-=5
    
    def animation(self):
        if self.rect.bottom > 300:
            self.image=self.player_jump
        else:
            self.player_index+=0.1
            if self.player_index>=len(self.player):
                self.player_index=0
            self.image=self.player[int(self.player_index)]        
    def apply_gravity(self):
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom=300
        if self.rect.left<=0:
            self.rect.left=0
        if self.rect.right>=800:
            self.rect.left=0
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
            
class obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type=='fly':
            fly1=pygame.image.load("graphics\Fly\Fly1.png").convert_alpha()
            fly2=pygame.image.load("graphics\Fly\Fly2.png").convert_alpha()
            self.frames=[fly1,fly2]
            ypos=210
        else:
            snail_1=pygame.image.load("graphics\snail\snail1.png").convert_alpha()
            snail_2=pygame.image.load("graphics\snail\snail2.png").convert_alpha()
            self.frames=[snail_1,snail_2]
            ypos=300
        self.animation_index=0
        self.image=self.frames[self.animation_index]
        self.rect=self.image.get_rect(midbottom=(randint(900,1200),ypos))
    
    def animation(self):
        self.animation_index+=0.1
        if self.animation_index >= len(self.frames):
            self.animation_index=0
        self.image=self.frames[int(self.animation_index)]
            
    def update(self):
        self.animation()
        self.rect.x-=5
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

#Collsion
def collision_sprite():
    if pygame.sprite.spritecollide(player1.sprite,obstacles,False):
        obstacles.empty()
        return False
    else:
        return True
    
game_active=False
#Static Files
sky=pygame.image.load("graphics\sky.png").convert()
ground=pygame.image.load("graphics\ground.png").convert()

player1=pygame.sprite.GroupSingle()
player1.add(Player())

obstacles=pygame.sprite.Group()
obstacle_list=[]
#player
player_gravity=0
player_stand=pygame.image.load("graphics\player\player_stand.png").convert_alpha()
player_stand=pygame.transform.rotozoom(player_stand,0,2)
player_stand_rec=player_stand.get_rect(center=(400,200))
game_font=pygame.font.Font('font\Pixeltype.ttf',50)

#Score
score=0
def display_score(score):
            rendered_score = game_font.render(f'{int(score)}', False, (111, 196, 169))
            screen.blit(rendered_score, (10, 10))

intro_name = game_font.render('Game Runner', False, (111, 196, 169))
intro_name_rect=intro_name.get_rect(center=(400,70))
again = game_font.render('Press Space to run again', False, (111, 196, 169))
again_rect=again.get_rect(center=(400,350))

#Custom Timers
obtimer=pygame.USEREVENT+1
pygame.time.set_timer(obtimer,1000)
jump_music=pygame.mixer.Sound('audio/jump.mp3')
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type==obtimer:
                obstacles.add(obstacle(choice(['fly','snail'])))
        else:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    game_active=True
                    score=0
            
    if game_active:
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,300))
        player1.update()
        player1.draw(screen)
        obstacles.draw(screen)
        obstacles.update()
        score+=1/10
        display_score(score)
        game_active=collision_sprite()
    else:
        obstacle_list.clear()
        screen.fill((94,129,162)) 
        screen.blit(player_stand,player_stand_rec)
        screen.blit(intro_name,intro_name_rect)
        player_gravity=0
        intro_score = game_font.render(f'Your Score:{int(score)}', False, (111, 196, 169))
        intro_score_rect=intro_score.get_rect(center=(400,350))
        if score==0:
            screen.blit(again,again_rect)
        else:
            screen.blit(intro_score,intro_score_rect)
        

    pygame.display.update()
    clock.tick(60)