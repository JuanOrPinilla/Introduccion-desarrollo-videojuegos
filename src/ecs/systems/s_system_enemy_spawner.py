import esper
import pygame
import random


from src.create.prefab_creator import crear_cuadrado
from src.ecs.components.c_enemy_spawner import CEnemySpawner

enemigos_generados = set()

def system_enemy_spawner(world: esper.World, delta_time):
    components = world.get_components(CEnemySpawner)
    
    for entity, (level_info) in components:
        for element in level_info:
            for enemy in element.spawn_events:

                # Crear un identificador único para cada enemigo
                enemy_id = (enemy['position']['x'], enemy['position']['y'], enemy['enemy_type'])
                if enemy_id in enemigos_generados:
                    continue 
                
                enemigos_generados.add(enemy_id) #Marcar com creado
                
                pos = pygame.Vector2(enemy['position']['x'], enemy['position']['y'])
                type = enemy['enemy_type']

                # Obtener atributos según el tipo de enemigo
                enemy_data = getattr(element, f"type_{type[-1]}", None)
                if not enemy_data:
                    continue  # Si el tipo no es válido, ignorarlo
                
                size_x = enemy_data.get("size", {}).get("x", 0)
                size_y = enemy_data.get("size", {}).get("y", 0)
                v_min = enemy_data.get("velocity_min", 0)
                v_max = enemy_data.get("velocity_max", 0)
                r = int(enemy_data.get("color", {}).get("r", 255))
                g = int(enemy_data.get("color", {}).get("g", 255))
                b = int(enemy_data.get("color", {}).get("b", 255))

                size = pygame.Vector2(int(size_x), int(size_y))  # Tamaño del enemigo
                v_x = random.uniform(v_min, v_max)  # Velocidad en x
                v_y = random.uniform(v_min, v_max)  # Velocidad en y
                vel = pygame.Vector2(v_x, v_y) 
                color = pygame.Color(r, g, b)  
                
                crear_cuadrado(world, size, pos, vel, color)  # Crear el enemigo