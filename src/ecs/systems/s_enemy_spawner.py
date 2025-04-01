import esper
import pygame
import random


from src.create.prefab_creator import crear_cuadrado
from src.ecs.components.c_enemy_spawner import CEnemySpawner

enemigos_generados = set()
tiempo_total = 0 

def system_enemy_spawner(world: esper.World, delta_time):
    global tiempo_total
    tiempo_total += delta_time  # Acumula el tiempo total transcurrido en el juego

    components = world.get_components(CEnemySpawner)

    for entity, (level_info) in components:
        for element in level_info:
            for enemy in element.spawn_events:
                time_spawn = enemy['time']
                
                # Crear un identificador único para cada enemigo
                enemy_id = (enemy['position']['x'], enemy['position']['y'], enemy['enemy_type'])

                # Verificar si ya ha sido generado o si aún no ha llegado su tiempo de aparición
                if enemy_id in enemigos_generados or tiempo_total < time_spawn:
                    continue 

                enemigos_generados.add(enemy_id)  # Marcar como creado
                
                pos = pygame.Vector2(enemy['position']['x'], enemy['position']['y'])
                type = enemy['enemy_type']

                # Obtener atributos según el tipo de enemigo desde el diccionario dinámico
                enemy_data = element.enemies_types.get(type, {})

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