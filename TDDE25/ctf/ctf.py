import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import sound
import sys
import math

#----- Initialisation -----#
#-- Initialise the display
pygame.init()
pygame.display.set_mode()
pygame.mixer.init()

#-- Initialise the clock
clock = pygame.time.Clock()

#-- Initialise the physics engine
space = pymunk.Space()
space.gravity = (0.0,  0.0)
space.damping = 0.1 # Adds friction to the ground for all objects


#-- Import from the ctf framework
import ai
import images
import gameobjects
import maps


#-- Copy the grass tile all over the level area
def create_grass_tile(current_map, background):
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # The call to the function "blit" will copy the image
            # contained in "images.grass" into the "background"
            # image at the coordinates given as the second argument
            background.blit(images.grass,  (x*images.TILE_SIZE, y*images.TILE_SIZE))

#-- Creates boxes on the map
def create_boxes(current_map, game_objects_list):
#-- Create the boxes
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
        # Get the type of boxes
            box_type = current_map.boxAt(x, y)
        # If the box type is not 0 (aka grass tile), create a box
            if(box_type != 0):
            # Create a "Box" using the box_type, aswell as the x,y coordinates,
            # and the pymunk space
                box = gameobjects.get_box_with_type(x, y, box_type, space)
                game_objects_list.append(box)

