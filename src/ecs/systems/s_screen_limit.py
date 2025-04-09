import esper
import pygame


from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_screen_limit(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagPlayer)
    
    c_t:CTransform
    c_v:CVelocity
    c_s:CSurface
    
    for entity, (c_t, c_v, c_s, c_p) in components:
        cuad_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        # Límite izquierdo
        if cuad_rect.left < 0:
            c_t.pos.x = 0
            c_v.vel.x = 0
        # Límite derecho
        elif cuad_rect.right > screen_rect.width:
            c_t.pos.x = screen_rect.width - cuad_rect.width
            c_v.vel.x = 0
        # Límite superior
        if cuad_rect.top < 0:
            c_t.pos.y = 0
            c_v.vel.y = 0
        # Límite inferior
        elif cuad_rect.bottom > screen_rect.height:
            c_t.pos.y = screen_rect.height - cuad_rect.height
            c_v.vel.y = 0