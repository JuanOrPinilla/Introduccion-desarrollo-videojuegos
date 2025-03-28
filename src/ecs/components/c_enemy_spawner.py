import pygame
import json

class CEnemySpawner:
    def __init__(self, size:pygame.Vector2, color:pygame.Color) -> None:
        
        with open('data/level.json','r') as file:
            level_data = json.load(file)
            
        self.spawn_events = level_data.get("enemy_spawn_events", [])  # Lista de eventos
        self.spawned = set()  # Conjunto para registrar eventos ya ejecutados
        self.elapsed_time = 0.0  # Tiempo acumulado

        
        