#-- Create the tanks
def create_tanks(current_map, tanks_list):
    for i in range(0, len(current_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = current_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space)
        # Add the tank to the list of tanks
        tanks_list.append(tank)
        
#-- Creates the bases
def create_bases(current_map, game_objects_list):
    for i in range(0, len(current_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = current_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        base = gameobjects.GameVisibleObject(pos[0], pos[1], images.bases[i])
        # Add the tank to the list of tanks
        game_objects_list.append(base)

#-- Create the flag
def create_flag(current_map, game_objects_list):
    global flag
    flag = gameobjects.Flag(current_map.flag_position[0], current_map.flag_position[1])
    game_objects_list.append(flag)

#-- Create the borders of the map
def create_border(current_map):
    static_body = space.static_body
    static_lines = [pymunk.Segment(static_body, (0.0, 0.0), (0.0, current_map.height), 0.05)
    ,pymunk.Segment(static_body, (0.0, current_map.height), (current_map.width, current_map.height), 0.05)
    ,pymunk.Segment(static_body, (current_map.width, current_map.height), (current_map.width, 0.0), 0.05)
    ,pymunk.Segment(static_body, (current_map.width, 0.0), (0.0, 0.0), 0.05)
    ]

    space.add(static_lines)

#-- Creates ai tanks
def create_ai_tanks(current_map, tanks_list, game_objects_list, ai_list, multi_check = 1):
    
    for i in range(multi_check, len(current_map.start_positions)):
        ai_tank = ai.Ai(tanks_list[i], game_objects_list,tanks_list, space, current_map)
        ai_list.append(ai_tank)

#-- Plays the game with fog of war enabled
def fog_of_war(FOG_OF_WAR, tanks_list, screen, multiplayer):
    if FOG_OF_WAR:
        if multiplayer:
            holes_in_fog = [tanks_list[0], tanks_list[1]]
        else:
            holes_in_fog = [tanks_list[0]]
        
        fog = pygame.Surface((1200,1200), SRCALPHA)
        fog.fill("black")
        for tank in holes_in_fog:
            pygame.draw.circle(fog, (255,255,255,0), (tank.body.position.x * images.TILE_SIZE, tank.body.position.y * images.TILE_SIZE), 80)
            pygame.draw.circle(fog, (255,255,255,20), (tank.body.position.x * images.TILE_SIZE, tank.body.position.y * images.TILE_SIZE), 70)
        screen.blit(fog,(0,0))

#-- Creates healthbars for each tank
def health_bar(tanks_list, screen):
    health_list = []
    #color
    

    for tank in tanks_list:
        redness = (tank.base_hp - tank.hp) / tank.base_hp
        greeness = tank.hp / tank.base_hp
        hp_frac = tank.hp / tank.base_hp
        
        health_x = tank.body.position[0]*images.TILE_SIZE
        health_y = tank.body.position[1]*images.TILE_SIZE
        
        health_list.append(pygame.draw.rect(screen, (255 * redness, 255 * greeness, 0), (health_x -15, health_y + 15, 30 * hp_frac, 7)))
        
#  Main Game
def play_game():


    #-- Constants
    FRAMERATE = 50

    #-- Variables
    #   Define the current level
    current_map         = maps.map0
    screen = pygame.display.set_mode(current_map.rect().size)

    #   List of all game objects
    game_objects_list   = []
    tanks_list          = []
    ai_list             = []

    FOG_OF_WAR = True
    MULTIPLAYER = True
    ROUND_LIMIT = 5
    ROUND_CHECK = 0
    SCORE_LIMIT = 3
    TIME_LIMIT = 8600
    WINCON = "TIME_LIMIT"

        #-- Control whether the game run
    running = True

    skip_update = 0

    #-- Resize the screen to the size of the current level
    #screen = pygame.display.set_mode(current_map.rect().size)

    #-- Generate the background
    background = pygame.Surface(screen.get_size())


    #  Adds collision types for all objects
    def collision_bullet_tank(arb, space, data):
        tank = arb.shapes[1].parent
        bullet = arb.shapes[0].parent
        bullet_shape = arb.shapes[0]
        
    
        if tank != bullet.tank:

            if tank.hp > 1:
                sound.hit_tank_sound.set_volume(0.1)
                sound.hit_tank_sound.play()
                if tank.spawn_protection > 150:
                    tank.hp -= 1
                    space.remove(bullet_shape, bullet_shape.body)
                    game_objects_list.remove((bullet))
                else:
                    space.remove(bullet_shape, bullet_shape.body)
                    game_objects_list.remove((bullet))
            
            elif tank.hp == 1:
                sound.kill_tank_sound.set_volume(0.1)
                sound.kill_tank_sound.play()
                if flag.is_on_tank:
                    tank.flag = None
                    flag.is_on_tank = False
                expl = gameobjects.Explosion(tank.body.position[0],tank.body.position[1], images.explosion)
                game_objects_list.append(expl)
                tank.body.position = tank.start_position
                space.remove(bullet_shape, bullet_shape.body)
                game_objects_list.remove((bullet))
                tank.hp = tank.base_hp
                tank.spawn_protection = 0
        
        return False

                
    def collision_bullet_woodenbox(arb, space, data):
        woodbox = arb.shapes[1].parent
        woodbox_shape = arb.shapes[1]
        bullet = arb.shapes[0].parent
        bullet_shape = arb.shapes[0]
        if woodbox.hp > 1:
            woodbox.hp -= 1
        elif woodbox.hp == 1:
            space.remove(woodbox_shape, woodbox_shape.body)
            game_objects_list.remove(woodbox)
            expl = gameobjects.Explosion(woodbox.body.position[0], woodbox.body.position[1], images.explosion)
            game_objects_list.append(expl)
        game_objects_list.remove((bullet))
        space.remove(bullet_shape, bullet_shape.body)
        sound.hit_box_sound.set_volume(1)
        sound.hit_box_sound.play()
        return False


    def collision_bullet_static_object(arb, space, data):
        bullet = arb.shapes[0].parent
        bullet_shape = arb.shapes[0]

        space.remove(bullet_shape, bullet_shape.body)
        game_objects_list.remove((bullet))
        return False

    #collision handling
    def collision_handler():
        collision_type = {"Bullet": 1, "Tank": 2, "Woodenbox": 3, "static_object": 4}

        handler_bullet_tank = space.add_collision_handler(collision_type["Bullet"], collision_type["Tank"])
        handler_bullet_woodenbox = space.add_collision_handler(collision_type["Bullet"],collision_type["Woodenbox"])
        handler_bullet_static_object = space.add_collision_handler(collision_type["Bullet"], collision_type["static_object"])

        handler_bullet_woodenbox.pre_solve = collision_bullet_woodenbox
        handler_bullet_tank.pre_solve = collision_bullet_tank
        handler_bullet_static_object.pre_solve = collision_bullet_static_object 


    create_flag(current_map, game_objects_list)
    create_border(current_map)
    create_bases(current_map, game_objects_list)
    create_tanks(current_map, tanks_list)
    create_boxes(current_map, game_objects_list)
    create_grass_tile(current_map, background)
    collision_handler()

    if MULTIPLAYER: 
        create_ai_tanks(current_map, tanks_list, game_objects_list, ai_list, 2)
        player = tanks_list[0] 
        player_2 = tanks_list[1]
    else:
        player = tanks_list[0]
        create_ai_tanks(current_map, tanks_list, game_objects_list, ai_list)


    # Background music
    sound.load_music("fnaf2.wav")

    time = TIME_LIMIT / FRAMERATE
    time_check = 0
    if WINCON == "ROUND_LIMIT":
        print("Round", ROUND_CHECK+1)

    #----- Main Loop -----#
    while running:
        #-- Handle the events
        if WINCON == "TIME_LIMIT":
            time_check +=1
            if time_check == TIME_LIMIT:
                running = False
            if time_check % 50 == 0:
                time -= 1
                print(int(time // 60), ":", int(time % 60), sep= "")

        for event in pygame.event.get():
            # Check if we receive a QUIT event (for instance, if the user press the
            # close button of the wiendow) or if the user press the escape key.
            
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            #ACCELERATE
            if event.type == KEYDOWN and event.key == K_UP:
                player.accelerate()
            if event.type == KEYUP and event.key == K_UP:       
                player.stop_moving()
            #DECELERATE
            if event.type == KEYDOWN and event.key == K_DOWN:
                player.decelerate()
            if event.type == KEYUP and event.key == K_DOWN:
                player.stop_moving()
            #TURN LEFT
            if event.type == KEYDOWN and event.key == K_LEFT:
                player.turn_left()
            if event.type == KEYUP and event.key == K_LEFT:
                player.stop_turning()
            #TURN RIGHT
            if event.type == KEYDOWN and event.key == K_RIGHT:
                player.turn_right()
            if event.type == KEYUP and event.key == K_RIGHT:
                player.stop_turning()
            #SHOOT
            if event.type == KEYDOWN and event.key == K_RETURN:
                if player.cooldown >= 50:
                    player.cooldown = 0
                    game_objects_list.append(player.shoot(space))
                    

    
            #ACCELERATE
            if event.type == KEYDOWN and event.key == K_w:
                player_2.accelerate()
            if event.type == KEYUP and event.key == K_w:       
                player_2.stop_moving()
            #DECELERATE
            if event.type == KEYDOWN and event.key == K_s:
                player_2.decelerate()
            if event.type == KEYUP and event.key == K_s:
                player_2.stop_moving()
            #TURN LEFT
            if event.type == KEYDOWN and event.key == K_a:
                player_2.turn_left()
            if event.type == KEYUP and event.key == K_a: 
                player_2.stop_turning()
            #TURN RIGHT
            if event.type == KEYDOWN and event.key == K_d:
                player_2.turn_right()
            if event.type == KEYUP and event.key == K_d:
                player_2.stop_turning()
            #SHOOT
            if event.type == KEYDOWN and event.key == K_SPACE:
                if player_2.cooldown >= 50:
                    player_2.cooldown = 0
                    game_objects_list.append(player_2.shoot(space))
                    
            
        #calls the Decide function on ai.tanks
        for i in range(0,len(ai_list)):
            ai.Ai.decide(ai_list[i])
                
        #-- Update physics
        if skip_update == 0:
            # Loop over all the game objects and update their speed in function of their
            # acceleration.
            for obj in game_objects_list:
                obj.update()
            skip_update = 2
        else:
            skip_update -= 1

        #   Check collisions and update the objects position
        space.step(1 / FRAMERATE)


        #-- Update Display

        # Display the background on the screen
        screen.blit(background, (0,0))            #(images.main_menu_bg.get_width()/2, images.main_menu_bg.get_height()/2))

        # Updates the display of tanks on screen
        for obj in tanks_list:
            obj.try_grab_flag(flag)
            obj.update()
            obj.update_screen(screen)
            obj.post_update()
            if obj.has_won():
                obj.score += 1
                obj.flag = None
                flag.is_on_tank = False
                k=1
                for tank in tanks_list:
                    print("Player ", k, ": ", tank.score, sep = "")
                    k += 1
                if WINCON == "SCORE_LIMIT":
                    if obj.score == SCORE_LIMIT:
                        running = False
                elif WINCON == "ROUND_LIMIT":
                    ROUND_CHECK += 1
                    if ROUND_CHECK == ROUND_LIMIT:
                        running = False
                        break
                    print("Round", ROUND_CHECK+1)
                #Reset gameboard
                for tank in range(len(tanks_list)):
                    pos = current_map.start_positions[tank]
                    tanks_list[tank].body.position = (pos[0], pos[1])
                    tanks_list[tank].body.angle = pos[2] * (180*math.pi)
                    tanks_list[tank].hp = tanks_list[tank].base_hp
                flag.x = current_map.flag_position[0]
                flag.y = current_map.flag_position[1]
                for i in range(100):
                    for obj in game_objects_list:
                        if isinstance(obj, gameobjects.Box):
                            game_objects_list.remove(obj)
                            space.remove(obj.shape)
                create_boxes(current_map, game_objects_list)
                #slut reset gameboard
                
        
        #update health
        health_bar(tanks_list, screen)
        
        #Update the display of game objects on screen 
        for obj in game_objects_list:
            
            obj.update()
            obj.update_screen(screen)
            obj.post_update()  
            if isinstance(obj, gameobjects.Explosion):
                obj.frame += 1
                if obj.frame == 10:
                    obj.frame = obj.base_frame
                    game_objects_list.remove(obj)

        fog_of_war(FOG_OF_WAR, tanks_list, screen, MULTIPLAYER)

        #   Redisplay the entire screen (see double buffer technique)
        pygame.display.flip()

        #   Control the game framerate
        clock.tick(FRAMERATE)

play_game()
