import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.engine.service_locator import ServiceLocator

def system_persecution_player_hunter(world:esper.World, player_entity:int, level_cfg:dict, hunter_cfg:dict):
    v_chase = hunter_cfg["velocity_chase"]
    v_return = hunter_cfg["velocity_return"]
    d_chase = hunter_cfg["distance_start_chase"]
    d_start_return = hunter_cfg["distance_start_return"]

    player_t = world.component_for_entity(player_entity, CTransform)
    player_s = world.component_for_entity(player_entity, CSurface)

    player_center = player_t.pos + pygame.Vector2(
        player_s.area.width / 2,
        player_s.area.height / 2
    )

    components = world.get_components(CSurface, CTransform, CVelocity, CTagHunter)

    for ent, (c_s, c_t, c_v, c_h) in components:
        if c_h.initial_pos is None:
            c_h.initial_pos = c_t.pos.copy()

        hunter_center = c_t.pos + pygame.Vector2(
            c_s.area.width / 2,
            c_s.area.height / 2
        )

        # Distancia al jugador
        distance_to_player = hunter_center.distance_to(player_center)
        # Distancia al punto de origen
        distance_to_origin = hunter_center.distance_to(
            c_h.initial_pos + pygame.Vector2(c_s.area.width / 2, c_s.area.height / 2)
        )

        # INICIO persecución si jugador está cerca
        if not c_h.chasing and distance_to_player <= d_chase:
            ServiceLocator.sounds_service.play(hunter_cfg["sound_chase"])
            c_h.chasing = True
        # DETIENE persecución si hunter se aleja demasiado de su posición original
        elif c_h.chasing and distance_to_origin > d_start_return:
            c_h.chasing = False

        target_center = (
            player_center if c_h.chasing
            else c_h.initial_pos + pygame.Vector2(c_s.area.width / 2, c_s.area.height / 2)
        )

        direction = target_center - hunter_center
        distance_to_target = direction.length()
        return_tolerance = 1.0

        if distance_to_target > return_tolerance:
            direction = direction.normalize()
            speed = v_chase if c_h.chasing else v_return
            c_v.vel = direction * speed
        else:
            c_v.vel = pygame.Vector2(0, 0)
            if not c_h.chasing:
                c_t.pos = c_h.initial_pos.copy() 
