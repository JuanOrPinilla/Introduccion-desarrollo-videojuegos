import pygame
import math
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_dash(world: esper.World, player_entity: int, mouse_pos: tuple, delta_time: float):
    c_t = None
    c_v = None
    
    # Buscar al jugador
    for ent, (c_transform, c_velocity, _tag) in world.get_components(CTransform, CVelocity, CTagPlayer):
        if ent == player_entity:
            c_t = c_transform
            c_v = c_velocity
            break
    
    if c_t is None or c_v is None:
        print("Jugador no encontrado para el dash.")
        return

    # Calcular dirección hacia el mouse
    dx = mouse_pos[0] - c_t.pos.x
    dy = mouse_pos[1] - c_t.pos.y
    distancia = math.hypot(dx, dy)
    if distancia == 0:
        return

    # Normalizar dirección
    dir_x = dx / distancia
    dir_y = dy / distancia

    # Aplicar velocidad de dash
    dash_speed = 500  # puedes tunear esta velocidad a gusto
    c_v.vel.x = dir_x * dash_speed
    c_v.vel.y = dir_y * dash_speed
