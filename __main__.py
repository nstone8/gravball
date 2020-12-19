import pygame
import pygame.locals
import math
import time
import sys
import objects as obj
pygame.init()

#initialize display
disp_info=pygame.display.Info()
display_size=[disp_info.current_w,disp_info.current_h]
window_size=[0,0]
display_ar=display_size[0]/display_size[1]
field_dims=obj.field['field_dims']
if field_dims[0]/field_dims[1]>display_ar:
    #window should be trimmed in the y direction
    scale=display_size[0]/field_dims[0] #px/m
    window_size[0]=display_size[0]
    window_size[1]=math.floor(field_dims[1]*scale)
else:
    #window should be trimmed in the x direction
    scale=display_size[1]/field_dims[1] #px/m
    window_size[1]=display_size[1]
    window_size[0]=math.floor(field_dims[0]*scale)

display=pygame.display.set_mode(size=window_size)
planets=[]
planets.append(obj.Planet(scale,mass=1E14,size=10,pos=[20,45]))
planets.append(obj.Planet(scale,mass=1E14,size=10,pos=[80,45]))
for p in planets:
    p.blit(display,display)
background=display.copy()

player=obj.Ship(scale,pos=[15,15])
clock=pygame.time.Clock()
mission_clock=None
while True:
    clock.tick(60) #set max framerate
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            sys.exit()
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_ESCAPE:
                sys.exit()
            if event.key == pygame.locals.K_UP:
                player.thrust[1]=-1*obj.field['player_thrust']
            if event.key == pygame.locals.K_DOWN:
                player.thrust[1]=obj.field['player_thrust']
            if event.key == pygame.locals.K_LEFT:
                player.thrust[0]=-1*obj.field['player_thrust']
            if event.key == pygame.locals.K_RIGHT:
                player.thrust[0]=obj.field['player_thrust']
        elif event.type == pygame.locals.KEYUP:
            if event.key == pygame.locals.K_UP:
                player.thrust[1]=0
            if event.key == pygame.locals.K_DOWN:
                player.thrust[1]=0
            if event.key == pygame.locals.K_LEFT:
                player.thrust[0]=0
            if event.key == pygame.locals.K_RIGHT:
                player.thrust[0]=0
        #redraw everything
    curtime=time.perf_counter()
    if mission_clock:
        step=curtime-mission_clock
    else:
        step=0
    mission_clock=curtime
    player.update_pos(step,planets)
    player.blit(display,background)
    pygame.display.flip()
