import math
import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_explosion_state import CExplosionState
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_dash import CTagDash
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator
      
def crear_cuadrado(ecs_world:esper.World,size:pygame.Vector2,pos:pygame.Vector2,
                   vel:pygame.Vector2,col:pygame.Color) -> int:
    
    cuad_entity = ecs_world.create_entity() #devuelve un entero
    ecs_world.add_component(cuad_entity,
                                    CSurface(size, col))
    ecs_world.add_component(cuad_entity,
                                    CTransform(pos))
    ecs_world.add_component(cuad_entity,
                                    CVelocity(vel))
    return cuad_entity
  
def create_sprite(ecs_world: esper.World, pos: pygame.Vector2, vel:pygame.Vector2, surface:pygame.Surface) -> int:
    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, CTransform(pos))
    ecs_world.add_component(sprite_entity, CVelocity(vel))
    ecs_world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity
    
def crear_cuadrado_enemigo(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    if "velocity_min" in enemy_info and "velocity_max" in enemy_info:
        # Es un asteroide
        vel_min = enemy_info["velocity_min"]
        vel_max = enemy_info["velocity_max"]
        vel_range = random.randrange(vel_min, vel_max)
        velocity = pygame.Vector2(
            random.choice([-vel_range, vel_range]),
            random.choice([-vel_range, vel_range])
        )
        enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
        world.add_component(enemy_entity, CTagEnemy())
        ServiceLocator.sounds_service.play(enemy_info["sound"])
        
    else:
        velocity = pygame.Vector2(0, 0)
        size = enemy_surface.get_size()
        size = (size[0] / enemy_info["animations"]["number_frames"] , size[1])
        hunter_entity = create_sprite(world, pos, velocity, enemy_surface)
        world.add_component(hunter_entity, CTagHunter())
        world.add_component(hunter_entity, CAnimation(enemy_info["animations"]))
        world.add_component(hunter_entity, CHunterState())
        world.add_component(hunter_entity, CTagEnemy())




def create_player_square(world:esper.World,player_info:dict, player_lvl_info:dict):
    player_surface = ServiceLocator.images_service.get(player_info["image"])
    size = player_surface.get_size()
    size = (size[0] / player_info["animations"]["number_frames"] , size[1])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size[0] / 2),
                         player_lvl_info["position"]["y"]- (size[1] /2 ))
    vel = pygame.Vector2(0,0)
    player_entity = create_sprite(world,pos,vel,player_surface)
    world.add_component(player_entity,CTagPlayer())
    world.add_component(player_entity, CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    return player_entity

def create_explosion_square(world:esper.World, explosion_cfg:dict,c_e_pos:pygame.Vector2):
    explosion_surface = ServiceLocator.images_service.get(explosion_cfg["image"])
    pos = c_e_pos
    vel = pygame.Vector2(0,0)
    
    explosion_entity = create_sprite(world,pos,vel,explosion_surface)
    world.add_component(explosion_entity,CTagExplosion())
    world.add_component(explosion_entity, CAnimation(explosion_cfg["animations"]))
    world.add_component(explosion_entity, CExplosionState())

    ServiceLocator.sounds_service.play(explosion_cfg["sound"])
    return explosion_entity
    
def create_bullet_square(world: esper.World, player_entity: int, bullet_info: dict, mouse_pos: tuple):
    
    p_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)
    
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size
    size = player_surface.area.size
    pos = pygame.Vector2(
        p_transform.pos.x + (size[0] / 2) - (bullet_size[0] / 2),
        p_transform.pos.y + (size[1] / 2) - (bullet_size[1] / 2)
    )

    mouse_vector = pygame.Vector2(mouse_pos) 
    direction = (mouse_vector - pos).normalize()
    vel = direction * bullet_info["velocity"]

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_info["sound"])
    return bullet_entity

def create_dash_effect(world: esper.World, player_entity: int, variacion_angle: float, mouse_pos: tuple):
    p_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)
    star_surface = ServiceLocator.images_service.get("assets/img/star.png")
    star_size = star_surface.get_rect().size

    size = player_surface.area.size
    pos_centro = pygame.Vector2(
        p_transform.pos.x + (size[0] / 2) - (star_size[0] / 2),
        p_transform.pos.y + (size[1] / 2) - (star_size[1] / 2)
    )

    mouse_vector = pygame.Vector2(mouse_pos)
    direction = (mouse_vector - pos_centro).normalize()
    reverse_dir = -direction

    angle_rad = math.radians(variacion_angle)
    rotated_dir = pygame.Vector2(
        reverse_dir.x * math.cos(angle_rad) - reverse_dir.y * math.sin(angle_rad),
        reverse_dir.x * math.sin(angle_rad) + reverse_dir.y * math.cos(angle_rad)
    )

    spawn_pos = pos_centro + rotated_dir * 10 


    vel = rotated_dir * 60

    star_entity = create_sprite(world, spawn_pos, vel, star_surface)
    world.add_component(star_entity, CTagDash())
    return star_entity

    
def crear_spawner(ecs_world:esper.World, level_data:dict):
    spawner_entity = ecs_world.create_entity() 
    ecs_world.add_component(spawner_entity,
                                    CEnemySpawner(level_data["enemy_spawn_events"]))
    
def create_input_player(world:esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_leftclick = world.create_entity()
    input_rightclick = world.create_entity()
    input_pause = world.create_entity()
    
    world.add_component(input_left,CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right,CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up,CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down,CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    world.add_component(input_leftclick, CInputCommand("PLAYER_FIRE", 1))
    world.add_component(input_rightclick, CInputCommand("DASH", 3))
    world.add_component(input_pause, CInputCommand("PAUSE_GAME", pygame.K_p))
    