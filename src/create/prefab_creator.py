import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
      
def crear_cuadrado(ecs_world:esper.World,
                   size:pygame.Vector2,
                   pos:pygame.Vector2,
                   vel:pygame.Vector2,
                   col:pygame.Color
                   ):
    
    cuad_entity = ecs_world.create_entity() #devuelve un entero
    ecs_world.add_component(cuad_entity,
                                    CSurface(size, col))
    ecs_world.add_component(cuad_entity,
                                    CTransform(pos))
    ecs_world.add_component(cuad_entity,
                                    CVelocity(vel))
    
def crear_enemigos(ecs_world:esper.World):
    spawner_entity = ecs_world.create_entity() #devuelve un entero
    ecs_world.add_component(spawner_entity,
                                    CEnemySpawner())