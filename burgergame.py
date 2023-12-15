import pygame
import random

pygame.init()

#Set display
window_width = 1000
window_height = 600
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Chicken Dog')
#Set FPS and Clock
FPS = 60
clock = pygame.time.Clock()

#Set Game Values
PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY= 5
PLAYER_BOOST_VELOCITY= 20
STARTING_BOOST_LEVEL = 100
STARTING_CHICKEN_VELOCITY = 3
CHICKEN_ACCELERATION = .5
BUFFER_DISTANCE = 100
score = 0
chicken_points = 0
chicken_eaten = 0

player_lives =PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY
boost_level = STARTING_BOOST_LEVEL

chicken_velocity = STARTING_CHICKEN_VELOCITY


#Set Color
orange = (246,170,54)
black = (0,0,0)
white = (255,255,255)


#Set Fonts
font = pygame.font.Font('Debrosee-ALPnL.ttf',32)
point_text = font.render('Chicken Point: ' + str(chicken_points), True,orange)
points_rect = point_text.get_rect()
points_rect.topleft = (10,10)
score_text = font.render('Score: ' + str(score), True, orange)
score_rect = score_text.get_rect()
score_rect.topleft = (10,50)
title_text = font.render('Chicken Dog', True,orange)
title_rect = title_text.get_rect()
title_rect.centerx = window_width//2
title_rect.y = 10
eaten_text = font.render('Chicken eaten : ' + str(chicken_eaten),True,orange)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = window_width//2
eaten_rect.y = 50

lives_text = font.render('Lives : ' + str(player_lives),True,orange)
lives_rect = lives_text.get_rect()
lives_rect.topright = (window_width-10, 10)
boost_text = font.render('Boost : ' + str(boost_level),True,orange)
boost_rect = boost_text.get_rect()
boost_rect.topright=(window_width-10,50)

game_over = font.render('Final Score : ' + str(score),True,orange)
game_over_rect = game_over.get_rect()
game_over_rect.center = (window_width//2 , window_height//2)
continue_text = font.render("Press any Key to Continue",True,orange)
continue_rect = continue_text.get_rect()
continue_rect.center = (window_width//2,window_height//2+64)

#Set Sound and music
bark_sound = pygame.mixer.Sound('doggot.wav')
miss_sound = pygame.mixer.Sound('dogmiss.wav')
pygame.mixer.music.load('background.wav')

#Set Image
player_image_right = pygame.image.load('Dog_Right.png')
player_image_left = pygame.image.load('Dog_ left.png')
player_image = player_image_left
player_rect = player_image.get_rect()
player_rect.centerx = window_width//2
player_rect.bottom = window_height

chicken_image = pygame.image.load('chicken.png')
chicken_rect = chicken_image.get_rect()
chicken_rect. topleft = (random.randint(0 , window_width-32),-100)
#The main loop
pygame.mixer.music.play(30)
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_image = player_image_left
    if keys[pygame.K_RIGHT] and player_rect.right < window_width:
        player_rect.x += player_velocity
        player_image = player_image_right
    if keys[pygame.K_UP] and player_rect.top > 100:
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < window_height:
        player_rect.y += player_velocity

    #Boost
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = PLAYER_NORMAL_VELOCITY
    #Move the chicken
    chicken_rect.y += chicken_velocity
    chicken_points = int(chicken_velocity * (window_height-chicken_rect.y + 100))
    #player missed the chicken
    if chicken_rect.y > window_height:
        player_lives -=1
        miss_sound.play()
        chicken_rect.topleft = (random.randint(0 , window_width-32),-100)
        chicken_velocity = STARTING_CHICKEN_VELOCITY

        player_rect.centerx = window_width//2
        player_rect.bottom = window_height
        boost_level = STARTING_BOOST_LEVEL

    if player_rect.colliderect(chicken_rect):
        score += chicken_points
        chicken_eaten += 1
        bark_sound.play()
        chicken_rect.topleft = (random.randint(0,window_width - 32),-100)
        chicken_velocity += CHICKEN_ACCELERATION
        boost_level += 25
        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL

        point_text = font.render('Chicken Point: ' + str(chicken_points), True, orange)
        score_text = font.render('Score: ' + str(score), True, orange)
        eaten_text = font.render('Chicken eaten : ' + str(chicken_eaten), True, orange)
        lives_text = font.render('Lives : ' + str(player_lives), True, orange)
        boost_text = font.render('Boost : ' + str(boost_level), True, orange)

        #check the game over
        if player_lives == 0:
            game_over_text = font.render("Final Score" +str(score),True,orange)
            display_surface.blit(game_over_text,game_over_rect)
            display_surface.blit(continue_text,continue_rect)
            pygame.display.update()

            pygame.mixer.music.stop()
            is_pause = True
            while is_pause:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        score =0
                        chicken_eaten = 0
                        player_lives = PLAYER_STARTING_LIVES
                        boost_level = STARTING_BOOST_LEVEL
                        chicken_velocity = STARTING_CHICKEN_VELOCITY
                        pygame.mixer.music.play()
                        is_pause = False
                    if event.type == pygame.QUIT:
                        is_pause =False
                        running = False









    display_surface.fill(black)
    display_surface.blit(point_text, points_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(eaten_text, eaten_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(boost_text, boost_rect)
    pygame.draw.line(display_surface, white, (0, 80), (window_width, 80), 3)
    #Blit
    display_surface.blit(player_image, player_rect)
    display_surface.blit(chicken_image, chicken_rect)
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()

