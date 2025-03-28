import esper
import pygame


from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world:esper.World, delta_time):
    pass