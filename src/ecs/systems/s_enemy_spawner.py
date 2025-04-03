import esper
import pygame
import random


from src.create.prefab_creator import crear_cuadrado_enemigo
from src.ecs.components.c_enemy_spawner import CEnemySpawner, SpawnEventData

enemigos_generados = set()
tiempo_total = 0 

def system_enemy_spawner(world: esper.World, enemies_data:dict, delta_time:float):
    components = world.get_component(CEnemySpawner)
    c_spw:CEnemySpawner
    for _, c_spw in components:
        c_spw.current_time += delta_time
        spw_evt:SpawnEventData
        for spw_evt in c_spw.spawn_event_data:
            if c_spw.current_time >= spw_evt.time and not spw_evt.triggered:
                spw_evt.triggered = True
                crear_cuadrado_enemigo(world, spw_evt.position, enemies_data[spw_evt.enemy_type])
        
    