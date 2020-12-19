import pygame
import math
field=dict(
    field_dims=[105,74], #m
    player_thrust=30, #m/s^2
    player_mass=1E6, #kg
    ball_mass=5E6 #kg
    )


class Sprite:
    def __init__(self,scale,mass=0,color=pygame.Color(255,255,255),size=2,v=[0,0],a=[0,0],pos=[0,0]):
        self.scale=scale
        self.size=size #m
        self.mass=mass
        self.a=a #m/s^2
        self.v=v #m/s
        self.pos=pos #m
        self.old_rect=None
        px_size=scale*size
        self.px_size=px_size
        surf=pygame.Surface((px_size*1.5,px_size*1.5)).convert()
        pygame.draw.circle(surf,color,[px_size*.75]*2,px_size*.5)
        self.surf=surf
        self.old_rect=None

    def blit(self,display,background):
        #erase old image
        if self.old_rect:
            display.blit(background,self.old_rect,self.old_rect)
            #display.blit(background,[0,0])
        #calculate position to draw on to display
        px_posx=self.pos[0]*self.scale
        px_posy=self.pos[1]*self.scale
        cornerx=px_posx-self.px_size*.75
        cornery=px_posy-self.px_size*.75
        self.old_rect=display.blit(self.surf,[round(cornerx),round(cornery)])

    def dist(self,sprite):
        return math.sqrt((self.pos[0]-sprite.pos[0])**2+(self.pos[1]-sprite.pos[1])**2)
    def direction_to(self,sprite):
        xx=sprite.pos[0]-self.pos[0]
        xy=sprite.pos[1]-self.pos[1]
        return math.atan2(xy,xx)
class Planet(Sprite):
    def get_acceleration(self,ship):
        magnitude=(6.674E-11)*self.mass/(self.dist(ship)**2)
        direction=ship.direction_to(self)
        return [magnitude*math.cos(direction),magnitude*math.sin(direction)]

class Ship(Sprite):
    thrust=[0,0]
    def update_pos(self,timestep,planets):
        all_grav=[p.get_acceleration(self) for p in planets]
        gx=sum([g[0] for g in all_grav])
        gy=sum([g[1] for g in all_grav])
        self.a=[self.thrust[0]+gx,self.thrust[1]+gy]

        posx,posy=self.pos
        vx,vy=self.v
        vx=vx+self.a[0]*timestep
        vy=vy+self.a[1]*timestep
        self.v=[vx,vy]
        posx=posx+self.v[0]*timestep
        posy=posy+self.v[1]*timestep
        self.pos=[posx,posy]
