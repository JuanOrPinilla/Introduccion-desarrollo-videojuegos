import pygame
import json

class CEnemySpawner:
    def __init__(self) -> None:
        
        with open('data/level_01.json','r') as file_level:
            level_data = json.load(file_level)
        
        self.spawn_events = level_data.get("enemy_spawn_events", [])  # Lista de eventos

        with open('data/enemies.json','r') as file_enemies:
            enemies_data = json.load(file_enemies)

        self.type_A = enemies_data.get("TypeA", {})
        self.type_B = enemies_data.get("TypeB", {})
        self.type_C = enemies_data.get("TypeC", {})
        self.type_D = enemies_data.get("TypeD", {})




        self.spawned = set()  # Conjunto para registrar eventos ya ejecutados
        self.elapsed_time = 0.0  # Tiempo acumulado
        

        
        