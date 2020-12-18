import pygame
field=dict(
    field_dims=[105,74], #m
    player_speed=10, #m/s
    player_mass=1E6, #kg
    ball_mass=5E6 #kg
    )


class Sprite:
    def __init__(self,scale,color=pygame.Color(255,255,255),size=2,v=[0,0],pos=[0,0]):
        self.scale=scale
        self.size=size #m
        self.v=v #m/s
        self.pos=pos #m
        self.grav=0
        self.old_rect=None
        px_size=scale*size
        self.px_size=px_size
        surf=pygame.Surface((px_size*1.5,px_size*1.5)).convert()
        pygame.draw.circle(surf,color,[px_size*.75]*2,px_size*.5)
        self.surf=surf
        self.old_rect=None
    def update_pos(self,timestep):
        posx,posy=self.pos
        posx=posx+self.v[0]*timestep
        posy=posy+self.v[1]*timestep
        self.pos=[posx,posy]
    def blit(self,display,background):
        #erase old image
        if self.old_rect:
            display.blit(background,[0,0],self.old_rect)
            #display.blit(background,[0,0])
        #calculate position to draw on to display
        px_posx=self.pos[0]*self.scale
        px_posy=self.pos[1]*self.scale
        cornerx=px_posx-self.px_size*.75
        cornery=px_posy-self.px_size*.75
        self.old_rect=display.blit(self.surf,[round(cornerx),round(cornery)])
