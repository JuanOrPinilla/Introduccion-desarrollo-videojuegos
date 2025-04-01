import pygame
import json

class CEnemySpawner:
    def __init__(self) -> None:
        
        with open('assets/cfg/level_01.json','r') as file_level:
            level_data = json.load(file_level)
        
        self.spawn_events = level_data.get("enemy_spawn_events", [])  # Lista de eventos

        with open('assets/cfg/enemies.json','r') as file_enemies:
            enemies_data = json.load(file_enemies)

        # Guardar todos los tipos de enemigos en un diccionario
        self.enemies_types = enemies_data
        
        self.spawned = set()  # Conjunto para registrar eventos ya ejecutados
        self.elapsed_time = 0.0  # Tiempo acumulado
        

        
        