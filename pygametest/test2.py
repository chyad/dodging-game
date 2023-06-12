import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_face_left = pygame.image.load('player.png').convert_alpha()
        player_face_right = pygame.transform.flip(player_face_left, True, False)
        # player_jump = player jump image maybe
        
        self.direction = 0
        self.player_face = [player_face_left, player_face_right]
        self.image = self.player_face[self.direction]
        
        self.rect = self.image.get_rect(midbottom = (200,310))
        self.gravity = 0
        
    def player_input(self):
        keys2 = pygame.KEYDOWN
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 310:
            self.gravity = -20
        if keys[pygame.K_LEFT]:
            self.direction = 0
            self.rect.x -= 5
            if(self.rect.x == 0):
                self.rect.midtop = (400, self.rect.y)
        if keys[pygame.K_RIGHT]:
            self.direction = 1
            self.rect.x += 5
            if(self.rect.x == 800):
                self.rect.midtop = (400, self.rect.y)
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        
        if self.rect.bottom >= 310:
            self.rect.bottom = 310
            
    def animation(self):
        self.image = self.player_face[self.direction]
        '''     # if jump image
        if player_rect.bottom<310:
            player_surf = player_jump[player_direction]
        else:
            player_surf = player_face[player_direction]
        '''
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Drop(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        self.type = type
        if type == 'body':
            player_face_left = pygame.image.load('player.png').convert_alpha()
            player_horizontal = pygame.transform.rotozoom(player_face_left, 90, 1)
            self.frames = [player_face_left,player_horizontal]
            y_pos = 310
        if type == 'body2':
            player_face_left = pygame.image.load('player.png').convert_alpha()
            player_horizontal = pygame.transform.rotozoom(player_face_left, 270, 1)
            self.frames = [player_face_left,player_horizontal]
            y_pos = 310

        self.animation_index = 0
        
        #self.image = self.frames[self.animation_index]
        self.image = player_horizontal
        if type == 'body':
            self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        if type == 'body2':
            self.rect = self.image.get_rect(midbottom = (randint(-300, -100), y_pos))
        
    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if type == 'body' and self.rect.x < -100:
            self.kill()
        if type == 'body2' and self.rect.x > 900:
            self.kill()
            
            
    def update(self):
        #self.animation()
        if self.type == 'body':
            self.rect.x -= 5
        if self.type == 'body2':
            self.rect.x += 5
        self.destroy()
            
def score_display():
    current_time = int((pygame.time.get_ticks() - start_time) /1000)
    score_surf = font.render(f'time awaken: {current_time}s', True, 'Black')
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    
    return current_time
  
def collision():
    if pygame.sprite.spritecollide(player.sprite, drop, True):
        drop.empty()
        return False
    else:
        return True
    

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('game')  #window name
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
game_active = False
start_time=0
score = 0


player = pygame.sprite.GroupSingle()
player.add(Player())

drop = pygame.sprite.Group()



game_name = font.render('zzZ', False, 'Grey')
game_name_rect = game_name.get_rect(center = (400, 50))

game_message = font.render('press r to get up', False, 'Grey')
game_message_rect = game_message.get_rect(center = (400, 100))

sky_surface = pygame.Surface((800,300))
sky_surface.fill((116, 165, 242))

ground_surface = pygame.Surface((800,150))
ground_surface.fill((80, 104, 107))

player_face_left = pygame.image.load('player.png').convert_alpha()
player_killscreen_surf = pygame.transform.rotozoom(player_face_left, 90, 2)
player_killscreen_rect = player_killscreen_surf.get_rect(center = (400,200))

pygame.display.set_icon(player_killscreen_surf)

timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer, 1000)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_active = True
                    start_time = pygame.time.get_ticks()
        
        if event.type == timer and game_active:
            drop.add(Drop(choice(['body','body2'])))

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = score_display()
        
        game_active = collision()

        player.draw(screen)
        player.update()
        
        drop.draw(screen)
        drop.update()

    else:
        screen.fill((116, 165, 242))
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
        
        score_message = font.render(f'you awaked for {score} secnods, good dream', False, 'Grey')
        score_message_rect = score_message.get_rect(center = (400, 350))
        if score:
            screen.blit(score_message, score_message_rect)
        
        screen.blit(player_killscreen_surf, player_killscreen_rect)
        
        
        
    
            
    pygame.display.update()
    
    clock.tick(60)
